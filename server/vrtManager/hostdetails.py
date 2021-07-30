import time

from vrtManager.connection import wvmConnect
from vrtManager.util import get_xml_path


def cpu_version(doc):
    for info in doc.xpath("/sysinfo/processor/entry"):
        elem = info.xpath("@name")[0]
        if elem == "version":
            return info.text
    return "Unknown"


class wvmHostDetails(wvmConnect):
    def get_memory_usage(self):
        """
        Function return memory usage on node.
        """
        all_mem = self.wvm.getInfo()[1]
        freemem = self.wvm.getMemoryStats(-1, 0)
        if isinstance(freemem, dict):
            free = round((freemem["buffers"] + freemem["free"] + freemem["cached"])/(1024),2)

            percent = abs(100 - ((free * 100) // all_mem))
            usage = all_mem - free
            mem_usage = {"total": all_mem, "usage": usage, "percent": percent}
        else:
            mem_usage = {"total": None, "usage": None, "percent": None}
        return mem_usage

    def get_host_status(self):
        status = {1:'已连接',-1:'异常'}
        res = self.wvm.isAlive()
        return status[res]

    def get_cpu_usage(self):
        """
        Function return cpu usage on node.
        """
        prev_idle = 0
        prev_total = 0
        cpu = self.wvm.getCPUStats(-1, 0)
        if isinstance(cpu, dict):
            for num in range(2):
                idle = self.wvm.getCPUStats(-1, 0)["idle"]
                total = sum(self.wvm.getCPUStats(-1, 0).values())
                diff_idle = idle - prev_idle
                diff_total = total - prev_total
                diff_usage = (1000 * (diff_total - diff_idle) / diff_total + 5) / 10
                prev_total = total
                prev_idle = idle
                if num == 0:
                    time.sleep(1)
                else:
                    if diff_usage < 0:
                        diff_usage = 0
        else:
            return {"usage": None}
        return {"usage": diff_usage}

    def get_connect_info(self):
        """
        Function return host server information: hostname, cpu, memory, ...
        """
        info = dict()
        #info['id'] = 1
        info['status'] = self.get_host_status()
        info['user'] = ''
        info['instance_count'] = len(self.get_instances())
        info['hostname'] = self.wvm.getHostname() # hostname
        info['memory'] = self.get_memory_usage()['total']  # memory
        info['use_memory_percent'] = self.get_memory_usage()['percent']
        info['vcpu'] = self.wvm.getInfo()[2]  # cpu core count
        # info['arch'] = self.wvm.getInfo()[0]  # architecture
        # info['use_memory'] = self.get_memory_usage()['usage']
        # info['cpu_usage'] = self.get_cpu_usage()['usage']
        # info['cpu_version'] = get_xml_path(self.wvm.getSysinfo(0), func=cpu_version)  # cpu version
        # info['uri'] = self.wvm.getURI()  # uri
        return info
    def get_host_detail(self):
        detail = {}
        detail['hostname'] = self.wvm.getHostname()  # hostname
        detail['hypervisors_domain_types'] = self.get_hypervisors_domain_types() # 虚拟机管理程序
        detail['simulator'] = self.get_emulator(self.wvm.getInfo()[0]) # 模拟器
        detail['qemu_lib_version'] = {'qemu': self.get_version(),'lib':self.get_lib_version()}
        detail['memory'] = self.get_memory_usage()['total']  # memory
        detail['arch'] = self.wvm.getInfo()[0]  # architecture
        detail['vcpu'] = self.wvm.getInfo()[2]  # cpu core count
        detail['cpu_version'] = get_xml_path(self.wvm.getSysinfo(0), func=cpu_version)  # cpu version
        detail['uri'] = self.wvm.getURI()  # uri
        detail['describe'] = ''

        return detail

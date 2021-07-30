<template>
  <el-container class="dashboard-container">
    <el-header>
      <h1>{{ Instance_info.hostname }}</h1>
    </el-header>
    <el-main>
      <template>
        <el-tabs v-model="activeName" @tab-click="handleClick">
          <!--          <el-tab-pane label="电源" name="power">用户管理</el-tab-pane>-->
          <!--          <el-tab-pane label="访问" name="visit">配置管理</el-tab-pane>-->
          <el-tab-pane label="调整配置" name="resize">
            <template>
              <el-tabs v-model="resizeName" style="width: 80%;margin-left: 10%;margin-top: 20px" type="card" @tab-click="handleResize">
                <el-tab-pane label="CPU" name="resizeCPU">
                  <b style="margin: 15px">逻辑主机CPU: {{ Instance_resize_cmd.host_cpu }}</b>
                  <div style="margin:30px">
                    <label style="margin-right: 30px">当前分配：</label>
                    <template>
                      <el-select v-model="cur_vcpu" placeholder="请选择">
                        <el-option
                          v-for="item in Instance_resize_cmd.vcpu_range"
                          :key="item"
                          :label="item"
                          :value="item"
                        />
                      </el-select>
                    </template>
                  </div>
                  <div style="margin: 30px">
                    <label style="margin-right: 30px">最大分配：</label>
                    <template>
                      <el-select v-model="vcpu" placeholder="请选择">
                        <el-option
                          v-for="item in Instance_resize_cmd.vcpu_range"
                          :key="item"
                          :label="item"
                          :value="item"
                        />
                      </el-select>
                    </template>
                  </div>
                  <el-button type="primary" @click="resizeCPU('resize_cpu')">提交</el-button>
                </el-tab-pane>
                <el-tab-pane label="内存" name="resizeMemory">
                  <b v-if="Instance_resize_cmd.host_memory >1024" style="margin: 15px">主机总内存: {{ (Instance_resize_cmd.host_memory/1024).toFixed(1) }} GB</b>
                  <b v-else style="margin: 15px">主机总内存: {{ Instance_resize_cmd.host_memory }} MB</b>
                  <div style="margin:30px">
                    <label style="margin-right: 30px">当前分配(MB)：</label>
                    <template>
                      <el-select
                        v-model="cur_memory"
                        allow-create
                        filterable
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="item in Instance_resize_cmd.memory_range"
                          :key="item"
                          :label="item"
                          :value="item"
                        />
                      </el-select>
                    </template>
                  </div>
                  <div style="margin: 30px">
                    <label style="margin-right: 30px">最大分配(MB)：</label>
                    <template>
                      <el-select v-model="memory" allow-create filterable placeholder="请选择">
                        <el-option
                          v-for="item in Instance_resize_cmd.memory_range"
                          :key="item"
                          :label="item"
                          :value="item"
                        />
                      </el-select>
                    </template>
                  </div>
                  <el-button type="primary" @click="resizeMemory('resize_mem')">提交</el-button>
                </el-tab-pane>
                <el-tab-pane label="磁盘" name="resizeDisc">
                  <b>磁盘分配(GB):</b>
                  <div v-if="Instance_resize_cmd.disk <1" style="margin: 20px">
                    <el-alert
                      title="获取磁盘信息时出错"
                      type="error"
                      effect="dark"
                    />
                  </div>
                  <div v-else>
                    <label style="margin-right: 30px">当前分配 (vda)：</label>
                    <div v-for="(item,index) in Instance_resize_cmd.disk" :key="index" style="margin: 30px">
                      <el-input-number v-model="new_disk[index]" />
                    </div>
                    <el-button type="primary" @click="resizeDisk('resize_disk')">提交</el-button>
                  </div>
                </el-tab-pane>
              </el-tabs>
            </template>
          </el-tab-pane>
          <el-tab-pane label="设置" name="set">
            <template>
              <el-tabs v-model="setName" style="width: 80%;margin-left: 10%;margin-top: 20px" type="card" @tab-click="handleSet">
                <el-tab-pane label="XML" name="XML" />
              </el-tabs>
            </template>
          </el-tab-pane>
          <el-tab-pane label="状态" name="status">定时任务补偿</el-tab-pane>
          <el-tab-pane label="销毁" name="destroy">定时任务补偿</el-tab-pane>
        </el-tabs>
      </template>
    </el-main>
    <el-footer>
      主机
    </el-footer>
  </el-container>
</template>

<script>
import { get_instance_info } from '@/api/instance'
import { getInstance_name } from '@/utils/virt-info'
import { get_instance_resize_cmd, post_instance_resize_cmd } from '@/api/instance'

export default {
  name: 'Instance',
  data() {
    return {
      activeName: 'resize',
      setName: 'XML',
      resizeName: 'resizeCPU',
      Instance_info: [],
      Instance_resize_cmd: [],
      cur_vcpu: '',
      vcpu: '',
      cur_memory: '',
      memory: '',
      new_disk: []
    }
  },
  created() {
    this.get_InstanceResizeCMD(getInstance_name())
    get_instance_info(getInstance_name()).then(res => {
      this.Instance_info = res.data
    }).catch(_ => {
    })
  },
  methods: {
    handleClick(tab, event) {
      if (tab.name === 'resize') {
        this.get_InstanceResizeCMD(getInstance_name())
      }
    },
    handleResize(tab, event) {
      if (tab.name === 'resizeCPU') {
        console.log(tab, event)
      }
    },
    handleSet(tab, event) {
      if (tab.name === 'XML') {
        console.log(tab, event)
      }
    },
    post_InstanceResizeCMD(row, name, method) {
      post_instance_resize_cmd(name, { 'name': name, 'method': method }).then(res => {
      }).catch(_ => {
      })
    },
    get_InstanceResizeCMD(name) {
      get_instance_resize_cmd(name).then(res => {
        this.Instance_resize_cmd = res.data
        this.cur_vcpu = res.data.cur_vcpu
        this.vcpu = res.data.vcpu
        this.cur_memory = res.data.cur_memory
        this.memory = res.data.memory
        for (let i = 0, len = res.data.disk.length; i < len; i++) {
          this.new_disk.push((res.data.disk[i].size / 1024 ** 3).toFixed(1))
        }
      }).catch(_ => {
      })
    },
    resizeCPU(method) {
      post_instance_resize_cmd(getInstance_name(), { 'cur_vcpu': this.cur_vcpu, 'vcpu': this.vcpu, 'method': method })
        .then(res => {
        })
    },
    resizeMemory(method) {
      const cur_memory = parseInt(this.cur_memory)
      const memory = parseInt(this.memory)
      if (cur_memory > 0 && cur_memory <= this.Instance_resize_cmd.host_memory && cur_memory > 0 && cur_memory <= this.Instance_resize_cmd.host_memory && cur_memory <= memory) {
        post_instance_resize_cmd(getInstance_name(), {
          'cur_memory': cur_memory,
          'memory': memory,
          'method': method
        })
          .then(res => {
            console.log(res)
          })
      }
    },
    resizeDisk(method) {
      for (let i = 0, len = this.Instance_resize_cmd.disk.length; i < len; i++) {
        this.Instance_resize_cmd.disk[i].new_disk = this.new_disk[i] * (2 ** 30)
      }
      post_instance_resize_cmd(getInstance_name(), {
        'disks': this.Instance_resize_cmd.disk,
        'method': method
      })
        .then(res => {
          console.log(res)
        })
    }
  }
}
</script>

<style lang="scss" scoped>

.dashboard {
  &-container {
    margin: 30px;
  }

  &-search {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>

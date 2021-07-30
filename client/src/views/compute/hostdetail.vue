<template>
  <el-tabs v-model="activeName" class="detail_data" type="border-card" @tab-click="handleClick">
    <el-tab-pane label="概览" name="info">
      <el-divider><h2>概览</h2></el-divider>
      <el-main id="gailan-info">
        <h3>基本细节</h3>
        <el-row class="hostname">
          <el-col :span="8"><p>主机</p></el-col>
          <el-col :span="12"><p> {{ Info.hostname }}</p></el-col>
        </el-row>
        <el-row class="xuniji">
          <el-col :span="8"><p>虚拟机管理程序</p></el-col>
          <el-col :span="12">
            <el-dropdown v-for="(value, key) in Info.hypervisors_domain_types" :key="key" size="mini" placement="top">
              <el-tag size="mini" type="info">{{ key }}</el-tag>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item v-for="item in value" :key="item">{{ item }}</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </el-col>
        </el-row>
        <el-row class="moniqi">
          <el-col :span="8"><p>模拟器</p></el-col>
          <el-col :span="12"><p>{{ Info.simulator }}</p></el-col>
        </el-row>
        <el-row class="banben">
          <el-col :span="8"><p>版本</p></el-col>
          <el-col v-for="(value, key) in Info.qemu_lib_version" :key="key" :span="12">
            <el-tag size="mini" effect="dark">{{ key }}</el-tag>
            <el-tag size="mini" effect="plain">{{ value }}</el-tag>
          </el-col>
        </el-row>
        <el-row class="neicun">
          <el-col :span="8"><p>内存</p></el-col>
          <el-col v-if="Info.memory >1024" :span="12"><p>{{ (Info.memory/1024).toFixed(1) }} GB</p></el-col>
          <el-col v-else :span="12"><p>{{ Info.memory }} MB</p></el-col>
        </el-row>
        <el-row class="jiagou">
          <el-col :span="8"><p>架构</p></el-col>
          <el-col :span="12"><p>{{ Info.arch }}</p></el-col>
        </el-row>
        <el-row class="vcpu">
          <el-col :span="8"><p>逻辑CPU</p></el-col>
          <el-col :span="12"><p>{{ Info.vcpu }}</p></el-col>
        </el-row>
        <el-row class="chuliqi">
          <el-col :span="8"><p>处理器</p></el-col>
          <el-col :span="12"><p>{{ Info.cpu_version }}</p></el-col>
        </el-row>
        <el-row class="lianjie">
          <el-col :span="8"><p>连接</p></el-col>
          <el-col :span="12"><p>{{ Info.uri }}</p></el-col>
        </el-row>
        <el-row class="xijie">
          <el-col :span="8"><p>细节(描述)</p></el-col>
          <el-col :span="12"><p>{{ Info.describe || '' }}</p></el-col>
        </el-row>
      </el-main>
      <!-- <el-footer>
        <h3>性能</h3>
      </el-footer> -->
    </el-tab-pane>
    <el-tab-pane label="实例" name="instance">
      <el-divider><h2>实例</h2></el-divider>
      <div class="virt_maintain">
        展示信息
        <InstanceTab ref="instance_tab" />
      </div>
    </el-tab-pane>
    <el-tab-pane label="存储" name="memory">
      <div v-for="(item,index) in Storages_info" :key="index">
        <el-card class="box-card" style="margin-bottom: 10px">
          <div v-if="item.status===1" slot="header" class="clearfix">
            <el-link type="primary">{{ item.name }}</el-link>
          </div>
          <div v-else slot="header" class="clearfix">
            <el-link type="danger">{{ item.name }}</el-link>
          </div>
          <div>
            <el-row>
              <el-col :span="10">类型</el-col>
              <el-col :span="14">{{ item.type }}</el-col>
            </el-row>
            <el-row>
              <el-col :span="10">大小</el-col>
              <el-col :span="14">{{ item.size }} GB</el-col>
            </el-row>
            <el-row>
              <el-col :span="10">卷</el-col>
              <el-col :span="14">{{ item.volumes }}</el-col>
            </el-row>
          </div>
        </el-card>
      </div>
    </el-tab-pane>
    <el-tab-pane label="网络" name="net">
      <div v-for="(item,index) in Nets_info" :key="index">
        <el-card class="box-card" style="margin-bottom: 10px">
          <div v-if="item.status===1" slot="header" class="clearfix">
            <el-link type="primary">{{ item.name }}</el-link>
          </div>
          <div v-else slot="header" class="clearfix">
            <el-link type="danger">{{ item.name }}</el-link>
          </div>
          <div>
            <el-row>
              <el-col :span="10">设备</el-col>
              <el-col :span="14">{{ item.device }}</el-col>
            </el-row>
            <el-row>
              <el-col :span="10">转发</el-col>
              <el-col :span="14">{{ item.forward }}</el-col>
            </el-row>
          </div>
        </el-card>
      </div>
    </el-tab-pane>
    <el-tab-pane label="接口" name="interface">
      <InterfacesInfo ref="interfaces_info" />
    </el-tab-pane>
    <el-tab-pane label="NWFilter规则" name="NWFilter">
      <el-table
        :data="NWFilters_info"
        style="width: 100%;margin-top: 10px"
        row-key="hostname"
        border
        default-expand-all
        :default-sort="{prop: 'uuid', order: 'descending'}"
      >
        <el-table-column
          label="id"
          :span="3"
        >
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.$index }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="UUID"
          :span="6"
          sortable
        >
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.uuid }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="名称"
          :span="6"
        >
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.name }}</span>
          </template>
        </el-table-column>
        <el-table-column label="应用" :span="9">
          <template slot-scope="scope">
            <el-button
              size="small"
              round
              title="查看"
              type="primary"
              @click="InstanceStatusControl(scope.$index, scope.row.hostname, 'start')"
            ><i class="el-icon-view" /> </el-button>
            <el-button
              size="small"
              round
              type="primary"
              title="克隆"
              @click="InstanceStatusControl(scope.$index, scope.row.hostname, 'suspend')"
            ><i class="el-icon-document-copy" /></el-button>
            <el-button
              size="small"
              round
              type="danger"
              title="删除"
              @click="InstanceStatusControl(scope.$index, scope.row.hostname, 'shutdown')"
            ><i class="el-icon-delete" /></el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-tab-pane>
    <el-tab-pane label="密码密钥" name="secrets">
      <div v-if="Secrets_info.length<1">
        <span>密码为空</span>
      </div>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
// import { mapGetters } from 'vuex'
import InstanceTab from '@/components/Instance'
import InterfacesInfo from '@/components/Interfaces'
import { get_host_detail,
  get_host_storages_info, get_host_nets_info, get_host_nwfilters_info,
  get_host_secrets_info } from '@/api/connection'

export default {
  name: 'Hostdetail',
  components: {
    InstanceTab,
    InterfacesInfo
  },
  data() {
    return {
      activeName: 'info',
      // Instances_info: [],
      Info: [],
      Storages_info: [],
      Nets_info: [],
      NWFilters_info: [],
      Secrets_info: []
    }
  },
  created() {
    this.info()
  },
  // computed: {
  //   ...mapGetters([
  //     'virt_host'
  //   ])
  // },
  methods: {
    handleClick(tab, event) {
      if (tab.name === 'info') {
        this.info()
      } else if (tab.name === 'instance') {
        this.$refs.instance_tab.instance()
      } else if (tab.name === 'memory') {
        this.memory()
      } else if (tab.name === 'net') {
        this.net()
      } else if (tab.name === 'interface') {
        this.$refs.interfaces_info.interface()
      } else if (tab.name === 'NWFilter') {
        this.NWFilter()
      } else if (tab.name === 'secrets') {
        this.Secret()
      } else if (tab.name === 'historys') {
        this.Historys()
      }
    },
    info() {
      get_host_detail().then(res => {
        this.Info = res.data
      }).catch(_ => {
      })
    },
    memory() {
      get_host_storages_info().then(res => {
        this.Storages_info = res.data || []
      })
    },
    net() {
      get_host_nets_info().then(res => {
        this.Nets_info = res.data || []
      })
    },
    NWFilter() {
      get_host_nwfilters_info().then(res => {
        this.NWFilters_info = res.data
      })
    },
    Secret() {
      get_host_secrets_info().then(res => {
        this.Secrets_info = res.data
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.detail_data {
  margin-top: 50px;
  width: 80%;
  margin-left: 10%;

  .el-tag {
    margin-left: 10px;
    margin-top: 15px;
}
}
</style>

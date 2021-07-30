<template>
  <el-container class="dashboard-container">
    <el-header>
      <h1>计算节点</h1>
    </el-header>
    <el-main>
      <el-row class="dashboard-search" style="margin-top: 15px;">
        <el-col :span="4">
          <el-button type="primary" icon="el-icon-circle-plus-outline" @click="vir_connection_Visible = true">新建连接</el-button>
          <!-- 建立连接 -->
          <el-dialog title="新建连接" :visible.sync="vir_connection_Visible" width="50%">
            <el-form ref="virt_connection_form" :model="virt_connection_form" :rules="virt_connection_rules" auto-complete="on" label-width="20%">
              <el-form-item label="主机IP" prop="hostip">
                <el-input ref="host" v-model="virt_connection_form.hostip" name="host" type="text" tabindex="1" auto-complete="on" />
              </el-form-item>
              <el-form-item label="用户名" prop="user">
                <el-input ref="name" v-model="virt_connection_form.user" tabindex="2" />
              </el-form-item>
              <el-form-item label="密码" prop="password">
                <el-input ref="passwd" v-model="virt_connection_form.password" tabindex="3" auto-complete="on" />
              </el-form-item>
              <el-form-item label="连接类型" prop="type">
                <el-select ref="type" v-model="virt_connection_form.type" tabindex="4" placeholder="please select connection type">
                  <el-option label="tcp" value="1" />
                  <el-option label="ssh" value="2" />
                  <el-option label="tls" value="3" />
                  <el-option label="socket" value="4" />
                </el-select>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" :loading="loading" @click.native.prevent="vir_connection_submit()">连接</el-button>
                <el-button @click="vir_connection_Visible = false">取消</el-button>
              </el-form-item>
            </el-form>
          </el-dialog>
        </el-col>
        <el-col :span="20" style="margin-right: 0" />
      </el-row>
      <div>
        <!-- 展示信息 -->
        <el-table
          ref="compute_info"
          v-loading="loading"
          :data="virt_data_table"
          style="width: 100%;margin-top: 10px"
          row-key="hostname"
          border
          default-expand-all
          :header-cell-style="{ background: '#fafafa' }"
        >
          <!-- 子列表 -->
          <!--          <el-table-column-->
          <!--            label="#"-->
          <!--            width="40"-->
          <!--          >-->
          <!--            <template slot-scope="scope">-->
          <!--              <i class="icon-prev" @click="showInstanceInfo(scope.row)" />-->
          <!--            </template>-->
          <!--          </el-table-column>-->
          <!--          <el-table-column prop="items" type="expand" width="1">-->
          <!--            <template slot-scope="scope">-->
          <!--              <el-table :data="scope.row.items" stripe style="width: 100%">-->
          <!--                <el-table-column type="index"></el-table-column>-->
          <!--                <el-table-column type="port" label="名字"></el-table-column>-->
          <!--              </el-table>-->
          <!--            </template>-->
          <!--          </el-table-column>-->
          <!-- 子列表结束 -->
          <el-table-column
            label="主机"
            width="150"
            property="hostname"
            header-align="center"
            align="left"
            :show-overflow-tooltip="true"
            :render-header="renderHeader"
          >
            <template slot-scope="{ row, $index }">
              <a v-if="row.message==='已连接'" class="clearfix" @click="handleEdit(row, $index)"><i class="el-icon-info" />{{ row.hostname }} <el-badge :value="row.instance_count" class="mark" /></a>
              <p v-else class="clearfix"><i class="el-icon-info" />{{ row.hostname }} <el-badge :value="row.instance_count" class="mark" /></p><el-popover>
                ref="popover4"
                placement="right"
                width="400"
                trigger="click">
                <div />
              </el-popover>
              <!--              <router-link :to="{path:'/compute/detail/'+scope.row.hostname, query:{token: scope.row.token }}">-->
              <!--                <i class="el-icon-info" />{{ scope.row.hostname }}</router-link>-->
            </template>
          </el-table-column>
          <el-table-column
            label="用户"
            min-width="100"
            property="user"
            :show-overflow-tooltip="true"
            :render-header="renderHeader"
          >
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.user }}</span>
            </template>
          </el-table-column>
          <el-table-column
            label="状态"
            min-width="100"
            property="status"
            :show-overflow-tooltip="true"
            :render-header="renderHeader"
          >
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.message }}</span>
            </template>
          </el-table-column>
          <el-table-column
            label="vcpu"
            min-width="100"
            property="vcpu"
            :show-overflow-tooltip="true"
            :render-header="renderHeader"
          >
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.vcpu }}</span>
            </template>
          </el-table-column>
          <el-table-column
            label="内存"
            min-width="100"
            property="memory"
            :show-overflow-tooltip="true"
            :render-header="renderHeader"
          >
            <template slot-scope="scope">
              <span v-if="scope.row.memory > 1024 " style="margin-left: 10px">{{ (scope.row.memory/1024).toFixed(1) }} GB</span>
              <span v-else style="margin-left: 10px">{{ scope.row.memory }} MB</span>
            </template>
          </el-table-column>
          <el-table-column
            label="内存使用率"
            min-width="120"
            property="use_memory_percent"
            :show-overflow-tooltip="true"
            :render-header="renderHeader"
          >
            <template slot-scope="scope">
              <el-progress :text-inside="true" :stroke-width="26" :percentage="scope.row.use_memory_percent" />
            </template>
          </el-table-column>
          <el-table-column label="操作" min-width="150" :show-overflow-tooltip="true">
            <template slot-scope="{ row, $index }">
              <el-button
                v-if="row.message === '已连接'"
                size="mini"
                type="primary"
                @click="handleEdit(row, $index)"
              >编辑</el-button>
              <el-button
                v-else
                size="mini"
              >编辑</el-button>
              <el-button
                size="mini"
                type="danger"
                @click="handleDelete(row, $index)"
              >删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import { mapGetters } from 'vuex'
// import InstanceTab from '@/components/Instance'
import { validHost } from '@/utils/validate'
import { get_host_info, connect_host, disconnect_host } from '@/api/connection'
import { setVirt_connect_token } from '@/utils/virt-info'
export default {
  name: 'Compute',
  data() {
    const validateHost = (rule, value, callback) => {
      if (!validHost(value)) {
        callback(new Error('请输入正确的地址'))
      } else {
        callback()
      }
    }
    return {
      show: false,
      expands: [],
      search_by_name: '',
      vir_connection_Visible: false,
      virt_message: '',
      virt_data_table: [],
      virt_connection_form: {
        hostip: '',
        user: '',
        password: '',
        type: ''
      },
      virt_connection_rules: {
        hostip: [{ required: true, trigger: 'blur', validator: validateHost }]
      },
      loading: false,
      redirect: undefined
    }
  },
  computed: {
    ...mapGetters([
      'user_name',
      'virt_host'
    ])
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  created() {
    get_host_info().then(res => {
      for (let i = 0, len = res.data.length; i < len; i++) {
        this.virt_data_table.push(res.data[i])
      }
      console.log(this.virt_data_table)
    })
      .catch(_ => {
      })
  },
  methods: {
    renderHeader(h, data) {
      return h('span', [
        h(
          'el-tooltip',
          {
            attrs: {
              class: 'item',
              effect: 'dark',
              content: data.column.label,
              placement: 'top'
            }
          },
          [h('span', data.column.label)]
        )
      ])
    },
    showInstanceInfo(row) {
      const $table = this.$refs.compute_info
      $table.toggleRowExpansion(row)
    },
    vir_connection_submit() {
      this.$refs.virt_connection_form.validate(valid => {
        if (valid) {
          // this.$router.push({ path: this.redirect || '/' })
          var param = new URLSearchParams(this.virt_connection_form)
          this.$confirm('确认提交？').then(_ => {
            connect_host(param).then(res => {
              this.vir_connection_Visible = false
              this.virt_data_table.push(res.data)
              this.$store.dispatch('virt_connection/connection', { 'info': this.virt_connection_form, 'token': res.virt_connect_tokens })
            })
              .catch(_ => {
              })
            this.vir_connection_Visible = false
          }).catch(() => {
            // this.loading = false
            this.vir_connection_Visible = false
          })
        } else {
          console.log('错误提交！！')
          return false
        }
      })
    },
    handleDelete(row, $index) {
      setVirt_connect_token(row.token)
      disconnect_host(row.hostname).then(res => {
        this.virt_data_table.pop(row)
      })
    },
    handleEdit(row, $index) {
      setVirt_connect_token(row.token)
      this.$router.push({
        path: `/compute/detail/${row.hostname}`
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

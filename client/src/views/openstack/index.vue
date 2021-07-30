<template>
  <el-container class="dashboard-container">
    <el-header>
      <h1>Openstack</h1>
    </el-header>
    <el-main>
      <template>
        <el-row class="dashboard-search" style="margin-top: 15px;">
          <el-col :span="4">
            <el-button type="primary" icon="el-icon-circle-plus-outline" @click="openstack_connection_Visible = true">
              新建连接
            </el-button>
            <!-- 建立连接 -->
            <el-dialog title="新建连接" :visible.sync="openstack_connection_Visible" width="50%">
              <el-form ref="openstack_connection_form"
                       :model="openstack_connection_form"
                       :rules="openstack_connection_rules"
                       auto-complete="on"
                       label-width="20%"
              >
                <el-form-item label="主机IP" prop="auth_ip">
                  <el-input ref="host"
                            v-model="openstack_connection_form.auth_ip"
                            name="host"
                            type="text"
                            tabindex="1"
                            auto-complete="on"
                  />
                </el-form-item>
                <el-form-item label="平台名称" prop="platename">
                  <el-input ref="platename" v-model="openstack_connection_form.platename" name="platename" type="text" tabindex="2" auto-complete="on" />
                </el-form-item>
                <el-form-item label="用户" prop="user">
                  <el-input ref="user"
                            v-model="openstack_connection_form.user.value"
                            placeholder="请输入内容"
                            class="input-with-select"
                            tabindex="3"
                            auto-complete="on"
                  >
                    <el-select slot="prepend"
                               v-model="openstack_connection_form.user.type"
                               placeholder="请选择"
                               style="width: 100px"
                    >
                      <el-option label="name" value="user_name" />
                      <el-option label="id" value="user_id" />
                    </el-select>
                  </el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                  <el-input ref="password"
                            v-model="openstack_connection_form.password"
                            type="password"
                            tabindex="4"
                            auto-complete="on"
                  />
                </el-form-item>
                <el-form-item label="domain" prop="domain">
                  <el-input ref="user"
                            v-model="openstack_connection_form.domain.value"
                            placeholder="请输入内容"
                            class="input-with-select"
                            tabindex="5"
                            auto-complete="on"
                  >
                    <el-select slot="prepend"
                               v-model="openstack_connection_form.domain.type"
                               placeholder="请选择"
                               style="width: 100px"
                    >
                      <el-option label="name" value="domain_name" />
                      <el-option label="id" value="domain_id" />
                    </el-select>
                  </el-input>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary"
                             :loading="loading"
                             @click.native.prevent="openstack_connection_submit(Openstack_Info_Value)"
                  >连接
                  </el-button>
                  <el-button @click="openstack_connection_Visible = false">取消</el-button>
                </el-form-item>
              </el-form>
            </el-dialog>
          </el-col>
          <el-col :span="20" style="margin-right: 0" />
        </el-row>
        <el-tabs v-model="Openstack_Info_Value"
                 type="card"
                 closable
                 style="margin-top: 20px"
                 @tab-remove="removeTab(Openstack_Info_Value)"
                 @tab-click="clickTab"
        >
          <el-tab-pane
            v-for="(item, image_index) in Openstack_Info"
            :key="item.id_md5"
            :label="item.platename || item.auth_ip"
            :name="item.id_md5"
          >
            <!--            <ImageList ref="Image_Table" />-->
            <template>
              <div class="dormitory">
                <div class="top" style="width: 60%;margin: 10px 20%">
                  <el-tooltip class="item" effect="dark" content="IP" placement="top-start">
                    <el-button>{{ item.auth_ip }}</el-button>
                  </el-tooltip>
                  <el-tooltip class="item" effect="dark" content="用户" placement="top">
                    <el-button>{{ item.user_name }}</el-button>
                  </el-tooltip>
                  <el-tooltip class="item" effect="dark" content="Domain" placement="top-end">
                    <el-button>{{ item.domain_name||'default' }}</el-button>
                  </el-tooltip>
                </div>
                <div class="searchWord">
                  <el-input v-model="search"
                            style="display: inline-block;width: 90%;margin-left: 5%"
                            placeholder="请输入搜索内容"
                  />
                </div>

                <el-table
                  ref="filterImageTable"
                  :key="tabIndex"
                  :data="(item.Image_Info || []).filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase())).slice((currentPage - 1) * PageSize, currentPage * PageSize)"
                  stripe
                  style="width: 90%;margin-left: 5%;margin-top: 20px"
                  :default-sort="{prop: 'owner', order: 'descending'}"
                >
                  <el-table-column type="expand">
                    <template #default="props">
                      <el-form label-position="left" inline class="detail-table-expand">
                        <el-form-item ref="ID" label="ID" class="image-detail-item">
                          <span>{{ props.row.id }}</span>
                        </el-form-item>
                        <el-form-item label="名称" class="image-detail-item">
                          <span>{{ props.row.name }}</span>
                        </el-form-item>
                        <el-form-item label="checksum" class="image-detail-item">
                          <span>{{ props.row.checksum }}</span>
                        </el-form-item>
                        <el-form-item label="File" class="image-detail-item">
                          <span>{{ props.row.file }}</span>
                        </el-form-item>
                        <el-form-item label="可见性" class="image-detail-item">
                          <span>{{ props.row.visibility }}</span>
                        </el-form-item>
                        <el-form-item label="受保护的" class="image-detail-item">
                          <span>{{ props.row.protected }}</span>
                        </el-form-item>
                        <el-form-item label="磁盘格式" class="image-detail-item">
                          <span>{{ props.row.disk_format }}</span>
                        </el-form-item>
                        <el-form-item label="大小" class="image-detail-item">
                          <span>{{ convertSize(props.row) }}</span>
                        </el-form-item>
                        <!--                      <el-history-item label="虚拟磁盘大小" class="image-detail-item">-->
                        <!--                        <span>{{ props.row.virtual_size }}</span>-->
                        <!--                      </el-history-item>-->
                        <el-form-item label="最小磁盘大小" class="image-detail-item">
                          <span>{{ props.row.min_disk }}</span>
                        </el-form-item>
                        <el-form-item label="最小内存" class="image-detail-item">
                          <span>{{ props.row.min_ram }}</span>
                        </el-form-item>
                        <el-form-item label="Disc Bus" class="image-detail-item">
                          <span>{{ props.row.hw_disk_bus }}</span>
                        </el-form-item>
                        <el-form-item label="Firmware Type" class="image-detail-item">
                          <span>{{ props.row.hw_firmware_type }}</span>
                        </el-form-item>
                        <el-form-item label="SCSI Model" class="image-detail-item">
                          <span>{{ props.row.hw_scsi_model }}</span>
                        </el-form-item>
                      </el-form>
                    </template>
                  </el-table-column>
                  <el-table-column
                    prop="id"
                    label="id"
                    width="180"
                    sortable
                  />
                  <el-table-column
                    prop="name"
                    label="名称"
                    width="180"
                    sortable
                  />
                  <el-table-column
                    prop="status"
                    label="状态"
                  />
                  <el-table-column
                    prop="os_hidden"
                    label="是否隐藏"
                    :formatter="convertStr"
                    :filters="[{ text: '是', value: 'true' }, { text: '否', value: 'false' }]"
                    :filter-method="filterSelect"
                    filter-placement="bottom-end"
                  />
                  <el-table-column
                    prop="disk_format"
                    label="磁盘格式"
                  />
                  <el-table-column
                    prop="size"
                    label="大小"
                    :formatter="convertSize"
                  />
                  <el-table-column
                    prop="updated_at"
                    label="修改日期"
                    sortable
                  />
                  <el-table-column
                    prop="created_at"
                    label="创建日期"
                    sortable
                  />
                  <el-table-column
                    property="os_hidden"
                    label="操作"
                  >
                    <template slot-scope="scope">
                      <el-button v-if="scope.row.os_hidden"
                                 type="primary"
                                 @click="update_image(scope.$index,image_index, scope.row.id,{'os_hidden':false,'id_md5':item.id_md5})"
                      >
                        恢复
                      </el-button>
                      <el-button v-else
                                 type="primary"
                                 @click="update_image(scope.$index,image_index, scope.row.id,{'os_hidden':true,'id_md5':item.id_md5})"
                      >
                        隐藏
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
                <div style="width:80%;margin:30px 10%">
                  <el-pagination :current-page="currentPage"
                                 :page-sizes="pageSizes"
                                 :page-size="PageSize"
                                 layout="total, sizes, prev, pager, next, jumper"
                                 :total="totalCount"
                                 @size-change="size_change"
                                 @current-change="current_change"
                  />
                </div>
              </div>
            </template>
          </el-tab-pane>
        </el-tabs>
      </template>
    </el-main>
  </el-container>
</template>

<script>
import { validIp } from '@/utils/validate'
import {
  connect_openstack,
  get_openstack_info,
  disconnect_openstack,
  get_openstack_image_lists,
  update_image_args
} from '@/api/openstack'
import { Message } from 'element-ui'

export default {
  name: 'OpenstackTable',
  data() {
    const validateIP = (rule, value, callback) => {
      if (!validIp(value)) {
        callback(new Error('请输入正确的IP地址'))
      } else {
        callback()
      }
    }
    return {
      // 总数据
      tableData: [],
      // 默认显示第几页
      currentPage: 1,
      // 总条数，根据接口获取数据长度(注意：这里不能为空)
      totalCount: 1,
      // 个数选择器（可修改）
      pageSizes: [5, 10, 15, 20],
      // 默认每页显示的条数（可修改）
      PageSize: 10,
      openstack_connection_Visible: false,
      openstack_data_table: [],
      search: '',
      openstack_connection_form: {
        auth_ip: '',
        user: {
          value: '',
          type: ''
        },
        password: '',
        domain: {
          value: '',
          type: ''
        }
      },
      Openstack_Info_Value: '',
      Openstack_Info: [],
      tabIndex: '',
      openstack_connection_rules: {
        auth_ip: [{ required: true, trigger: 'blur', validator: validateIP }]
      },
      loading: false,
      random_key: ''
    }
  },
  // computed: {
  //   // 模糊搜索
  //   tables() {
  //     const search = this.search
  //     if (search) {
  //       // filter() 方法创建一个新的数组，新数组中的元素是通过检查指定数组中符合条件的所有元素。
  //       // 注意： filter() 不会对空数组进行检测。
  //       // 注意： filter() 不会改变原始数组。
  //       return this.Openstack_Info.filter(data => {
  //         return Object.keys(data).some(key => {
  //           // indexOf() 返回某个指定的字符在某个字符串中首次出现的位置，如果没有找到就返回-1；
  //           // 该方法对大小写敏感！所以之前需要toLowerCase()方法将所有查询到内容变为小写。
  //           if (typeof data[key] === 'string') {
  //             console.log(String(data[key]).toLowerCase().includes(search))
  //             return String(data[key]).toLowerCase().includes(search)
  //           //   return false
  //           // } else {
  //           //   return true
  //           }
  //
  //           // return data.Image_Info[key]['status'].includes(search)
  //           // return Object.keys(data.Image_Info[key]).some(item => {
  //           //   if (typeof data.Image_Info[key][item] === 'string' && data.Image_Info[key][item].length > 0) {
  //           //     console.log(String(data.Image_Info[key][item]).includes(search))
  //           //     return data.Image_Info[key][item].includes(search)
  //           //   }
  //           //   // return String(data.Image_Info[key][item]||'').toLowerCase().indexOf(search) > -1
  //           // })
  //         })
  //       })
  //     }
  //   }
  // },
  created() {
    this.openstack_info()
  },
  methods: {
    current_change: function(val) {
      this.currentPage = val
    },
    size_change(val) {
      // 改变每页显示的条数
      this.PageSize = val
      // 注意：在改变每页显示的条数时，要将页码显示到第一页
      this.currentPage = 1
    },
    convertSize(row, column) {
      const res = parseInt(row.size)
      if (res > 2 ** 30) {
        return (res / 2 ** 30).toFixed(2) + ' GB'
      } else {
        return (res / 2 ** 20).toFixed(2) + 'MB'
      }
    },
    convertStr(row, column) {
      return row[column.property].toString()
    },
    openstack_connection_submit(targetName) {
      this.$refs.openstack_connection_form.validate(valid => {
        if (valid) {
          this.$confirm('确认提交？').then(_ => {
            connect_openstack(this.openstack_connection_form).then(res => {
              if (res.data.length < 1) {
                Message({
                  message: res.message,
                  type: 'danger',
                  duration: 5 * 1000
                })
              } else {
                this.$set(this.Openstack_Info, this.Openstack_Info.length, res.data)
                this.get_image_lists(this.Openstack_Info[this.Openstack_Info.length - 1]['id_md5']).then(data => {
                  this.$set(this.Openstack_Info[this.Openstack_Info.length - 1], 'Image_Info', data.images)
                  this.Openstack_Info_Value = this.Openstack_Info[this.Openstack_Info.length - 1]['id_md5']
                  this.tabIndex = this.Openstack_Info.length - 1
                  this.totalCount = data.images.length
                  this.currentPage = 1
                }).catch(_ => {
                  console.log(this.Openstack_Info)
                })
                this.openstack_connection_Visible = false
              }
            }).catch(_ => {
              this.openstack_connection_Visible = false
            })
          })
        } else {
          console.log('错误提交！！')
          return false
        }
      })
    },
    clickTab(tab, event) {
      this.currentPage = 1
      this.totalCount = this.Openstack_Info[tab.index].Image_Info.length
      this.tabIndex = tab.index
      console.log(tab.index)
    },
    removeTab(targetName) {
      const tabs = this.Openstack_Info
      const activeName = this.Openstack_Info_Value
      let flag = true
      let nextTab = []
      if (activeName === targetName) {
        this.$confirm('确定删除！').then(_ => {
          tabs.forEach((tab, index) => {
            if (tab.id_md5 === targetName) {
              nextTab = tabs[index + 1] || tabs[index - 1]
              this.tabIndex = tabs[index + 1] ? index + 1 : index - 1
            }
          })
          if (nextTab && flag) {
            flag = false
            this.Openstack_Info_Value = nextTab.id_md5
            this.totalCount = nextTab.Image_Info.length
            this.currentPage = 1
            this.Openstack_Info = tabs.filter(t => t.id_md5 !== targetName)
          }
          disconnect_openstack({ 'id_md5': targetName }).then(res => {
          })
          // this.Openstack_Info_Value = activeName
          // this.Openstack_Info = tabs.filter(tab => tab.id_md5 !== targetName)
        })
      }
    },
    filterSelect(value, row, column) {
      return row[column.property].toString() === value
    },
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
    openstack_info() {
      get_openstack_info().then(res => {
        this.total = res.data.length
        if (res.data.length < 1) {
          Message(res.message)
        } else {
          for (let i = 0, len = res.data.length; i < len; i++) {
            this.Openstack_Info.push(res.data[i])
            this.get_image_lists(this.Openstack_Info[i]['id_md5']).then(data => {
              /**
               * 注意，修改一个初始化时，不存在的对象里的属性时，不能使用
               * this.Openstack_Info[i]['Image_Info'] = data.images
               * 因为在页面初始化渲染后，该属性不存在，导致第一次修改时不会渲染，导致修改不可见
               * 只有再次修改时才会在页面显示
               */
              this.$set(this.Openstack_Info[i], 'Image_Info', data.images)
              if (i === this.currentPage - 1) {
                this.totalCount = data.images.length
              }
            })
            // this.$refs.Image_Table.get_image_lists(this.Openstack_Info[i]['id_md5'])
          }
          this.Openstack_Info_Value = this.Openstack_Info[0]['id_md5']
          this.tabIndex = this.Openstack_Info_Value
        }
      })
    },
    get_image_lists(id_md5) {
      return new Promise((resolve, reject) => {
        get_openstack_image_lists(id_md5).then(res => {
          resolve(res.data)
        }).catch(error => {
          reject(error)
        })
      })
    },
    update_image(index, image_index, id, param) {
      update_image_args(id, param).then(res => {
        this.$set(this.Openstack_Info[image_index].Image_Info[(this.currentPage - 1) * this.PageSize + index], 'os_hidden', res.data.images[0].os_hidden)
      })
    }
  }
}
</script>

<style scoped lang="scss">
.detail-table-expand {
  &-el-form-item {
    width: 180px;
    display: block;
  }
}

.image-detail-item {
  min-width: 45%;
}
</style>

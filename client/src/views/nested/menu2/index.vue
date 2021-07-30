<template>
  <div>
    <el-form size="mini" :model="searchData" class="searchBox">
      <el-row :gutter="24">
        <el-col :xs="24" :sm="24" :md="12" :lg="6" :xl="4">
          <el-form-item label="skuId" class="textArea">
            <el-input
              v-model="searchData.skuIds"
              type="textarea"
              autosize
              placeholder="请输入"
            />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="24" :md="12" :lg="6" :xl="4">
          <el-form-item label="sku编码" class="textArea">
            <el-input
              v-model="searchData.skuCodes"
              type="textarea"
              autosize
              placeholder="请输入"
            />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="24" :md="12" :lg="6" :xl="4">
          <el-form-item label="sku名称(中文)">
            <el-input v-model="searchData.skuNameCn" placeholder="请输入" />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="24" :md="12" :lg="6" :xl="4">
          <el-form-item label="Sku名称(英文)">
            <el-input v-model="searchData.skuNameEn" placeholder="请输入" />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="24" :md="12" :lg="6" :xl="4">
          <el-form-item label="颜色(中文)">
            <diy-select
              v-model="searchData.colorCns"
              :itemlist="colorCnsList"
              :is-need-search="true"
              :single="false"
              :all="true"
              label="name"
              value="name"
            />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="24" :md="12" :lg="6" :xl="4">
          <el-form-item label="颜色(英文)">
            <diy-select
              v-model="searchData.colorEns"
              :itemlist="colorEnsList"
              :is-need-search="true"
              :single="false"
              :all="true"
              label="name"
              value="name"
            />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="24" :md="12" :lg="6" :xl="4">
          <el-form-item label="颜色(本地)">
            <diy-select
              v-model="searchData.colorLocals"
              :itemlist="colorLocalsList"
              :is-need-search="true"
              :single="false"
              :all="true"
              label="name"
              value="name"
            />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="24" :md="12" :lg="6" :xl="4">
          <el-form-item label="运营商id" class="textArea">
            <el-input
              v-model="searchData.carrierIds"
              type="textarea"
              autosize
              placeholder="请输入"
            />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="24" :md="12" :lg="6" :xl="4">
          <el-form-item label="运营商编码" class="textArea">
            <el-input
              v-model="searchData.carrierCodes"
              type="textarea"
              autosize
              placeholder="请输入"
            />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="24" :md="12" :lg="6" :xl="4">
          <el-form-item label="运营商名称(中文)">
            <diy-select
              v-model="searchData.carrierNameCns"
              :itemlist="carrierNameCnsList"
              :is-need-search="true"
              :single="false"
              :all="true"
              label="name"
              value="name"
            />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="24" :md="12" :lg="6" :xl="4">
          <el-form-item label="运营商名称(英文)">
            <diy-select
              v-model="searchData.carrierNameEns"
              :itemlist="carrierNameEnsList"
              :is-need-search="true"
              :single="false"
              :all="true"
              label="name"
              value="name"
            />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="24" :md="12" :lg="6" :xl="4">
          <el-form-item label="归一化国家地区id" class="textArea">
            <el-input
              v-model="searchData.normalizationIds"
              type="textarea"
              autosize
              placeholder="请输入"
            />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="24" :md="12" :lg="6" :xl="4">
          <el-form-item label="归一化国家地区编码" class="textArea">
            <el-input
              v-model="searchData.normalizationCodes"
              type="textarea"
              autosize
              placeholder="请输入"
            />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="24" :md="12" :lg="6" :xl="4">
          <el-form-item label="认证机型名">
            <diy-select
              v-model="searchData.certifiedModels"
              :itemlist="certifiedModelsList"
              :is-need-search="true"
              :single="false"
              :all="true"
              label="name"
              value="name"
            />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="24" :md="12" :lg="6" :xl="4">
          <el-form-item label="创建时间">
            <el-date-picker
              v-model="searchData.createDate"
              type="daterange"
              range-separator="~"
              start-placeholder="开始时间"
              end-placeholder="结束时间"
              :picker-options="pickerOptions"
              :unlink-panels="true"
              value-format="yyyy-MM-dd"
            />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="24" :md="12" :lg="6" :xl="4">
          <el-form-item label="更新时间">
            <el-date-picker
              v-model="searchData.updateDate"
              type="daterange"
              range-separator="~"
              start-placeholder="开始时间"
              end-placeholder="结束时间"
              :picker-options="pickerOptions"
              :unlink-panels="true"
              value-format="yyyy-MM-dd"
            />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="24" :md="12" :lg="6" :xl="4">
          <el-form-item>
            <el-button type="primary" @click="getTableData('init')">查询</el-button>
            <el-button @click="reset">重置</el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <el-table
      v-loading="loading"
      row-key="skuId"
      size="mini"
      class="tableBox"
      :data="tableList"
      style="width:100%;"
      border
      :header-cell-style="{ background: '#fafafa' }"
      :expand-row-keys="expands"
    >
      <el-table-column type="expand" width="1">
        <template slot-scope="scopeOut">
          <el-table
            v-show="scopeOut.row.countryShow"
            ref="countryArea"
            :data="scopeOut.row.nations"
            border
            size="mini"
            row-key="id"
            :expand-row-keys="expandsInner"
            :header-cell-style="{ background: '#fafafa' }"
          >
            <el-table-column type="expand" width="1">
              <template slot-scope="scopeInner">
                <el-table
                  v-show="scopeInner.row.lifeShow"
                  :data="scopeInner.row.lifecycles"
                  border
                  size="mini"
                  :header-cell-style="{ background: '#fafafa' }"
                >
                  <el-table-column
                    type="index"
                    label="序号"
                    width="50"
                    header-align="center"
                    align="center"
                    :show-overflow-tooltip="true"
                  />
                  <el-table-column
                    prop="extendAttributeId"
                    label="id"
                    :show-overflow-tooltip="true"
                  />
                  <el-table-column prop="orderNumber" label="顺序" :show-overflow-tooltip="true" />
                  <el-table-column
                    prop="lifecycleCode"
                    label="生命周期编码"
                    :show-overflow-tooltip="true"
                  />
                  <el-table-column
                    prop="lifecycleNameCn"
                    label="生命周期中文名"
                    :show-overflow-tooltip="true"
                  />
                  <el-table-column
                    prop="lifecycleTime"
                    label="生命周期时间"
                    :show-overflow-tooltip="true"
                  />
                  <el-table-column prop="skuLifecycleStatus" label="生命周期状态">
                    <template slot-scope="scopes">
                      <el-tag v-if="scopes.row.skuLifecycleStatus === 0" type="danger">失效</el-tag>
                      <el-tag v-if="scopes.row.skuLifecycleStatus === 1" type="info">有效</el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column
                    prop="lifecycleCreateTime"
                    label="创建时间"
                    :show-overflow-tooltip="true"
                  />
                  <el-table-column
                    prop="lifecycleUpdateTime"
                    label="更新时间"
                    :show-overflow-tooltip="true"
                  />
                </el-table>
              </template>
            </el-table-column>
            <el-table-column
              type="index"
              label="序号"
              width="50"
              header-align="center"
              align="center"
              :show-overflow-tooltip="true"
            />
            <el-table-column prop="id" label="id" :show-overflow-tooltip="true" />
            <el-table-column prop="nationId" label="国家地区id" :show-overflow-tooltip="true" />
            <el-table-column
              prop="nationTwoAbbr"
              label="国家地区二位码"
              :show-overflow-tooltip="true"
            />
            <el-table-column
              prop="nationNameCn"
              label="国家地区中文名"
              :show-overflow-tooltip="true"
            />
            <el-table-column
              prop="nationNameEn"
              label="国家地区英文名"
              :show-overflow-tooltip="true"
            />
            <el-table-column prop="nationCreateTime" label="创建时间" :show-overflow-tooltip="true" />
            <el-table-column prop="nationUpdateTime" label="更新时间" :show-overflow-tooltip="true" />
            <el-table-column label="其他" :show-overflow-tooltip="true">
              <template slot-scope="scopeInner">
                <span
                  style="color:#09F;cursor: pointer;"
                  @click="expandTable(scopeInner.row)"
                >生命周期</span>
              </template>
            </el-table-column>
          </el-table>
          <el-table
            v-show="scopeOut.row.extenShow"
            :data="scopeOut.row.extendAttributes"
            row-key="id"
            border
            size="mini"
            :header-cell-style="{ background: '#fafafa' }"
          >
            <el-table-column
              type="index"
              label="序号"
              width="50"
              header-align="center"
              align="center"
              :show-overflow-tooltip="true"
            />
            <el-table-column prop="extendAttributeId" label="id" :show-overflow-tooltip="true" />
            <el-table-column prop="attrCode" label="扩展属性编码" :show-overflow-tooltip="true" />
            <el-table-column
              prop="attrNameCn"
              label="扩展属性名(中文)"
              :show-overflow-tooltip="true"
            />
            <el-table-column
              prop="attrNameEn"
              label="扩展属性名(英文)"
              :show-overflow-tooltip="true"
            />
            <el-table-column
              prop="attrValueCn"
              label="扩展属性值(中文)"
              :show-overflow-tooltip="true"
            />
            <el-table-column
              prop="attrValueEn"
              label="扩展属性值(英文)"
              :show-overflow-tooltip="true"
            />
            <el-table-column
              prop="attrValueLocal"
              label="扩展属性值(本地)"
              :show-overflow-tooltip="true"
            />
            <el-table-column prop="valueDataType" label="数据类型">
              <template slot-scope="scopes">
                <el-tag v-if="scopes.row.valueDataType === 1" size="mini">字符串</el-tag>
                <el-tag
                  v-if="scopes.row.valueDataType === 2"
                  type="info"
                  size="mini"
                >带单位实数等</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="valueUnit" label="单位" :show-overflow-tooltip="true" />
            <el-table-column prop="createTime" label="创建时间" :show-overflow-tooltip="true" />
            <el-table-column prop="updateTime" label="更新时间" :show-overflow-tooltip="true" />
          </el-table>
        </template>
      </el-table-column>
      <el-table-column
        type="index"
        label="序号"
        width="50"
        header-align="center"
        align="center"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column
        property="skuId"
        label="skuId"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column
        property="skuCode"
        label="sku编码"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column
        property="skuNameCn"
        label="sku名称(中文)"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column
        property="skuNameEn"
        label="sku名称(英文)"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column
        property="flowStatus"
        label="流程状态"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column
        property="spuId"
        label="关联spuId"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column
        property="salesSkuId"
        label="关联营销skuId"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column
        property="statisticsSkuId"
        label="关联统计机型id"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column
        property="colorCn"
        label="颜色(中文)"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column
        property="colorEn"
        label="颜色(英文)"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column
        property="colorLocal"
        label="颜色(本地)"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column
        property="carrierId"
        label="运营商id"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column
        property="carrierCode"
        label="运营商编码"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column
        property="carrierNameCn"
        label="运营商名称(中文)"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column
        property="carrierNameEn"
        label="运营商名称(英文)"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column
        property="normalizationId"
        label="归一化国家/地区id"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column
        property="normalizationCode"
        label="归一化国家/地区编码"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column
        property="normalizationNameCn"
        label="归一化国家/地区名称(中文)"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column
        property="certifiedModel"
        label="认证机型名"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column
        property="projectCode"
        label="研发项目编码"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column
        property="projectName"
        label="研发项目名称"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column
        property="createTime"
        label="创建时间"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column
        property="updateTime"
        label="更新时间"
        :show-overflow-tooltip="true"
        :render-header="renderHeader"
      />
      <el-table-column label="其他" :show-overflow-tooltip="true" width="140">
        <template slot-scope="scopeOut">
          <span
            style="color:#09F;cursor: pointer;"
            @click="expandExTable(scopeOut.row)"
          >扩展属性</span>
          <span>|</span>
          <span
            style="color:#09F;cursor: pointer;"
            @click="expandCounTable(scopeOut.row)"
          >国家/地区</span>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      class="pagination"
      :current-page="pageNum"
      :page-sizes="[10, 20, 30, 50]"
      :page-size="pageSize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
</template>
<script>
// import Crypto from '@/utils/crypto.js'
// import diySelect from '@/components/Select/diySelect.vue'

export default {
  data() {
    return {
      searchData: {},
      tableList: [],
      pageNum: 1,
      pageSize: 10,
      total: 0,
      loading: false,
      secretKey: '',
      pickerOptions: {
        shortcuts: [
          {
            text: '最近一周',
            onClick(picker) {
              const end = new Date()
              const start = new Date()
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '最近一个月',
            onClick(picker) {
              const end = new Date()
              const start = new Date()
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '最近三个月',
            onClick(picker) {
              const end = new Date()
              const start = new Date()
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '最近六个月',
            onClick(picker) {
              const end = new Date()
              const start = new Date()
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 180)
              picker.$emit('pick', [start, end])
            }
          }
        ]
      },
      dataList: [],
      expands: [],
      expandsCoun: [],
      lifeShow: false,
      countryShow: false,
      expandsInner: [], // 生命周期展开数组
      counFlag: true,
      colorCnsList: [],
      colorEnsList: [],
      colorLocalsList: [],
      carrierNameCnsList: [],
      carrierNameEnsList: [],
      certifiedModelsList: []
    }
  },
  created() {
    this.getTableData('init')
    this.getSkuItem()
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
    expandTable(row) {
      row.lifeShow = !row.lifeShow
      if (row.lifeShow) {
        this.expandsInner.push(row.id)
      } else {
        this.expandsInner = this.expandsInner.filter(item => item !== row.id)
      }
      console.log(this.expandsInner, '生命周期')
    },
    expandCounTable(row) {
      row.countryShow = !row.countryShow
      if (row.countryShow) {
        this.expands.push(row.skuId)
      } else {
        this.expands = this.expands.filter(item => item !== row.skuId)
      }
      row.extenShow = false
      console.log(this.expands, '国家/地区')
    },
    expandExTable(row) {
      row.extenShow = !row.extenShow
      if (row.extenShow) {
        this.expands.push(row.skuId)
      } else {
        this.expands = this.expands.filter(item => item !== row.skuId)
      }
      row.countryShow = false
      console.log(this.expands, '扩展属性')
    },
    reset() {
      this.searchData = {}
      this.getTableData('init')
    },
    getTableData(init) {
      this.expandsInner = []
      this.expands = []
      let creatObj = {}
      if (this.searchData.createDate !== undefined && this.searchData.createDate !== null) {
        creatObj = {
          startCreateTime: this.searchData.createDate[0],
          endCreateTime: this.searchData.createDate[1]
        }
      } else {
        delete this.searchData.createDate
        creatObj = {}
      }
      let updateObj = {}
      if (this.searchData.updateDate !== undefined && this.searchData.updateDate !== null) {
        updateObj = {
          startUpdateTime: this.searchData.updateDate[0],
          endUpdateTime: this.searchData.updateDate[1]
        }
      } else {
        delete this.searchData.updateDate
        updateObj = {}
      }
      const obj = {
        skuIds: this.searchData.skuIds ? this.searchData.skuIds.split(/[(\r\n)\r\n]+/) : [],
        skuCodes: this.searchData.skuCodes ? this.searchData.skuCodes.split(/[(\r\n)\r\n]+/) : [],
        carrierIds: this.searchData.carrierIds
          ? this.searchData.carrierIds.split(/[(\r\n)\r\n]+/)
          : [],
        carrierCodes: this.searchData.carrierCodes
          ? this.searchData.carrierCodes.split(/[(\r\n)\r\n]+/)
          : [],
        normalizationIds: this.searchData.normalizationIds
          ? this.searchData.normalizationIds.split(/[(\r\n)\r\n]+/)
          : [],
        normalizationCodes: this.searchData.normalizationCodes
          ? this.searchData.normalizationCodes.split(/[(\r\n)\r\n]+/)
          : [],
        skuNameCn: this.searchData.skuNameCn,
        skuNameEn: this.searchData.skuNameEn,
        colorCns: this.searchData.colorCns,
        colorEns: this.searchData.colorEns,
        colorLocals: this.searchData.colorLocals,
        carrierNameCns: this.searchData.carrierNameCns,
        carrierNameEns: this.searchData.carrierNameEns,
        certifiedModels: this.searchData.certifiedModels,
        ...updateObj,
        ...creatObj
      }
      if (init) {
        this.pageNum = 1
        this.pageSize = 10
      }
      this.loading = true
      const param = {
        pageNum: this.pageNum,
        pageSize: this.pageSize,
        ...obj
      }
      this.$api.productTree.skuList({ ...param }).then(res => {
        if (res.data) {
          this.tableList = res.data.content
          this.tableList.forEach(item => {
            this.$set(item, 'countryShow', false)
            this.$set(item, 'extenShow', false)
          })
          this.total = res.data.total
        }
        this.loading = false
      })
    },
    handleCurrentChange(page) {
      this.pageNum = page
      this.getTableData()
    },
    handleSizeChange(pageSize) {
      this.pageSize = pageSize
      this.getTableData()
    },
    getSkuItem() {
      this.$api.productTree.skuItem().then(res => {
        if (res.data) {
          this.colorCnsList = []
          this.colorEnsList = []
          this.colorLocalsList = []
          this.carrierNameCnsList = []
          this.carrierNameEnsList = []
          this.certifiedModelsList = []
          for (const key in res.data) {
            const itemArr = []
            res.data[key].forEach(item => {
              const obj = {
                name: item
              }
              itemArr.push(obj)
            })
            if (key === 'colorCns') {
              this.colorCnsList = itemArr
            } else if (key === 'colorEns') {
              this.colorEnsList = itemArr
            } else if (key === 'colorLocals') {
              this.colorLocalsList = itemArr
            } else if (key === 'carrierNameCns') {
              this.carrierNameCnsList = itemArr
            } else if (key === 'carrierNameEns') {
              this.carrierNameEnsList = itemArr
            } else if (key === 'certifiedModels') {
              this.certifiedModelsList = itemArr
            }
          }
        }
      })
    }
  }
}
</script>
<style lang="scss" scoped>
.mainContent {
  margin: 20px;
}
.form-content {
  font-weight: 600;
}
.pagination {
  float: right;
  margin-top: 10px;
}
.import {
  margin: 0 0 20px 0;
}
.el-dialog .el-dialog__body {
  padding-top: 0 !important;
}
.el-form-item {
  margin-bottom: 15px !important;
}
.el-select,
.el-cascader,
.el-date-editor.el-input {
  width: 100%;
}
.searchBox >>> .el-form-item {
  display: flex;
  width: 100%;
  height: 30px;
  .el-form-item__label {
    white-space: nowrap;
  }
  .el-range-editor--mini.el-input__inner {
    height: 30px;
  }
  .el-form-item__content {
    flex: 1;
    .el-date-editor--daterange.el-input,
    .el-date-editor--daterange.el-input__inner,
    .el-date-editor--timerange.el-input,
    .el-date-editor--timerange.el-input__inner {
      width: 100% !important;
    }
  }
}
.tableBox >>> .el-table__expand-icon:after {
  content: '';
}
.tableBox >>> .el-table__expand-icon > i {
  display: none;
}
.tableBox >>> .el-table__expand-column {
  border-right: none;
}
</style>

<template>
  <div class="app-container">
    <el-table
      :data="(Historys_info || []).slice((currentPage - 1) * PageSize, currentPage * PageSize)"
      style="width: 100%;margin-top: 10px"
      row-key="id"
      border
      default-expand-all
      :default-sort="{prop: 'id', order: 'descending'}"
      @sort-change="sortChange"
    >
      <el-table-column
        label="id"
        prop="id"
        sortable="custom"
        width="40px"
      />
      <el-table-column
        label="checksum"
        prop="checksum"
      />
      <el-table-column
        label="镜像名"
        prop="image_name"
        sortable
      />
      <el-table-column
        label="openstack IP"
      >

        <template slot-scope="scope">
          <el-dropdown v-for="(value, key) in scope.row.openstacks" :key="key" size="mini" placement="top">
            <el-tag size="small" type="warning">{{ key }}</el-tag>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item :key="value">{{ value==='None'?key:value }}</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </template>
      </el-table-column>
      <el-table-column
        label="status"
        width="90px"
      >
        <template slot-scope="scope">
          <el-tag v-if="scope.row.status === '成功'" type="success">{{ scope.row.status }}</el-tag>
          <el-tag v-else type="danger">{{ scope.row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="开始时间"
        prop="start_time"
        sortable
      />
      <el-table-column
        label="结束时间"
        prop="end_time"
        sortable
      />
      <el-table-column
        label="action"
      >
        <template slot-scope="scope">
          <el-tag v-for="act in scope.row.action.split(';')" :key="act" size="small" type="info">{{ act }}</el-tag>
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

<script>
import { get_host_history_info } from '@/api/connection'
export default {
  name: 'History',
  data() {
    return {
      Historys_info: [],
      // 总数据
      tableData: [],
      // 默认显示第几页
      currentPage: 1,
      // 总条数，根据接口获取数据长度(注意：这里不能为空)
      totalCount: 1,
      // 个数选择器（可修改）
      pageSizes: [5, 10, 15, 20],
      // 默认每页显示的条数（可修改）
      PageSize: 5,
      tabIndex: ''
    }
  },
  created() {
    this.Historys()
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
    sortChange(v) {
      if (v.column.order === 'ascending') {
        // 通过属性showWeights进行排序
        if (v.column.property === 'id') {
          this.Historys_info.sort(this.sortList('id'))
        }
      } else if (v.column.order === 'descending') {
        if (v.column.property === 'id') {
          this.Historys_info.sort(this.sortListDesc('id'))
        }
      }
    },
    sortList(property) {
      return function(a, b) {
        const value1 = parseInt(a[property])
        const value2 = parseInt(b[property])
        return value1 - value2
      }
    },
    sortListDesc(property) {
      return function(a, b) {
        const value1 = parseInt(a[property])
        const value2 = parseInt(b[property])
        return value2 - value1
      }
    },
    Historys() {
      get_host_history_info().then(res => {
        this.Historys_info = res.data
        this.totalCount = res.data.length
        this.currentPage = 1
      })
    }
  }
}
</script>

<style scoped>
.app-container{
  width: 95%;
  margin: 20px 2.5%;
}
.line{
  text-align: center;
}
.el-tag {
    margin: 5px;
}
</style>


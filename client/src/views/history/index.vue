<template>
  <div class="app-container">
    <el-table
      :data="Historys_info"
      style="width: 100%;margin-top: 10px"
      row-key="id"
      border
      default-expand-all
      :default-sort="{prop: 'id', order: 'ascending'}"
    >
      <el-table-column
        label="id"
        prop="id"
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
  </div>
</template>

<script>
import { get_host_history_info } from '@/api/connection'
export default {
  name: 'History',
  data() {
    return {
      Historys_info: []
    }
  },
  created() {
    this.Historys()
  },
  methods: {
    Historys() {
      get_host_history_info().then(res => {
        this.Historys_info = res.data
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


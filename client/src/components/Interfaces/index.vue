<template>
  <div v-show="instance_info_show">
    <div v-for="(item,index) in Interfaces_info" :key="index">
      <el-card class="box-card" style="margin-bottom: 10px">
        <div v-if="item.state===1" slot="header" class="clearfix">
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
            <el-col :span="10">mac地址</el-col>
            <el-col :span="14">{{ item.mac }}</el-col>
          </el-row>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { get_host_interfaces_info } from '@/api/connection'
import { getVirt_connect_token } from '@/utils/virt-info'

export default {
  name: 'InterfacesInfo',
  data() {
    return {
      instance_info_show: true,
      Interfaces_info: []
    }
  },
  created() {
    // this.interface()
  },
  methods: {
    interface() {
      get_host_interfaces_info({ 'token': getVirt_connect_token() }).then(res => {
        this.Interfaces_info = res.data || []
      })
    }
  }
}
</script>

<style scoped>

</style>

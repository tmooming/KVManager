<template>
  <el-table
    :data="Image_Info"
    stripe
    style="width: 80%;margin-left: 10%;margin-top: 20px"
    :default-sort="{prop: 'owner', order: 'descending'}"
  >
    <el-table-column
      prop="owner"
      label="所有者"
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
      prop="type"
      label="类型"
    >
      Image
    </el-table-column>
    <el-table-column
      prop="status"
      label="状态"
    />
    <el-table-column
      prop="visibility"
      label="可见性"
    />
    <el-table-column
      prop="protected"
      label="受保护的"
    />
    <el-table-column
      prop="disk_format"
      label="磁盘格式"
    />
    <el-table-column
      prop="size"
      label="大小"
    />
  </el-table>
</template>

<script>
import { get_openstack_image_lists } from '@/api/openstack'

export default {
  name: 'ImageLists',
  data() {
    return {
      Image_Info: []
    }
  },
  methods: {
    get_image_lists(id_md5) {
      console.log(id_md5)
      get_openstack_image_lists(id_md5).then(res => {
        this.Image_Info = res.data
      }).catch(_ => {
      })
      // return new Promise((resolve, reject) => {
      //   get_openstack_image_lists(id_md5).then(res => {
      //     resolve(res.data)
      //   }).catch(error => {
      //     reject(error)
      //   })
      // })
    }
  }
}
</script>

<style scoped>

</style>

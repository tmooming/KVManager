<template>
  <div id="app">
    <keep-alive include="el-tabel">
      <router-view />
    </keep-alive>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

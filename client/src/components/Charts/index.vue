<template>
  <div ref="main" style="width: 700px;height: 500px;border:1px solid rgb(180,180,180)" />
</template>

<script>
import * as echarts from 'echarts'
// import ECharts from 'vue-echarts'
// import 'echarts/lib/chart/pie'
export default {
  name: 'CpuChart',

  // 在echarts_option中写东西就行了，官方文档直接下这里就可以自己玩了
  data() {
    return {
      echarts1_option: {
        // 主体代码块
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          data: [820, 932, 901, 934, 1290, 1330, 1320],
          type: 'line',
          areaStyle: {}
        }]
      }
    }
  },
  // 挂载前初始化echarts实例
  mounted: function() {
  // 基于准备好的dom，初始化echarts实例
    const myChart = echarts.init(this.$refs.main)
    // 绘制图表，this.echarts1_option是数据
    myChart.setOption(this.echarts1_option)
  }
}
</script>

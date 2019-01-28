<template>
  <v-chart :options="polar"/>
</template>

<script>
import ECharts from 'vue-echarts'
import 'echarts/lib/chart/bar'
import 'echarts/lib/component/polar'
import { get } from "../http";

export default {
  name: 'ChartDashboard',
  components: {
    'v-chart': ECharts
  },
  data () {
    let data = []

    // for (let i = 0; i <= 5; i++) {
    //     data.push(i)
    // }
    console.log(data)
    return {
      // polar: {
      //   title: {
      //     text: '极坐标双数值轴'
      //   },
      //   legend: {
      //     data: ['line']
      //   },
      //   tooltip: {
      //   },
      //   xAxis: {
      //     data: ['0', '1', '2', '3', '4', '5']
      //   },
      //   yAxis: {},
      //   series: [
      //     {
      //       // coordinateSystem: 'polar',
      //       name: 'line',
      //       type: 'line',
      //       showSymbol: false,
      //       data: data
      //     }
      //   ],
      //   animationDuration: 2000
      // }
      polar: {},
    }
  },
  mounted() {
    this.getChartObj()
  },
  methods: {
    getChartObj() {
      get('http://127.0.0.1:8000/api/v1/mzitu/charts/test/').then(
      response => {
          console.log(response.data);
          this.polar = response.data
      }
    )
    }
  }
}
</script>

<style scoped>
.echarts {
  width: 100%;
  height: 500px;
}
</style>

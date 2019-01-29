<template>
  <div class="charts">
    <div id="barTags" ref="barTags"></div>
    <div id="barProxyIp" ref="barProxyIp"></div>
  </div>
</template>

<script>
import echarts from "echarts";
import { get } from "../http";
import { CHART } from "../http/api";

export default {
  name: "ChartDashboard",
  data() {
    return {
      barTagsOptions: {},
      barProxyIpOptions: {}
    };
  },
  mounted() {
    this.setBarTags();
    this.setBarProxyIp();
  },
  methods: {
    setBarTags() {
      let obj = {};
      get(CHART().TagsBar).then(response => {
        obj = response.data;
        this.barTagsOptions = {
          visualMap: [
            {
              type: "continuous",
              orient: "horizontal",
              dimension: 0,
              min: 0,
              max: obj.maxCount,
              top: 0,
              right: 0
            }
          ],
          title: {
            text: obj.title
          },
          legend: {
            data: ["tags"]
          },
          grid: {
            left: "15%"
          },
          xAxis: {
            type: "value",
            position: "top",
            show: false
          },
          yAxis: {
            type: "category",
            data: obj.axisLabel,
            axisLabel: {
              textStyle: {
                // fontSize: "12"
              },
              // interval: 3,
              rotate: 0
            },
            axisLine: { show: false },
            axisTick: [
              {
                //坐标轴小标记
                show: false
              }
            ]
          },
          dataZoom: [
            {
              type: "slider",
              yAxisIndex: 0,
              start: 50,
              end: 100,
              filterMode: "empty"
            },
            {
              type: "inside",
              yAxisIndex: 0,
              start: 50,
              end: 100
            }
          ],
          series: [
            {
              name: "bar",
              type: "bar",
              itemStyle: {
                normal: {
                  label: {
                    show: true,
                    position: "inside",
                    textStyle: {
                      color: "#fff"
                      // fontSize: "12"
                    }
                  }
                }
              },
              // showSymbol: false,
              data: obj.data
            }
          ],
          animationDuration: 1500
        };
        this.barTags = echarts.init(document.getElementById("barTags"));
        this.barTags.setOption(this.barTagsOptions);
      });
    },
    setBarProxyIp() {
      let obj = {};
      get(CHART().ProxyIpsBar).then(response => {
        obj = response.data;
        this.barProxyIpOptions = {
          visualMap: [
            {
              type: "continuous",
              dimension: 1,
              min: 0,
              max: obj.maxCount,
              // inRange: {
              //   // 明暗度的范围是 0 到 1
              //   colorLightness: [1, 0]
              // }
            }
          ],
          title: {
            text: obj.title
          },
          legend: {
            data: ["proxyips"]
          },
          grid: {
            left: "15%"
          },
          xAxis: {
            type: "category",
            name: "Score"
          },
          yAxis: {
            type: "value",
            name: "数量"
          },
          dataZoom: [
            {
              show: true,
              type: "slider",
              xAxisIndex: 0,
              start: 70,
              end: 100,
              filterMode: "empty"
            }
          ],
          series: [
            {
              name: "scatter",
              type: "scatter",
              symbolSize: function(val) {
                return Math.log10(val[1]) * 100;
              },
              itemStyle: {
                normal: {
                  label: {
                    show: true,
                    position: "inside",
                    textStyle: {
                      color: "#fff"
                    }
                  }
                }
              },
              // showSymbol: false,
              data: obj.data
            }
          ],
          animationDuration: 1500
        };
        this.barProxyIp = echarts.init(document.getElementById("barProxyIp"));
        this.barProxyIp.setOption(this.barProxyIpOptions);
      });
    }
  }
};
</script>

<style scoped>
/* todo: 用网格来决定大小 */
#barProxyIp,
#barTags {
  width: 100%;
  height: 500px;
}
</style>

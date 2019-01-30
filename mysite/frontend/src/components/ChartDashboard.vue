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
    setBarTags() {  // 设置Tags柱状图
      let obj = {};
      get(CHART().TagsBar).then(response => {
        obj = response.data;
        this.barTagsOptions = {
          // 视觉设置
          visualMap: [
            {
              type: "continuous",  // 连续型
              orient: "horizontal",  // 水平显示样例
              dimension: 0,  // 用series.data第一列数据
              min: 0,  // 最小值
              max: obj.maxCount,  // 最大值
              top: 0,  // 相对位置，这个设置会出现在右上角，可以用百分比
              right: 0
            }
          ],
          title: {
            text: obj.title
          },
          // 图例，多个数据集的时候有用
          legend: {
            data: ["tags"]
          },
          // ？
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
          // 滚动条和缩放
          dataZoom: [
            {
              type: "slider",  // 滚动和缩放条
              yAxisIndex: 0,
              start: 50,  // 初始化百分比位置
              end: 100,
              filterMode: "empty"  // 不按照数据自动缩放
            },
            {
              type: "inside",  // 可用鼠标拖动图表
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
          animationDuration: 1500  // 1.5s的动画过渡
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

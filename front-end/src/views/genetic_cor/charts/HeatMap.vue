<template>
  <div :class="className" :style="{width:width}" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
// import resize from './mixins/resize'

export default {
  // mixins: [resize],
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    chartData: {
      type: Array,
      required: true
    },
    xData: {
      type: Array,
      required: true
    },
    yData: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      chart: null
    }
  },
  watch: {
    chartData: {
      deep: true,
      handler(val) {
        this.setOptions(val)
        this.chart.resize({ height: this.autoHeight })
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart()
    })
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$el, 'macarons')
      var seriesData = this.chartData
      this.chart.resize({
        height: 600
      })
      this.setOptions(seriesData, this.xData, this.yData)
    },
    setOptions(seriesData, xData, yData) {
      this.chart.setOption({
        title: {
          text: 'HeatMap',
          subtext: 'HeatMap',
          textStyle: {
            fontSize: 32
          },
          left: '40%'
        },
        grid: {
          top: '10%',
          left: '30%',
          right: '10%',
          bottom: '40%'
        },
        tooltip: {
          trigger: 'item',
          axisPointer: {
            type: 'shadow'
          },
          formatter: function(params) {
            var value = params.value
            var source = value[0]
            var target = value[1]
            var status = value[2]
            return [source + ' Vs ' +
                target, 'rg:' + status
            ].join('<br/>')
          }
        },
        toolbox: {
          show: true,
          feature: {
            dataZoom: {
              yAxisIndex: 'none'
            },
            dataView: { readOnly: false },
            restore: {},
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          data: xData,
          axisLabel: {
            interval: 0,
            rotate: 60,
            formatter: function(value) {
              if (value.length > 35) {
                return value.substring(0, 35) + '...'
              } else {
                return value
              }
            }
          },
          axisTick: {
            show: false
          },
          axisLine: {
            show: false
          }
        },
        yAxis: {
          type: 'category',
          data: yData,
          axisLabel: {
            interval: 0,
            rotate: 0,
            formatter: function(value) {
              if (value.length > 35) {
                return value.substring(0, 35) + '...'
              } else {
                return value
              }
            }
          },
          axisTick: {
            show: false
          }
        },
        series: {
          type: 'heatmap',
          data: seriesData,
          itemStyle: {
            emphasis: {
              shadowBlur: 10
            },
            borderWidth: 1,
            borderColor: '#fff'
          }
        },
        visualMap: {
          min: -1,
          max: 1,
          calculable: true,
          right: '5%',
          color: ['#bf444c', 'white', 'green'],
          top: 'center'
        }
      })
    }

  }
}

</script>

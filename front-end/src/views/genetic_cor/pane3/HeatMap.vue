<template>
  <div :class="className" :style="{width:width}" />
</template>

<script>
// import echarts from 'echarts'
import * as echarts from 'echarts';
require('echarts/theme/macarons') // echarts theme
// import resize from './mixins/resize'

export default {
  // mixins: [resize],
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    rgModel:{
      type:String,
      default : ''
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
          text: 'HeatMap' + " (" + this.rgModel.toUpperCase() + ")",
          subtext: this.className,
          textStyle: {
            fontSize: 26
          },
          subtextStyle:{
            fontSize: 18
          },
          left: '50%'
        },
        grid: {
          top: '12%',
          left: '30%',
          bottom: '40%'
        },
        tooltip: {
          trigger: 'item',
          axisPointer: {
            type: 'shadow'
          },
                      backgroundColor: "rgba(255,255,255,0.8)",
            color: "black",
            borderWidth: "1", //边框宽度设置1
            borderColor: "gray", //设置边框颜色
            textStyle: {
              color: "black" //设置文字颜色
            },
          formatter: function(params) {
            var value = params.value
            var source = value[0]
            var target = value[1]
            var status = value[2]
            var pvalue = value[3]
            return [source + ' Vs ' +
                target, 'rg: ' + status,
                'pvalue: ' + pvalue
            ].join('<br/>')
          }
        },
        toolbox: {
          show: true,
          feature: {
            dataZoom: {
              yAxisIndex: 'none'
            },
            restore: {},
            saveAsImage: {pixelRatio:2}
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
          label: {
            show:true,
            formatter: function(data) {
              if (data.value[3]){
                if (data.value[3]<0.001){
                  return  "**"
                }else if (data.value[3]<0.05){
                  return "*"
                }
                else{
                  return ""
                }
              }else{
                return ""
              }
            }
          },
          itemStyle: {
            emphasis: {
              shadowBlur: 10
            },
            borderWidth: 1,
            borderColor: '#fff'
          }
        },
        visualMap: {
          min: -1.0,
          max: 1.0,
          calculable: true,
          precision:1,
          right: '5%',
          color: ['#fa6d1d', 'white', '#0780cf'],
          top: 'center'
        }
      })
    }

  }
}

</script>

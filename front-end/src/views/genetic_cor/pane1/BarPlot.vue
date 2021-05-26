<template>
  <div :class="className" :style="{width:width}" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme

export default {
  // mixins: [resize],
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    subName: {
      type: String,
      default: 'Genetic Correlation'
    },
    width: {
      type: String,
      default: '100%'
    },
    chartData: {
      type: Array,
      required: true
    },
    colData: {
      type: Array,
      required: true
    },
    errorData: {
      type: Array,
      required: true
    },
    pvalData: {
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
        this.setOptions(val, this.pvalData)
        if (val.length > 10) {
          this.autoHeight = val.length * 25 + 50
          this.chart.resize({ height: this.autoHeight })
        } else {
          this.chart.resize({ height: 350 })
        }
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
      var barData = this.chartData
      var pData = this.pvalData
      this.chart.resize({ height: 350 })
      this.setOptions(barData, pData)
    },
    renderItem(params, api) {
      var highPoint = api.coord([api.value(1), api.value(0)])
      var lowPoint = api.coord([api.value(2), api.value(0)])
      var halfWidth = api.size([1, 0])[1] * 0.2
      var style = api.style({
        stroke: api.visual('color'),
        fill: null
      })
      return {
        type: 'group',
        children: [{
          type: 'line',
          shape: {
            x1: highPoint[0],
            y1: highPoint[1] - halfWidth,
            x2: highPoint[0],
            y2: highPoint[1] + halfWidth
          },
          style: style
        }, {
          type: 'line',
          shape: {
            x1: highPoint[0],
            y1: highPoint[1],
            x2: lowPoint[0],
            y2: lowPoint[1]
          },
          style: style
        }, {
          type: 'line',
          shape: {
            x1: lowPoint[0],
            y1: lowPoint[1] - halfWidth,
            x2: lowPoint[0],
            y2: lowPoint[1] + halfWidth
          },
          style: style
        }
        ]
      }
    },
    setOptions(bardata, pdata) {
      this.chart.setOption({
        title: {
          text: this.className,
          subtext: this.subName,
          textStyle: {
            fontSize: 26
          },
          subtextStyle:{
            fontSize: 18
          },
          left: '35%'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: { // 坐标轴指示器，坐标轴触发有效
            type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
          }
        },
        toolbox: {
          show: true,
          feature: {
            dataView: { readOnly: false },
            saveAsImage: {pixelRatio:2}
          }
        },
        grid: {
          top: 80,
          bottom: 30,
          left: '30%'
        },
        /* dataZoom: [{
            type: 'slider',
            start: 0,
            yAxisIndex:[0],
            end: 20
          }, {
            type: 'inside',
            start: 0,
            yAxisIndex:[0],
            end: 20
          }],*/
        visualMap: [/* {
            dimension:1,
            seriesIndex:1,
            pieces: [{
                gt: 0,
                // color: 'rgb(119,168,173)'
                color: 'rgb(157,221,157)'
            }, {
                lt: 0,
                color: 'rgb(194,85,82)'
            }]
        }*/
          {
            show: false,
            dimension: 0,
            seriesIndex: 0,
            pieces: [{
              gt: 0,
              // color: 'rgb(119,168,173)'
              color: 'rgb(157,221,157)'
            }, {
              lt: 0,
              color: 'rgb(194,85,82)'
            }]
          }
        ],
        xAxis: {},
        yAxis: {
          type: 'category',
          data: this.colData,
          axisLabel: {
            fontSize: 14,
            interval: 0,
            formatter: function(value) {
              if (value.length > 35) {
                return value.substring(0, 35) + '...'
              } else {
                return value
              }
            }
          }
        },
        series: [{
          type: 'bar',
          stack: '总量',
          data: bardata

          /* label:{
                color: 'blue',
                show:true,
                formatter:function(value){
                  var val = pdata[value.dataIndex]
                  if (val){
                    if (val <0.0001){
                      return '***'
                    } else if (val <0.001){
                      return '**'
                    } else if (val <0.05){
                      return '*'
                    } else{
                      return ''
                    }
                  }else{
                    return ''
                  }
                }
            }*/
        },
        {
          type: 'custom',
          name: 'error',
          itemStyle: {
            normal: {
              borderWidth: 1.5
              // color:'black'
            }
          },
          encode: {
            y: 0,
            x: [1, 2]
          },
          renderItem: this.renderItem,
          data: this.errorData,
          z: 10
        }
        ]
      })
    }
  }
}

</script>

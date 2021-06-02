<template>
  <div :class="className" :style="{width:width}" />
</template>

<script>
// import echarts from 'echarts'
import * as echarts from 'echarts';
import 'echarts/theme/fruit' // echarts theme
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
    nodes: {
      type: Array,
      required: true
    },
    links: {
      type: Array,
      required: true
    },
    categories: {
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
    nodes: {
      deep: true,
      handler(val) {
        this.chart.resize({ height: 500 })
        this.setOptions(val, this.links, this.categories)
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
      this.chart.resize({
        height: 800
      })
      this.setOptions(this.nodes, this.links, this.categories)
    },

    setOptions(nodes, links, categories) {
      this.chart.setOption({
        title: {
          text: 'Circular layout' + " (" + this.rgModel.toUpperCase() + ")",
          subtext: this.className,
          left: '20%',
          textStyle: {
            fontSize: 26
          },
          subtextStyle:{
            fontSize: 18
          },
        },
        grid: {
          top: '40%',
          bottom: '10%'
        },
        tooltip: {            backgroundColor: "rgba(255,255,255,0.8)",
            color: "black",
            borderWidth: "1", //边框宽度设置1
            borderColor: "gray", //设置边框颜色
            textStyle: {
              color: "black" //设置文字颜色
            },},
        legend: [{
          data: categories.map(function(a) {
            return a.name
          })
        }],
        toolbox: {
          show: true,
          feature: {
            dataView: { readOnly: false },
            saveAsImage: {pixelRatio:2}
          }
        },
        animationDurationUpdate: 1500,
        animationEasingUpdate: 'quinticInOut',
        series: [
          {
            name: 'Graph',
            type: 'graph',
            layout: 'circular',
            circular: {
              rotateLabel: true
            },
            data: nodes,
            links: links,
            categories: categories,
            roam: true,
            label: {
              show:true,
              position: 'inside',
              formatter: function(value) {
              if (value.name.length > 20) {
                return value.name.substring(0, 20) + '...'
              } else {
                return value.name
              }
            },
            },
            scaleLimit: {
                min: 0.4,
                max: 2
            },
            lineStyle: {
              color: 'source',
              curveness: 0.3
            },
            emphasis: {
              focus: 'adjacency',
                lineStyle: {
                    width: 5
                }
            }
          }
        ]
      })
    }

  }
}

</script>

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
        tooltip: {},
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
              rotateLabel: false
            },
            data: nodes,
            links: links,
            categories: categories,
            roam: true,
            label: {
              position: 'outside',
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
                    width: 10
                }
            }
          }
        ]
      })
    }

  }
}

</script>

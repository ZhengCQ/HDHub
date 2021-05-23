<template>
  <div :class="className" :style="{ width: width }" />
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
      width: {
        type: String,
        default: '100%'
      },
      chartData: {
        type: Array,
        required: true
      }
    },
    data() {
      return {
        chart: null,
        max_y: 0,
        max_x: 0,
        min_x: 0,
        min_y: 0,
        dimensions:[
            'name', 'HDL', 'LDSC', 'LDSC  min', 'LDSC max', 'HDL min', 'HDL max'
        ]
      }
    },
    watch: {
      chartData: {
        deep: true,
        handler(val) {
          this.setOptions(val)
            this.chart.resize({
              height: 550
            })
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
      get_axis_xy(data) {
        for (var i of data) {
          if (i[6] > this.max_y) {
            this.max_y = i[6].toFixed(1)
          }
          if (i[4] > this.max_x) {
            this.max_x = i[4].toFixed(1)
          }
          if (i[5] < this.min_y) {
            this.min_y = i[5].toFixed(1)
          }
          if (i[3] > this.mix_x) {
            this.mix_x = i[3].toFixed(1)
          }
        }
        if (this.max_y > this.max_x) {
          this.max_x = this.max_y
        } else {
          this.max_y = this.max_x
        }

        if (this.min_y < this.min_x) {
          this.min_x = this.min_y
        } else {
          this.min_y = this.min_x
        }
      },
      initChart() {
        this.chart = echarts.init(this.$el, 'macarons')
        var barData = this.chartData
        this.chart.resize({
          height: 550
        })
        this.setOptions(barData)
        
      },
      renderItem(params, api) {
        var children = [];
        var coordDims = ['x', 'y'];

        for (var baseDimIdx = 0; baseDimIdx < 2; baseDimIdx++) {
          var otherDimIdx = 1 - baseDimIdx;
          var encode = params.encode;
          var baseValue = api.value(encode[coordDims[baseDimIdx]][0]);
          var param = [];
          param[baseDimIdx] = baseValue;
          param[otherDimIdx] = api.value(encode[coordDims[otherDimIdx]][1]);
          var highPoint = api.coord(param);
          param[otherDimIdx] = api.value(encode[coordDims[otherDimIdx]][2]);
          var lowPoint = api.coord(param);
          var halfWidth = 5;

          var style = api.style({
            stroke: api.visual('color'),
            fill: null
          });

          children.push({
            type: 'line',
            transition: ['shape'],
            shape: makeShape(
              baseDimIdx,
              highPoint[baseDimIdx] - halfWidth, highPoint[otherDimIdx],
              highPoint[baseDimIdx] + halfWidth, highPoint[otherDimIdx]
            ),
            style: style
          }, {
            type: 'line',
            transition: ['shape'],
            shape: makeShape(
              baseDimIdx,
              highPoint[baseDimIdx], highPoint[otherDimIdx],
              lowPoint[baseDimIdx], lowPoint[otherDimIdx]
            ),
            style: style
          }, {
            type: 'line',
            transition: ['shape'],
            shape: makeShape(
              baseDimIdx,
              lowPoint[baseDimIdx] - halfWidth, lowPoint[otherDimIdx],
              lowPoint[baseDimIdx] + halfWidth, lowPoint[otherDimIdx]
            ),
            style: style
          });
        }

        function makeShape(baseDimIdx, base1, value1, base2, value2) {
          var shape = {};
          shape[coordDims[baseDimIdx] + '1'] = base1;
          shape[coordDims[1 - baseDimIdx] + '1'] = value1;
          shape[coordDims[baseDimIdx] + '2'] = base2;
          shape[coordDims[1 - baseDimIdx] + '2'] = value2;
          return shape;
        }

        return {
          type: 'group',
          children: children
        };
      },
      setOptions(data) {
        this.get_axis_xy(data),
        this.chart.setOption({
          title: {
            text: this.className,
            subtext: 'Genetic Correlation(HDL vs LDSC)',
            left: '40%'
          },
          tooltip: {},
          toolbox: {
          show: true,
          feature: {
            dataView: { readOnly: true },
            saveAsImage: {}
          }
        },
          grid: {
            bottom: 80
          },
          xAxis: {
            name: 'LDSC',
            min: this.min_x,
            max: this.max_x,
            axisLine: { onZero: false }
          },
          yAxis: {
            name: 'HDL',
            min:this.min_y,
            max: this.max_y,
            axisLine: { onZero: false }
          },
          series: [{
              type: 'scatter',
              name: 'genetic Correlation',
              data: data,
              dimensions: this.dimensions,
        encode: {
            x: 2,
            y: 1,
            tooltip: [2, 1, 3, 4, 5, 6],
            itemName: 0
        },
        symbolSize:15,
        itemStyle: {
            color: '#77bef7'
        }
            }, {
              type: 'custom',
              name: 'genetic Correlation',
              renderItem: this.renderItem,
              dimensions: this.dimensions,
              encode: {
                x: [2, 3, 4],
                y: [1, 5, 6],
                tooltip: [2, 1, 3, 4, 5, 6],
                itemName: 0
              },
              data: data,
              z: 100
            },
            {
              name: '对角线',
              type: 'line',
              data: [this.min_y, this.max_y]
            }
          ]
        })
      }
    }
  }

</script>

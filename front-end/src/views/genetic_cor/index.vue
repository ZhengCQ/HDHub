<template>
  <div class="container">
    <div style="padding-top:70px">
      <div style="text-align: center;">
        <h3>HDL Hub</h3>
        <h4>Using high-definition likelihood (HDL), we estimated the heritability of traits based on the genome-wide
          association summary statistics, and calculated their paired genetic correlation </h4>
      </div>
      <div>
        <el-form ref="form" label-width="100px" :model="form" style="padding-top:60px;" class="summit-form">
          <el-form-item label="Traits">
            <el-select
              v-model="form.traits"
              filterable
              multiple
              remote
              :remote-method="queryTraits"
              placeholder="Search and Select Trait"
            >
              <el-option v-for="(item) in gene_options" :key="item.index" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item align="center">
            <el-button type="primary" style="width:45%;margin-bottom:30px;" @click="queryTraitsDetail">Get Detail
            </el-button>
          </el-form-item>
        </el-form>
      </div>
      <!-- GWAS性状筛选 开始-->
      <div v-if="traitsDetailData" align="center">
        <el-table
          ref="traitstab"
          :data="traitsDetailData"
          border
          fit
          highlight-current-row
          style="width: 100%;"
          align="center"
          @selection-change="handleSelectionChange1"
        >
          <el-table-column type="selection" width="55" />
          <el-table-column
            v-for="item in tableTraitKey"
            :key="item.name"
            :label="item.label"
            :prop="item.prop"
            :width="item.width"
            :align="item.align || 'center'"
          >

            <!--template slot="header" slot-scope="scope">

              <el-popover :ref="item.name" placement="top" width="200" trigger="click">
                <el-form :model="summaryForm">
                  <el-form-item :label="item.name">
                    <el-input v-model="summaryForm[item.name]" autocomplete="off"></el-input>
                  </el-form-item>
                </el-form>

                <div>
                  <el-button @click="cancelInput(item.name)">清除</el-button>
                  <el-button @click="cancelInput(item.name)">确定</el-button>
                </div>

                <span slot="reference">{{item.name}} <i class="el-icon-search" slot="reference"></i></span>
              </el-popover>

            </template-->

            <template slot-scope="scope">
              <span>{{ scope.row[item.name] }}</span>
            </template>
          </el-table-column>

          <slot />
        </el-table>
        <!--表格 结束-->
        <div style="margin-top: 20px">
          <el-button @click="getTables();">Explore</el-button>
        </div>
      </div>
      <!-- GWAS性状筛选 结束-->

      <!-- 详细traits数据 开始-->
      <!--设置弹框 开始-->
      <el-dialog title="Reset" :visible.sync="formVis_fig1a">

        <el-form :model="fig1aform">

          <el-form-item label="Correlation(positive)">

            <div style="width:80%;padding-left:25%;">
              <el-slider v-model="fig1aform.p_cor" :min="0" :max="3" range :step="0.1">></el-slider>
              <el-input-number v-model="fig1aform.p_cor[0]" :min="0" :max="3" :step="0.1" placeholder="Min" />
              <el-input-number v-model="fig1aform.p_cor[1]" :min="0" :max="3" :step="0.1" placeholder="Max" />
            </div>
          </el-form-item>

          <el-form-item label="Correlation(negative)">
            <div style="width:80%;padding-left:25%;">
              <el-slider v-model="fig1aform.n_cor" :min="-3" :max="0" range :step="0.1">></el-slider>
              <el-input-number v-model="fig1aform.n_cor[0]" :min="-3" :max="0" :step="0.1" placeholder="Min" />
              <el-input-number v-model="fig1aform.n_cor[1]" :min="-3" :max="0" :step="0.1" placeholder="Max" />
            </div>
          </el-form-item>

          <el-form-item label="Pvalue" prop="p_cutoff">
            <div style="padding-left:25%;">
              <el-input-number v-model="fig1aform.p_cutoff" :min="0" :max="1" :step="0.01" placeholder="Max" />
            </div>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="formVis_fig1a = false">取 消</el-button>
          <el-button type="primary" @click="formVis_fig1a = false;getTables()">确 定</el-button>
        </div>
      </el-dialog>
      <!--设置弹框 结束-->

      <!--tabs 开始-->
      <el-tabs v-if="tableData.length>0" v-model="activeName" type="card">
        <!--数据设置 开始-->
        <el-row>
          <el-col style="background: #eee; padding: 10px 0px 10px 30px; width:14%">
            <div class="grid-content bg-purple-dark">
              <i class="el-icon-setting el-icon--left" @click="formVis_fig1a = true">数据设置</i>
              <!--i class="el-icon-download" @click="downloadPic">图片下载</i-->
            </div>
          </el-col>
        </el-row>
        <!--数据设置 结束-->
        <!--总表格-->
        <el-tab-pane label="Table" name="first">
          <!--表格下载 开始-->
          <BookTypeOption v-model="bookType" />
          <el-button
            :loading="downloadLoading"
            style="margin:0 0 20px 20px;"
            type="primary"
            icon="el-icon-document"
            @click="handleDownload()"
          >Export Table</el-button>
          <!--表格下载 结束-->
          <div>
            <!--表格 开始-->
            <el-table
              ref="traitsTablelst"
              :data="tableData"
              border
              fit
              highlight-current-row
              style="width: 100%;"
              align="center"
              :row-key="getRowKeys"
              @selection-change="handleSelectionChange2"
            >
              <el-table-column type="selection" :reserve-selection="true" width="55" />
              <el-table-column
                v-for="item in tableKey"
                :key="item.name"
                :label="item.label"
                :prop="item.prop"
                :width="item.width"
                :align="item.align || 'center'"
              >
                <template slot-scope="scope">
                  <span>{{ scope.row[item.name] }}</span>
                </template>
              </el-table-column>
              <el-table-column label="Operation" width="100" align="center">
                <template slot-scope="scope">
                  <el-button size="small" type="primary" @click="checkDetail(scope.$index, scope.row)">Detail
                  </el-button>
                </template>
              </el-table-column>
              <slot />
            </el-table>
            <!--表格 结束-->
            <!--页码 开始-->

            <pagination
              v-show="total_items > 0"
              :total="total_items"
              :page.sync="listQuery.page"
              :limit.sync="listQuery.page_size"
              @pagination="getTables()"
            />
            <!--页码 结束-->

          </div>
        </el-tab-pane>
        <!---柱状图-->
        <el-tab-pane label="Bar Plot" name="second">

          <div v-show="'second' === activeName" align="center">
            <!--画图 开始-->
            <el-row style="background: #fff; padding: 0px 0px 0px 0px; width:100%">
              <div align="center" />
              <bar-plot
                :class-name="form.trait1"
                :chart-data="barPlotData"
                :col-data="columnsData"
                :pval-data="barPlotDataPval"
                :error-data="barPlotDataSe"
              />
            </el-row>
            <!--画图 结束-->
            <!--p style="margin-top:10px;align=left">The Detail Results Tables Show As:</p-->
          </div>
        </el-tab-pane>
        <!---select traits table-->
        <el-tab-pane label="select Traits Table" name="five">
          <el-button @click="getCyclePairsTables()">Get Pairs for Target</el-button>
          <el-button @click="getCluster()">Pairs2Cluster</el-button>
          </br>
          <!--表格下载 开始-->
          <BookTypeOption v-model="bookType" />
          <el-button
            :loading="downloadLoading"
            style="margin:0 0 20px 20px;"
            type="primary"
            icon="el-icon-document"
            @click="handleDownload()"
          >Export Table</el-button>
          <!--表格下载 结束-->
          <div>
            <!--表格 开始-->
            <el-table
              ref="traitsPairTable"
              :data="tableDataParis"
              border
              fit
              highlight-current-row
              style="width: 100%;"
              align="center"
            >
              </el-table-column>
              <el-table-column
                v-for="item in tableKey"
                :key="item.name"
                :label="item.label"
                :prop="item.prop"
                :width="item.width"
                :align="item.align || 'center'"
              >
                <template slot-scope="scope">
                  <span>{{ scope.row[item.name] }}</span>
                </template>
              </el-table-column>
              <el-table-column label="Operation" width="100" align="center">
                <template slot-scope="scope">
                  <el-button size="small" type="primary" @click="checkDetail(scope.$index, scope.row)">Detail
                  </el-button>
                </template>
              </el-table-column>
              <slot />
            </el-table>
            <!--表格 结束-->
            <!--页码 开始-->

            <pagination
              v-show="total_items2 > 0"
              :total="total_items2"
              :page.sync="listQuery.page"
              :limit.sync="listQuery.page_size"
              @pagination="getCyclePairsTables()"
            />
            <!--页码 结束-->

          </div>
        </el-tab-pane>

        <!---热图-->

        <el-tab-pane label="Heatmap" name="third">
          <el-button @click="clusterHeatmap()">RUN Cluster</el-button>
          <div align="center">
            <!--画图 开始-->
            <el-row v-show="heatMapData.length>0" style="background: #fff; padding: 0px 0px 0px 0px; width:100%">
              <heat-map
                :class-name="this.form.trait1"
                :chart-data="heatMapData"
                :x-data="colHeatMapData"
                :y-data="colHeatMapData"
              />
            </el-row>
            <!--画图 结束-->

            <div v-show="netNodes.length>0" align="center">
            <!--画图 开始-->
            <el-row style="background: #fff; padding: 0px 0px 0px 0px; width:100%">
              <net-graph
                :class-name="this.form.trait1"
                :nodes="netNodes"
                :links="netLinks"
                :categories="netCategories"
              />
            </el-row>
            <!--画图 结束-->
          </div>

          </div>
        </el-tab-pane>
        <!--关系图-->
        <el-tab-pane label="Network" name="fourth">
          <el-button @click="clusterNetwork()">RUN Network</el-button>
          <div v-show="netNodes.length>0" align="center">
            <!--画图 开始-->
            <el-row style="background: #fff; padding: 0px 0px 0px 0px; width:100%">
              <net-graph
                :class-name="this.form.trait1"
                :nodes="netNodes"
                :links="netLinks"
                :categories="netCategories"
              />
            </el-row>
            <!--画图 结束-->
            <!--p style="margin-top:10px;align=left">The Detail Results Tables Show As:</p-->
          </div>
        </el-tab-pane>

      </el-tabs>
      <!--tabs 结束-->
    </div>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import BarPlot from './charts/BarPlot'
import HeatMap from './charts/HeatMap'
import NetGraph from './charts/NetGraph'
import {
  queryInfo,
  queryInfoDetail,
  postPairCor,
  postCyclePairCor,
  getDetail,
  postNetwork,
  postCluster
} from '@/api/genetic_cor'
import BookTypeOption from '@/components/Base/BookTypeOption'
export default {
  components: {
    Pagination,
    BookTypeOption,
    BarPlot,
    HeatMap,
    NetGraph
  },
  data() {
    return {
      form: {
        traits: ''
      },
      activeName: 'first',
      fig1aform: {
        p_cor: [0.2, 1.2],
        n_cor: [-1.2, -0.2],
        p_cutoff: 0.05
      },
      summaryForm: {},
      formVis_fig1a: false,
      inputContent: '',
      visible: false,
      dialogVisible: false,
      traitsDetailData: '',
      multiSel: [],
      multiSel_traits: [],
      gene_options: [],
      tableData: [],
      tableDataParis: [],
      tableDataParis_allids: [],
      isTrait2: true,
      isPairs: true,
      downloadLoading: false,
      total_items: 0,
      total_items2: 0,
      listQuery: {
        page: 1,
        page_size: 10,
        sort: '+id'
      },
      barPlotData: [],
      columnsData: [],
      barPlotDataSe: [],
      barPlotDataPval: [],
      heatMapData: [],
      colHeatMapData: [],
      netLinks: [],
      netNodes: [],
      netCategories: [],
      bookType: 'xlsx',
      tableTraitKey: [{
        name: 'trait',
        label: 'Trait',
        prop: 'trait'
      },
      {
        name: 'filename',
        label: 'filename',
        prop: 'filename'
      },
      {
        name: 'ethnic',
        label: 'ethnic',
        prop: 'ethnic'
      },
      {
        name: 'sex',
        label: 'sex',
        prop: 'sex'
      },
      {
        name: 'sampel_size',
        label: 'sampel_size',
        prop: 'sampel_size'
      },
      {
        name: 'ncase',
        label: 'ncase',
        prop: 'ncase'
      },
      {
        name: 'ncontrol',
        label: 'ncontrol',
        prop: 'ncontrol'
      }
      ],
      tableKey: [{
        name: 'trait1',
        label: 'Trait1',
        prop: 'trait1'
      },
      {
        name: 'trait2',
        label: 'Trait2',
        prop: 'trait2'
      },
      {
        name: 'gwas1',
        label: 'gwas1',
        prop: 'gwas1'
      },
      {
        name: 'gwas2',
        label: 'gwas2',
        prop: 'gwas2'
      },
      {
        name: 'cov',
        label: 'Covariance',
        prop: 'cov'
      },
      {
        name: 'cov_se',
        label: 'Covariance_SE',
        prop: 'cov_se'
      },
      {
        name: 'cor',
        label: 'Corrlation',
        prop: 'cor'
      },
      {
        name: 'cor_se',
        label: 'Corrlation_SE',
        prop: 'cor_se'
      },
      {
        name: 'p',
        label: 'p',
        prop: 'p'
      }
      ],
      isdata: false
    }
  },
  watch: {
    activeName: function(val) {
      if (val === 'second') {
        this.getBarPic()
      }
    }
  },
  methods: {
    queryTraits(queryString, cb) {
      var list = []
      queryInfo({
        value: queryString
      })
        .then((res) => {
          var pheinfo = res.data
          for (const i in pheinfo) {
            list.push({
              value: pheinfo[i]
            })
          }
          // list = queryString ? list.filter(this.createFilter(queryString)) : list
          this.gene_options = list
        })
        .catch((error) => {
          console.log(error)
        })
    },
    reset_datainfo() {
      this.tableData = []
      this.multiSel_traits = []
      this.multiSel = []
      this.tableDataParis = []
      this.tableDataParis_allids = []
      this.traitsDetailData = []
      this.heatMapData = []
      this.nodes = []
      this.netNodes = []
    },
    queryTraitsDetail() {
      this.reset_datainfo()
      queryInfoDetail({
        value: this.form
      }).then((res) => {
        this.traitsDetailData = res.data
        // 默认选择
        this.$nextTick(function() {
          this.toggleSelection(this.traitsDetailData, 'traitstab')
        })
      })
    },
    toggleSelection(rows, reftab) {
      if (rows) {
        console.log(rows)
        rows.forEach((row) => {
          // 设置该表格选框选中
          if (reftab === 'traitstab') {
            this.$refs.traitstab.toggleRowSelection(row)
          } else if (reftab === 'traitsTablelst') {
            this.$refs.traitsTablelst.toggleRowSelection(row)
          }
        })
      } else {
        if (reftab === 'traitstab') {
          this.$refs.traitstab.clearSelection()
        } else if (reftab === 'traitsTablelst') {
          this.$refs.traitsTablelst.clearSelection()
        }
      }
    },
    cancelInput(id) {
      console.log(this.summaryForm)
      this.$refs[id][0].doClose()
    },
    handleSelectionChange1(val) {
      this.multiSel = val
    },
    handleSelectionChange2(val) {
      this.multiSel_traits = val
    },
    getRowKeys(row) {
      return row.id
    },
    renderHeaderOne(h, {
      column,
      $index
    }) {
      return h(
        'span', {
          class: 'table-head',
          style: {
            width: '100%',
            'text-align': 'center'
          }
        },
        [
          h('span', {}, column.label),
          h(
            'el-popover', {
              props: {
                placement: 'top-start',
                width: '200',
                trigger: 'click'
              }
            },
            [
              h(
                'i', {
                  slot: 'reference',
                  class: 'el-icon-search'
                },
                ''
              ),
              h('div', {}, [
                h(
                  'el-input', {
                    width: '300'
                  },
                  ''
                )
              ]),
              h(
                'div', {
                  style: 'text-align: right; margin: 0'
                },
                [
                  h(
                    'el-button', {
                      type: 'primary',
                      size: 'mini',
                      on: {
                        click: () => {
                          // 点击确认按钮的事件
                          alert('确定')
                          console.log()
                          console.log(`${column.label}   ${$index}`)
                        }
                      }
                    },
                    '确定'
                  ),
                  h('span', {}, '          '),
                  h(
                    'el-button', {
                      size: 'mini',
                      on: {
                        click: () => {
                          // 点击取消按钮的事件
                          alert('取消')
                          console.log(`${column.label}   ${$index}`)
                        }
                      }
                    },
                    '取消'
                  )
                ]
              )
            ]
          )
        ]
      )
    },
    getTables() {
      var tgt_tratis = []
      this.multiSel.forEach((val) => {
        tgt_tratis.push(val.filename)
      })
      postPairCor({
        value: tgt_tratis,
        query: this.listQuery,
        filter: this.fig1aform,
        activeName: this.activeName
      }).then((res) => {
        this.total_items = res.data._meta.total_items
        this.tableData = res.data.items
        this.getBarPic()
        this.$notify({
          title: 'Success',
          message: 'Success count the results',
          type: 'success',
          duration: 1000
        })
      })
    },
    getBarPic() {
      this.barPlotData = []
      this.columnsData = []
      this.barPlotDataSe = []
      this.barPlotDataPval = []

      var bar_table = (this.multiSel_traits.length > 0 ? this.multiSel_traits : this.tableData)
      var sorted_keys_array = Object.keys(bar_table).sort((a, b) => {
        return bar_table[b].cor - bar_table[a].cor
      })
      sorted_keys_array.forEach((v, idx) => {
        var val = bar_table[v]
        this.barPlotData.push(val.cor)
        this.columnsData.push(val.trait2)
        this.barPlotDataPval.push(val.p)
        this.barPlotDataSe.push([
          idx,
          val.cor - val.cor_se,
          val.cor + val.cor_se
        ])
      })
    },
    getCyclePairsTables() {
      var bar_table = (this.multiSel_traits.length > 0 ? this.multiSel_traits : this.tableData)
      var gwaslst = []
      gwaslst.push(bar_table[0].gwas1_id)
      for (var i of bar_table) {
        gwaslst.push(i.gwas2_id)
      }
      postCyclePairCor({
        value: gwaslst,
        query: this.listQuery,
        filter: this.fig1aform
      }).then((res) => {
        this.total_items2 = res.data._meta.total_items
        this.tableDataParis = res.data.items
        this.tableDataParis_allids = res.qy_ids
      })
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map((v) =>
        filterVal.map((j) => {
          if (j === 'timestamp') {
            // return parseTime(v[j])

          } else {
            return v[j]
          }
        })
      )
    },
    getDate() {
      const myDate = new Date()
      // 获取当前年
      const year = myDate.getFullYear()
      // 获取当前月
      const month = myDate.getMonth() + 1
      // 获取当前日
      const date = myDate.getDate()
      // 获取当前小时数(0-23)
      const h = myDate.getHours()
      // 获取当前分钟数(0-59)
      const m = myDate.getMinutes()
      const s = myDate.getSeconds()

      // 获取当前时间
      const time =
          year +
          '-' +
          this.convert(month) +
          '-' +
          this.convert(date) +
          '-' +
          this.convert(h) +
          '-' +
          this.convert(m) +
          '-' +
          this.convert(s)
      return time
    },
    convert(val) {
      return val < 10 ? '0' + val : val
    },

    downloadPic() {
      const mycanvas = document.getElementsByTagName('canvas')[0]
      const image = mycanvas.toDataURL('image/png')
      const $a = document.createElement('a')
      $a.setAttribute('href', image)
      $a.setAttribute(
        'download',
        this.form.traits[0].replace(/ /g, '_') + '_genetic_cor.png'
      )
      $a.click()
    },
    async handleDownload(dataType) {
      var data = this.tableData
      // var theader = Object.keys(data[0]);
      var theader = [
        'trait1',
        'trait2',
        'gwas1',
        'gwas2',
        'cov',
        'cov_se',
        'cor',
        'cor_se',
        'p'
      ]
      import('@/vendor/Export2Excel').then((excel) => {
        const filterVal = theader
        data = this.formatJson(filterVal, data)
        excel.export_json_to_excel({
          header: theader,
          data,
          filename: 'Genetic_corrlelation_' + this.getDate(),
          autoWidth: this.autoWidth,
          bookType: this.bookType
        })
        // this.downloadLoading = false;
      })
    },
    getCluster() {
      postCluster({
        value: this.tableDataParis_allids,
        filter: this.fig1aform
      }).then((res) => {
        console.log(res)
      })
    },
    clusterHeatmap() {
      var gwaslst = []
      var bar_table = (this.multiSel_traits.length > 0 ? this.multiSel_traits : this.tableData)
      gwaslst.push(bar_table[0].gwas1_id)
      for (var i of bar_table) {
        gwaslst.push(i.gwas2_id)
      }
      postCluster({
        value: gwaslst,
        // value: this.tableDataParis_allids,
        filter: this.fig1aform
      }).then((res) => {
        this.heatMapData = res.heatmap.data
        this.colHeatMapData = res.heatmap.col
        
        this.netLinks = res.network.links
        this.netNodes = res.network.nodes
        this.netCategories = [{
          name: '类别0'
        }]

        
        this.$notify({
          title: 'Success',
          message: 'Success count the results',
          type: 'success',
          duration: 1000
        })
      })
    },

    clusterNetwork() {
      var gwaslst = []
      gwaslst.push(this.tableData[0].gwas1)
      for (var i of this.tableData) {
        gwaslst.push(i.gwas2)
      }
      postNetwork({
        value: gwaslst,
        filter: this.fig1aform
      }).then((res) => {
        this.netLinks = res.links
        this.netNodes = res.nodes
        this.netCategories = [{
          name: '类别0'
        }]
      })
    }
  }
}

</script>
<style lang="scss" scoped>
  .el-select {
    position: relative;
    font-size: 14px;
    display: inline-block;
    width: 100%;
  }

  .summit-form {
    position: relative;
    width: 640px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }

  #tool-panel {
    position: absolute;
    top: 0;
    right: 0;
    left: 0;
    padding-top: 5px;
    padding-left: 15px;
  }

  #tool-panel .left-panel {
    float: left;
  }

</style>

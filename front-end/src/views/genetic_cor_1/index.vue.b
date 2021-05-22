<template>
  <div class="container">
    <div style="padding-top:70px;">
      <div style="text-align: center;">
        <h3>HDL Hub</h3>
        <h4>Using high-definition likelihood (HDL), we estimated the heritability of traits based on the genome-wide
          association summary statistics, and calculated their paired genetic correlation </h4>
      </div>
      <div>
        <el-form ref="form" label-width="100px" :model="form" style="padding-top:60px;" class="summit-form">
          <el-form-item label="Trait1">
            <el-select v-model="form.trait1" filterable remote :remote-method="queryTraits"
              placeholder="Search and Select Trait">
              <el-option v-for="(item,index) in gene_options" :key="item.index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item v-show="isTrait2" label="Trait2">
            <el-select v-model="form.trait2" filterable multiple remote :remote-method="queryTraits"
              placeholder="Search and Select Trait">
              <el-option v-for="(item,index) in gene_options" :key="item.index" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>

        <el-form-item label="Pvalue" prop="p_cutoff">
          <el-input-number
            v-model="form.p_cutoff" 
            :min="0" 
            :max="1"
            :step="0.01"
            placeholder="Max"
            >
          </el-input-number>
        </el-form-item>

        <el-form-item label="Correlation" prop="cor_cutoff">
          <el-input-number
            v-model="form.cor_min" 
            :min="-3" 
            :max="3"
            :step="0.1"
            placeholder="Min"
            >
          </el-input-number>
         <el-input-number
            v-model="form.cor_max" 
            :min="-3" 
            :max="3"
            :step="0.1"
            placeholder="Max"
            >
          </el-input-number>
        </el-form-item>
          <el-form-item align="center">
            <el-button type="primary" style="width:45%;margin-bottom:30px;" @click="onSubmit">Submit</el-button>
            <el-button v-if="isTrait2" type="primary" style="width:45%;margin-bottom:30px;" @click="ToSingle">ToSingle
            </el-button>
            <el-button v-else type="primary" style="width:45%;margin-bottom:30px;" @click="ToPairs">ToPairs</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div v-if="tableData" align="center">
         <!--画图 开始-->

          <el-row style="background: #fff; padding: 0px 0px 0px 0px; width:100%">
          <div align="center">
           <i class="el-icon-download" @click="downloadPic"></i>
         </div>
            <bar-plot
              :className="this.form.trait1"
              :chart-data="barPlotData"
              :col-data="columnsData"
              :pval-data="barPlotDataPval"
              :error-data="barPlotDataSe"
            />

          </el-row>
          <!--画图 结束-->
        <!--p style="margin-top:10px;align=left">The Detail Results Tables Show As:</p-->

        <!--页码 开始-->
        <pagination v-show="total_items>0" :total="total_items" :page.sync="listQuery.page"
          :limit.sync="listQuery.page_size" @pagination="onSubmit()" />
        <!--页码 结束-->

        <!--表格 开始-->
        <el-table :data="tableData" border fit highlight-current-row style="width: 100%;" align='center'>
          <el-table-column v-for="item in tableKey" :key="item.name" :label="item.label" :prop="item.prop"
            :width="item.width" :align="item.align || 'center'">
            <template slot-scope="scope">
              <span>{{ scope.row[item.name] }}</span>
            </template>
          </el-table-column>
            <el-table-column label="Operation" width="100" align="center">
        <template slot-scope="scope">
          <el-button size="small"  type="primary" @click="checkDetail(scope.$index, scope.row)">Detail</el-button>
        </template>
      </el-table-column>
          <slot> </slot>

        </el-table>
        <!--表格 结束-->

        <!--表格下载 开始-->
        <BookTypeOption v-model="bookType" />
        <el-button :loading="downloadLoading" style="margin:0 0 20px 20px;" type="primary" icon="el-icon-document"
          @click="handleDownload()">Export Table</el-button>
         <!--表格下载 结束-->
      </div>
    </div>
  </div>
</template>

<script>
  import Pagination from "@/components/Pagination";
  import BarPlot from "./charts/BarPlot";
  import {
    queryInfo,
    postPairCor,
    getDetail
  } from "@/api/genetic_cor";
  import BookTypeOption from "@/components/Base/BookTypeOption";
  export default {
    components: {
      Pagination,
      BookTypeOption,
      BarPlot
    },
    data() {
      return {
        form: {
          'cor_max':undefined,
          'cor_min':undefined,
          'p_cutoff':undefined,
          'trait1':'',
          'trait2':''
        },
        gene_options: [],
        tableData: '',
        isTrait2: true,
        isPairs: true,
        downloadLoading: false,
        total_items: 0,
        listQuery: {
          page: 1,
          page_size: 10,
          sort: "+id",
        },
       barPlotData: [],
       columnsData: [],
       barPlotDataSe: [],
       barPlotDataPval: [],
        bookType: "xlsx",
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
      };
    },
    methods: {
      ToSingle() {
        this.isTrait2 = false
        this.form.trait2 = ''
      },
      ToPairs() {
        this.isTrait2 = true
      },
      queryTraits(queryString, cb) {
        var list = [];
        queryInfo({
            'value': queryString
          }).then(res => {
            var pheinfo = res.data;
            for (const i in pheinfo) {
              list.push({
                value: pheinfo[i]
              });
            }
            // list = queryString ? list.filter(this.createFilter(queryString)) : list
            this.gene_options = list
          })
          .catch(error => {
            console.log(error);
          });
      },
      onSubmit() {
        // this.listQuery.page_size = 10
        this.barPlotData = []
        this.columnsData = []
        this.barPlotDataSe = []
        this.barPlotDataPval = []
        postPairCor({
          value: this.form,
          query: this.listQuery
        }).then(res => {
          this.total_items = res.data._meta.total_items
          this.tableData = res.data.items;
          res.data.items.forEach((val,idx) => {
            this.barPlotData.push(val.cor)
            this.columnsData.push(val.trait2)
            this.barPlotDataPval.push(val.p)
            this.barPlotDataSe.push([idx, val.cor - val.cor_se, val.cor + val.cor_se])
          });
          this.$notify({
            title: "Success",
            message: "Success count the results",
            type: "success",
            duration: 1000
          });
        });
      },
    formatJson(filterVal, jsonData) {
      return jsonData.map((v) =>
        filterVal.map((j) => {
          if (j === "timestamp") {
            return parseTime(v[j]);
          } else {
            return v[j];
          }
        })
      );
    },
    getDate() {
      const myDate = new Date()
      //获取当前年
      const year = myDate.getFullYear()
      //获取当前月
      const month = myDate.getMonth() + 1
      //获取当前日
      const date = myDate.getDate()
      //获取当前小时数(0-23)
      const h = myDate.getHours()
      //获取当前分钟数(0-59)
      const m = myDate.getMinutes()
      const s = myDate.getSeconds()

      //获取当前时间
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

   async checkDetail(index,row){
     var info = await getDetail(row.id)

   },
   downloadPic(){
    let mycanvas=document.getElementsByTagName('canvas')[0]
    let image=mycanvas.toDataURL("image/png");
    let $a = document.createElement('a');
    $a.setAttribute("href", image);
    $a.setAttribute("download", this.form.trait1.replace(/ /g,'_') + "_genetic_cor.png");
    $a.click();
   },
    async handleDownload(dataType) {
      // this.downloadLoading = true;
      this.listQuery.page = 1
      this.listQuery.page_size = 30
      var info = await postPairCor({
          value: this.form,
          query: this.listQuery
        });
      var data = info['data']['items'];
      // var theader = Object.keys(data[0]);
      var theader = ['trait1','trait2','gwas1','gwas2','cov','cov_se', 'cor','cor_se','p']
      import("@/vendor/Export2Excel").then((excel) => {
        const filterVal = theader;
        data = this.formatJson(filterVal, data);
        excel.export_json_to_excel({
          header: theader,
          data,
          filename: 'Genetic_corrlelation_'  + this.getDate(),
          autoWidth: this.autoWidth,
          bookType: this.bookType,
        });
        // this.downloadLoading = false;
      });
    }
    }
  };

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
</style>

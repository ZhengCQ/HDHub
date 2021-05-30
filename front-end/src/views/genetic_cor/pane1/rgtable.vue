<template>
  <div>
    <!--页码 开始-->
    <pagination v-show="total_items > 0" :total="total_items" :page.sync="listQuery.page"
      :limit.sync="listQuery.page_size" @pagination="getTables(rgModel,rg_h2)" />
    <!--页码 结束-->
    <!--表格 开始-->
    <el-table ref="traitsPairTable" :data="tableData" border fit highlight-current-row style="width: 100%;"
      :row-key="getRowKeys" @selection-change="handleSelectionChange" align="center">
      </el-table-column>
      <el-table-column type="selection" :reserve-selection="true" width="55" />
      <el-table-column v-for="item in tableKey" :key="item.name" :label="item.label" :prop="item.prop"
        :width="item.width" :align="item.align || 'center'">
        <template slot-scope="scope">
          <span>{{ scope.row[item.name] }}</span>
        </template>
      </el-table-column>
      <!--el-table-column label="Operation" width="100" align="center">
        <template slot-scope="scope">
          <el-button size="small" type="primary" @click="checkDetail(scope.$index, scope.row)">Detail
          </el-button>
        </template>
      </el-table-column-->
      <slot />
    </el-table>
    <!--表格 结束-->
  </div>

</template>

<script>
  import Pagination from "@/components/Pagination";
  import {
    postPairCor
  } from "@/api/genetic_cor";
  export default {
    components: {
      Pagination,
    },
    props: {
      in_bar_table:{
        type:Array
      },
      gwasIds: {
        type: Array,
      },
      rgModel: {
        type: String,
      },
      rg_h2:{
        type: String,
      },
      filterInfo: {
        type: Object
      },
      isTop: {
        type: Boolean
      }
    },
    data() {
      return {
        tableData: [],
        multiSel: this.in_bar_table,
        bar_table: [],
        total_items: 0,
        listQuery: {
          page: 1,
          page_size: 10,
          sort: "+id",
        },
        model: this.rgModel,
        barPlotData_rg: {
          data: [],
          col: [],
          se: [],
          pval: []
        },
        barPlotData_h2: {
          data: [],
          col: [],
          se: [],
        },
        tableKey: [{
            name: "trait1",
            label: "Trait1",
            prop: "trait1",
          },
          {
            name: "trait2",
            label: "Trait2",
            prop: "trait2",
          },
          {
            name: "cor",
            label: "Correlation",
            prop: "cor",
          },
          {
            name: "cor_se",
            label: "Correlation_SE",
            prop: "cor_se",
          },
          {
            name: "p",
            label: "p",
            prop: "p",
          },
          {
            name: "cov",
            label: "Covariance",
            prop: "cov",
          },
          {
            name: "cov_se",
            label: "Covariance_SE",
            prop: "cov_se",
          },
          {
            name: "gwas1",
            label: "gwas1",
            prop: "gwas1",
          },
          {
            name: "gwas2",
            label: "gwas2",
            prop: "gwas2",
          },
          {
            name: "h1",
            label: "h1",
            prop: "h1",
          },
          {
            name: "h1_se",
            label: "h1_se",
            prop: "h1_se",
          },
          {
            name: "h2",
            label: "h2",
            prop: "h2",
          },
          {
            name: "h2_se",
            label: "h2_se",
            prop: "h2_se",
          },
        ],
      };
    },
    mounted() {
      if (this.gwasIds.length > 0){
        this.getTables(this.rgModel, this.rg_h2) 
      }
      if (this.multiSel.length >0 & !this.isTop){
          this.toggleSelection(this.multiSel)
      }
    },
    watch: {
      multiSel: function (val) {
        if (!this.isTop) {
          this.getBarPic(this.rg_h2)
        }
      },
      rgModel: function (val) {
        this.model = val
        // this.$refs.traitsPairTable.clearSelection()
      },
    },
    methods: {
      toggleSelection(rows) {
      this.$nextTick(() => {
        rows.forEach((row) => {
          this.$refs.traitsPairTable.toggleRowSelection(row, true);
        });
      });
    },
      getRowKeys(row) {
        return row.id
      },
      handleSelectionChange(val) {
        this.multiSel = val
      },
      getTables(model_in, rg_h2) {
        this.rg_h2 = rg_h2
        postPairCor({
          value: this.gwasIds,
          query: this.listQuery,
          filter: this.filterInfo,
          activeName: this.activeName,
        }, model_in).then((res) => {
          this.total_items = res.data._meta.total_items;
          this.tableData = res.data.items;
          this.getBarPic(rg_h2)
          this.$notify({
            title: "Success",
            message: "Success count the results",
            type: "success",
            duration: 1000,
          });
        });
      },
      reset_bar(rg_h2) {
        if (rg_h2 == 'rg') {
          for (var i of ['data', 'col', 'se', 'pval']) {
            this.barPlotData_rg[i] = []
          }
        } else if (rg_h2 == 'h2') {
          for (var i of ['data', 'col', 'se']) {
            this.barPlotData_h2[i] = []
          }
        } else {
          console.log(rg_h2 + 'it should be rg or h2')
        }
      },
      getBarPic(rg_h2) {
        this.bar_table = (this.isTop ? this.tableData : this.multiSel)
        this.reset_bar(rg_h2)
        if (this.bar_table.length == 0){
          this.$emit("barPlotData", [this.barPlotData_rg,this.bar_table]);
          return
        }
        var sorted_keys_array = Object.keys(this.bar_table).sort((a, b) => {
            return this.bar_table[b].cor - this.bar_table[a].cor
          })
        if (rg_h2 == 'rg') {
          sorted_keys_array.forEach((v, idx) => {
            var val = this.bar_table[v]
            this.barPlotData_rg.data.push(val.cor)
            this.barPlotData_rg.col.push(val.trait2)
            this.barPlotData_rg.pval.push(val.p)
            this.barPlotData_rg.se.push([
              idx,
              val.cor - val.cor_se * 1.96,
              val.cor + val.cor_se * 1.96
            ])
          })
          this.$emit("barPlotData", [this.barPlotData_rg,this.bar_table]);

        } else {
          var total_indx = 0
          sorted_keys_array.forEach((v, idx) => {
            total_indx = idx
            var val = this.bar_table[v]
            this.barPlotData_h2.data.push(val.h2)
            this.barPlotData_h2.col.push(val.trait2)
            this.barPlotData_h2.se.push([
              idx,
              val.h2 - val.h2_se * 1.96,
              val.h2 + val.h2_se * 1.96
            ])
          })
          this.barPlotData_h2.data.push(this.bar_table[0].h1)
            this.barPlotData_h2.col.push(this.bar_table[0].trait1)
            this.barPlotData_h2.se.push([
              total_indx+1,
              this.bar_table[0].h1 - this.bar_table[0].h1_se * 1.96,
              this.bar_table[0].h1 + this.bar_table[0].h1_se * 1.96
            ])
          this.$emit("barPlotData", [this.barPlotData_h2,this.bar_table]);

        }
      },
    },
  };

</script>

<template>
  <div>
        <!--页码 开始-->
    <pagination v-show="total_items > 0" :total="total_items" :page.sync="listQuery.page"
      :limit.sync="listQuery.page_size" @pagination="getTables()" />
    <!--页码 结束-->
    <!--表格 开始-->
    <el-table ref="traitsPairTable" 
      :data="tableData" 
      border
      fit
      highlight-current-row style="width: 100%;"
      :row-key="getRowKeys"
      @selection-change="handleSelectionChange"
      align="center">
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
import { postPairCor } from "@/api/genetic_cor";
export default {
  components: {
    Pagination,
  },
  props: {
    gwasIds: {
      type: Array,
    },
    rgModel: {
      type: String
    },
    filterInfo:{
      type: Object
    },
    isTop:{
      type: Boolean
    }
  },
  data() {
    return {
      tableData: [],
      multiSel: [],
      total_items: 0,
      listQuery: {
        page: 1,
        page_size: 10,
        sort: "+id",
      },
      barPlotData:{
        data: [],
        col: [],
        se: [],
        pval: []
      },
      tableKey: [
        {
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
  watch: {
    multiSel: function(val) {
      if (!this.isTop) {
        this.getBarPic()
      }
    }
  },
  methods: {
    getRowKeys(row) {
      return row.id
    },
    handleSelectionChange(val) {
      this.multiSel = val
    },
    getTables() {
      postPairCor({
        value: this.gwasIds,
        query: this.listQuery,
        filter: this.filterInfo,
        activeName: this.activeName,
      },this.rgModel).then((res) => {
        this.total_items = res.data._meta.total_items;
        this.tableData = res.data.items;
        this.getBarPic()
        this.$notify({
          title: "Success",
          message: "Success count the results",
          type: "success",
          duration: 1000,
        });
      });
    },
    reset_bar(){
      this.barPlotData.data = []
      this.barPlotData.col = []
      this.barPlotData.se = []
      this.barPlotData.pval = []
    },
    getBarPic() {
      this.reset_bar()
      var bar_table = (this.isTop ? this.tableData: this.multiSel)
      var sorted_keys_array = Object.keys(bar_table).sort((a, b) => {
        return bar_table[b].cor - bar_table[a].cor
      })
      sorted_keys_array.forEach((v, idx) => {
        var val = bar_table[v]
        this.barPlotData.data.push(val.cor)
        this.barPlotData.col.push(val.trait2)
        this.barPlotData.pval.push(val.p)
        this.barPlotData.se.push([
          idx,
          val.cor - val.cor_se,
          val.cor + val.cor_se
        ])
      })
      this.$emit("barPlotData", this.barPlotData);
    },
  },
};
</script>

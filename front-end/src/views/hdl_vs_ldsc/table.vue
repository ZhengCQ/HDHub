<template>
  <div>
    <!--页码 开始-->
    <!--pagination v-show="total_items > 0" :total="total_items" :page.sync="listQuery.page"
      :limit.sync="listQuery.page_size" @pagination="getTables(target_gwas_ids)" /--!>
    <!--页码 结束-->

    <!--表格 开始-->

    <el-table ref="traitsPairTable" :data="tableDataParis" border fit highlight-current-row style="width: 100%;"
      align="center">
      </el-table-column>
      <el-table-column v-for="item in tableKey" :key="item.name" :label="item.label" :prop="item.prop"
        :width="item.width" :align="item.align || 'center'">
        <template slot-scope="scope">
          <span>{{ scope.row[item.name] }}</span>
        </template>
      </el-table-column>
      <slot />
    </el-table>
    <!--表格 结束-->
  </div>
</template>

<script>
import Pagination from "@/components/Pagination";
import { postHdlLdscPairCor } from '@/api/genetic_cor'
export default {
  components: {
    Pagination,
  },
  props: {
    filterInfo:{
      type: Object
    }
  },
  data() {
    return {
      total_items: 0,
        listQuery: {
        page: 1,
        page_size: 10,
        sort: "+id",
      },
      target_gwas_ids:[],
      tableDataParis: [],
      tableKey: [
        {
          name: "trait1_x",
          label: "Trait1",
          prop: "trait1_x",
        },
        {
          name: "trait2_x",
          label: "Trait2",
          prop: "trait2_x",
        },
        {
          name: "cor_HDL",
          label: "Correlation_HDL",
          prop: "cor_HDL",
        },
        {
          name: "cor_se_HDL",
          label: "Correlation_SE_HDL",
          prop: "cor_se_HDL",
        },
        {
          name: "p_HDL",
          label: "p_HDL",
          prop: "p_HDL",
        },
        {
          name: "cov_HDL",
          label: "Covariance_HDL",
          prop: "cov_HDL",
        },
        {
          name: "cov_se_HDL",
          label: "Covariance_SE_HDL",
          prop: "cov_se_HDL",
        },
        {
          name: "cor_LDSC",
          label: "Correlation_LDSC",
          prop: "cor_LDSC",
        },
        {
          name: "cor_se_LDSC",
          label: "Correlation_SE_LDSC",
          prop: "cor_se_LDSC",
        },
        {
          name: "p_LDSC",
          label: "p_LDSC",
          prop: "p_LDSC",
        },
        {
          name: "cov_LDSC",
          label: "Covariance_LDSC",
          prop: "cov_LDSC",
        },
        {
          name: "cov_se_LDSC",
          label: "Covariance_SE_LDSC",
          prop: "cov_se_LDSC",
        }
      ],
    };
  },
  methods: {
    getTables(target_gwas_ids) {
      this.target_gwas_ids = target_gwas_ids
      postHdlLdscPairCor({
        value: target_gwas_ids,
        query: this.listQuery,
        filter: this.filterInfo
      }).then((res) => {
        this.total_items = res.data.total_items
        this.tableDataParis = res.data.items
        this.dataPlot = res.data.data_plot
        this.$emit("ScatterPlotData",this.dataPlot);
      })
    },
  }
};
</script>

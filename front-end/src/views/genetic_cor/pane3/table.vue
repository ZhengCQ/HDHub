<template>
  <div>
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
    <!--页码 开始-->

    <pagination v-show="total_items > 0" :total="total_items" :page.sync="listQuery.page"
      :limit.sync="listQuery.page_size" @pagination="getCyclePairsTables()" />
    <!--页码 结束-->
  </div>
</template>

<script>
import Pagination from "@/components/Pagination";
import { postCyclePairCor } from '@/api/genetic_cor'
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
      tableDataParis: [],
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
  methods: {
    getTables(target_gwas_ids) {
      console.log(target_gwas_ids)
      postCyclePairCor({
        value: target_gwas_ids,
        query: this.listQuery,
        filter: this.filterInfo
      }).then((res) => {
        this.total_items = res.data._meta.total_items
        this.tableDataParis = res.data.items
        this.tableDataParis_allids = res.qy_ids
        this.$emit("PlotData",res);
      })
    },
  }
};
</script>

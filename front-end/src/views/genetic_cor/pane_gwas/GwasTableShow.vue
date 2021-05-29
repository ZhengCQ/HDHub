<template>
  <!-- GWAS性状筛选 开始-->
  <el-table
    ref="traitstabs"
    :data="tableinfo"
    :key="timer"
    border
    fit
    highlight-current-row
    style="width: 100%"
    align="center"
  >
    <el-table-column
      v-for="item in tableTraitKey"
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
    <slot />
  </el-table>
  <!--表格 结束-->
  <!-- GWAS性状筛选 结束-->
</template>

<script>
import { queryInfoDetail } from "@/api/genetic_cor";
export default {
  components: {
    queryInfoDetail,
  },
  data() {
    return {
      tableinfo: null,
      timer : 1,
      gwas_ids: [],
      tableTraitKey: [
        {
          name: "trait",
          label: "Trait",
          prop: "trait",
        },
        {
          name: "filename",
          label: "filename",
          prop: "filename",
        },
        {
          name: "ethnic",
          label: "ethnic",
          prop: "ethnic",
        },
        {
          name: "sex",
          label: "sex",
          prop: "sex",
        },
        {
          name: "sampel_size",
          label: "sampel_size",
          prop: "sampel_size",
        },
        {
          name: "ncase",
          label: "ncase",
          prop: "ncase",
        },
        {
          name: "ncontrol",
          label: "ncontrol",
          prop: "ncontrol",
        },
      ],
    };
  },
  methods: {
    async queryTraitsDetail(traits) {
      // this.reset_datainfo();
        const { data } = await queryInfoDetail({value: { traits: traits}})
        this.tableinfo = data;
        this.tableinfo.forEach((v, idx) => {
          this.tableinfo[idx]['idx'] = idx
        })
    }
  },
};
</script>

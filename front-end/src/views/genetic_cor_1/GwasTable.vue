<template>
  <!-- GWAS性状筛选 开始-->
  <el-table ref="traitstab" :data="tableinfo" border fit highlight-current-row style="width: 100%" align="center"
    @selection-change="handleSelectionChange1">
    <el-table-column type="selection" width="55" />
    <el-table-column v-for="item in tableTraitKey" :key="item.name" :label="item.label" :prop="item.prop"
      :width="item.width" :align="item.align || 'center'">
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
  export default {
    props: {
      tableinfo: {
        type: Array,
      },
    },
    data() {
      return {
        tableTraitKey: [{
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
    mounted() {
      this.toggleSelection(this.tableinfo)
    },

    methods: {
      toggleSelection(rows) {
        if (rows) {
          rows.forEach((row) => {
            // 设置该表格选框选中
              this.$refs.traitstab.toggleRowSelection(row)
          })
        } else {
            this.$refs.traitstab.clearSelection()
        }
      },
      handleSelectionChange1(val) {
        this.$emit("gwasSel", val);

      },

    },
  };

</script>

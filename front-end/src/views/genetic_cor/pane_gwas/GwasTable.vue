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
  import {
    queryInfoDetail
  } from "@/api/genetic_cor";
  export default {
    components: {
      queryInfoDetail
    },
    data() {
      return {
        tableinfo: [],
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
    methods: {
      toggleSelection(rows) {
        this.$nextTick(() => {
          rows.forEach((row) => {
            this.$refs.traitstab.toggleRowSelection(row, true)
          })
        })
      },
      handleSelectionChange1(val) {
        this.$emit("gwasSel", val);
      },
      queryTraitsDetail(traits) {
        // this.reset_datainfo();
        queryInfoDetail({
          value: {
            'traits': traits
          },
        }).then((res) => {
          this.tableinfo = res.data
          this.toggleSelection(this.tableinfo)
                this.oldList = this.tableinfo.map(v => v.id)
      this.newList = this.oldList.slice()
      this.$nextTick(() => {
        this.setSort()
      })
          // this.$emit("traitsDetailData", res.data);
          // 默认选择
          //this.$nextTick(function () {
          //  this.toggleSelection(this.traitsDetailData, "traitstab");
          //});
        });
      },
          setSort() {
      const el = this.$refs.traitstab.$el.querySelectorAll('.el-table__body-wrapper > table > tbody')[0]
      this.sortable = Sortable.create(el, {
        ghostClass: 'sortable-ghost', // Class name for the drop placeholder,
        setData: function(dataTransfer) {
          // to avoid Firefox bug
          // Detail see : https://github.com/RubaXa/Sortable/issues/1012
          dataTransfer.setData('Text', '')
        },
        onEnd: evt => {
          const targetRow = this.list.splice(evt.oldIndex, 1)[0]
          this.list.splice(evt.newIndex, 0, targetRow)

          // for show the changes, you can delete in you code
          const tempIndex = this.newList.splice(evt.oldIndex, 1)[0]
          this.newList.splice(evt.newIndex, 0, tempIndex)
        }
      })
    }
    },
  };

</script>

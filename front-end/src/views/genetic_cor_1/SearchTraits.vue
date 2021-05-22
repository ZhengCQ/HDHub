<template>
  <div>
    <el-form ref="form" :model="form">
      <el-form-item>
        <el-select
          v-model="form.traits"
          filterable
          multiple
          remote
          :remote-method="queryTraits"
          placeholder="input traits name. eg: Type 2 Diabates"
        >
          <el-option
            v-for="item in gene_options"
            :key="item.index"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>

      <el-form-item align="center">
        <el-button
          round
          plain
          type="primary"
          icon="el-icon-search"
          style="margin-bottom: 30px"
          @click="queryTraitsDetail"
          >GO
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { queryInfo, queryInfoDetail } from "@/api/genetic_cor";

export default {
  data() {
    return {
      form: {
        traits: [],
      },
      gene_options: [],
    };
  },
  props:{
    sel_traits:{
      type: Array
    }
  },
  mounted() {
    this.form.traits = this.sel_traits
  },
  methods: {
    queryTraits(queryString, cb) {
      var list = [];
      queryInfo({
        value: queryString,
      })
        .then((res) => {
          var pheinfo = res.data;
          for (const i in pheinfo) {
            list.push({
              value: pheinfo[i],
            });
          }
          // list = queryString ? list.filter(this.createFilter(queryString)) : list
          this.gene_options = list;
          console.log(this.form)
        })
        .catch((error) => {
          console.log(error);
        });
    },
    queryTraitsDetail() {
      // this.reset_datainfo();
      queryInfoDetail({
        value: this.form,
      }).then((res) => {
        this.$emit("traitsDetailData", res.data);
        // 默认选择
        //this.$nextTick(function () {
        //  this.toggleSelection(this.traitsDetailData, "traitstab");
        //});
      });
    },
  },
};
</script>


<style>
.el-select {
  position: relative;
  font-size: 16px;
  display: inline-block;
  width: 100%;
}
</style>

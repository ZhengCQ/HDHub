<template>
  <div class="container">
    <div style="padding-top: 160px">
      <div style="text-align: center">
        <h1>GWAS summary trait</h1>
      </div>
      <div>
        <el-form ref="form" :model="form" class="summit-form">
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
        <div class="row">
          <div class="col-xs-6 col-md-4">
            <h5>
              High-definition likelihood (HDL) is a powerful method for
              estimating genetic correlations between complex traits using
              genome-wide association study (GWAS) summary statistics.
            </h5>
          </div>
          <div class="col-xs-6 col-md-4">
            <h5>
              HD Hub is a centralized database with hundreds of thousands of
              heritability and genetic correlation estimates, estimated using
              HDL based on harmonized summary association statistics for complex
              traits from LD Hub and UK Biobank (UKBB)
            </h5>
          </div>
          <div class="col-xs-6 col-md-4">
            <h5>
              HD Hub is a web-based platform that provides interactive and
              real-time visualizations and analysis of HDL results. Future
              developments of HDL with different extensions can also be explored
              via HD Hub.
            </h5>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { queryInfo, queryInfoDetail } from "@/api/genetic_cor";

export default {
  data() {
    return {
      form: {
        traits: "",
      },
      gene_options: [],
    };
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
        })
        .catch((error) => {
          console.log(error);
        });
    },
    queryTraitsDetail() {
      this.reset_datainfo();
      queryInfoDetail({
        value: this.form,
      }).then((res) => {
        this.traitsDetailData = res.data;
        // 默认选择
        this.$nextTick(function () {
          this.toggleSelection(this.traitsDetailData, "traitstab");
        });
      });
    },
  },
};
</script>


<style lang="scss" scoped>
.el-select {
  position: relative;
  font-size: 16px;
  display: inline-block;
  width: 100%;
}

.summit-form {
  position: relative;
  max-width: 100%;
  margin: 0 auto;
  overflow: hidden;
}

@media (min-width: 1024px) {
  .summit-form {
    width: 50%;
  }
}

@media (max-width: 768px) {
  .summit-form {
    width: 90%;
  }
}
</style>

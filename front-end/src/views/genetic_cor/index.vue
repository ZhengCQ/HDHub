<template>
  <el-container style="border: 1px solid #eee; padding-top: 55px">
    <el-aside
      width="250px"
      style="background-color: rgb(238, 241, 246); padding-top: 50px"
    >
      <div style="text-align: center">
        <el-switch
          style="display: block"
          v-model="ishdl"
          active-color="#13ce66"
          inactive-color="#ff4949"
          active-text="HDL"
          inactive-text="LDSC"
          @change="changeModel"
        >
        </el-switch>
      </div>

      <div class="summit-form">
        <h5>Trait1</h5>
        <search-traits :sel_traits="traits"></search-traits>
      </div>
      <div>
        <h5>Trait2</h5>
        <div style="text-align: center">
          <el-switch
            style="display: block"
            v-model="isTop"
            active-color="#13ce66"
            inactive-color="#ff4949"
            active-text="Top"
            inactive-text="Optional"
            @change="changeTrait2Model"
          >
          </el-switch>
        </div>
        <el-button> NetGraph</el-button>
      </div>
    </el-aside>

    <el-container>
      <set-para
        @fig1asetDialog="fig1aset"
        :isSetup="isSetup"
        :FormInfo="setParaInfo"
      ></set-para>
      <el-header>
        <div style="text-align: left; font-size: 16px">
          <i
            class="el-icon-setting el-icon--left"
            style="margin-right: 15px"
            @click="isSetup = true"
            >数据设置</i
          >
        </div>
      </el-header>

      <el-main>
        <el-tabs v-model="activeName" type="card">
          <el-tab-pane label="BarPlot of Genetic Correlation" name="first">
            <el-row
              style="background: #fff; padding: 0px 0px 0px 0px; width: 100%"
            >
              <div align="center" />

              <div v-if="barPlotData">
                <bar-plot
                  :key="timer"
                  :class-name="subName"
                  :subName="traits[0]"
                  :chart-data="barPlotData.data"
                  :col-data="barPlotData.col"
                  :pval-data="barPlotData.pval"
                  :error-data="barPlotData.se"
                />
              </div>
            </el-row>
            <rg-table
              @barPlotData="getBarData"
              :gwasIds="gwas_ids"
              :rgModel="rgmodel"
              :filterInfo="setParaInfo"
              :isTop="isTop"
              ref="rgtable"
            ></rg-table>
          </el-tab-pane>

          <el-tab-pane label="Scatter of HDL VS LDSC" name="second">
            <div v-if="scatterData">
              <error-pair-scatter
                :key="timer"
                :class-name="traits[0]"
                :chart-data="scatterData"
              />
            </div>
            <pair-table
              @ScatterPlotData="getScatterData"
              :filterInfo="setParaInfo"
              ref="pairtable"
            >
            </pair-table>
          </el-tab-pane>
        </el-tabs>
      </el-main>
    </el-container>
  </el-container>
</template>


<script>
import SetPara from "./setpara.vue";
import SearchTraits from "./SearchTraits.vue";
import RgTable from "./pane1/rgtable.vue";
import BarPlot from "./pane1/BarPlot";
import PairTable from "./pane2/table.vue";
import ErrorPairScatter from "./pane2/ErrorPairScatter";

export default {
  name: "Genetic_cor",
  components: {
    SetPara,
    SearchTraits,
    RgTable,
    BarPlot,
    PairTable,
    ErrorPairScatter,
  },
  data() {
    return {
      traitsDetailData: "",
      timer: "",
      traits: [],
      gwas_ids: [],
      ishdl: true,
      isTop: true,
      rgmodel: "hdl",
      subName: "Genetic Correction",
      barPlotData: "",
      scatterData: "",
      activeName: "first",
      isSetup: false,
      setParaInfo: {
        p_cor: [0.2, 1.2],
        n_cor: [-1.2, -0.2],
        p_cutoff: 0.05,
      },
    };
  },
  created() {
    if (this.$route.params.gwas) {
      this.gwas_ids = this.$route.params.gwas;
      this.traits = this.$route.params.traits;
    }
    if (this.gwas_ids.length == 0) {
      this.gwas_ids = [11];
      this.traits = ["Type 2 Diabetes"];
    }
  },
  mounted() {
    this.getBarInfo();
  },
  watch: {
    activeName: function (val) {
      if (val === "second") {
        this.getScatterInfo();
      }
      if(val === 'first') {
        this.getBarInfo();
      }
    },
  },
  methods: {
    getBarInfo() {
      this.subName =  "BarPlot of Genetic Correction (" + this.rgmodel.toUpperCase() + ")";
      this.$refs.rgtable.getTables(this.rgmodel);
    },
    getScatterInfo() {
        var table_info = this.$refs.rgtable.bar_table;
        var target_gwas_ids = [table_info[1]["gwas1_id"]];
        for (var i of table_info) {
          target_gwas_ids.push(i["gwas2_id"]);
        }        
      this.$refs.pairtable.getTables(target_gwas_ids);
    },
    changeModel() {
      this.ishdl ? (this.rgmodel = "hdl") : (this.rgmodel = "ldsc");
      this.getBarInfo();      
    },
    changeTrait2Model() {
      this.getBarInfo();
    },
    getBarData(data) {
      this.barPlotData = data;
    },
    getScatterData(data) {
      this.scatterData = data;
    },
    fig1aset() {
      this.isSetup = false;
      this.getBarInfo();
    },
  },
};
</script>

<style scoped>
.el-header {
  background-color: #b3c0d1;
  color: #333;
  line-height: 60px;
}

.el-aside {
  color: #333;
}

.el-select {
  position: relative;
  font-size: 14px;
  display: inline-block;
  width: 10%;
}

.summit-form {
  padding-top: 20px;
  position: relative;
  max-width: 95%;
  margin: 0 auto;
  overflow: hidden;
}
</style>

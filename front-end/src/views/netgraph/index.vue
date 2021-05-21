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
        <!--画图 开始-->
        <el-row
          v-show="heatMapData.length > 0"
          style="background: #fff; padding: 0px 0px 0px 0px; width: 100%"
        >
          <heat-map
            :className="traits[0]"
            :chart-data="heatMapData"
            :x-data="colHeatMapData"
            :y-data="colHeatMapData"
          />
        </el-row>

        <!--画图 开始-->
        <el-row
          v-show="netNodes.length > 0"
          style="background: #fff; padding: 0px 0px 0px 0px; width: 100%"
        >
          <net-graph
            :className="traits[0]"
            :nodes="netNodes"
            :links="netLinks"
            :categories="netCategories"
          />
        </el-row>
        <!--画图 结束-->

        <pair-table
          @PlotData="getPlotData"
          :gwasIds="gwas_ids"
          :rgModel="rgmodel"
          :filterInfo="setParaInfo"
          ref="pairtable"
        >
        </pair-table>
      </el-main>
    </el-container>
  </el-container>
</template>
<script>
import SearchTraits from "../genetic_cor/SearchTraits.vue";
import HeatMap from "./charts/HeatMap";
import NetGraph from "./charts/NetGraph";
import PairTable from "./table";
import SetPara from "../genetic_cor_new/setpara.vue";
export default {
  components: {
    SearchTraits,
    HeatMap,
    NetGraph,
    PairTable,
    SetPara,
  },
  data() {
    return {
      traits: "",
      activeName: "first",
      gwas_ids: [],
      gwas1_ids: [],
      gwas2_ids: [],
      heatMapData: [],
      colHeatMapData: [],
      netNodes: [],
      netLinks: [],
      netCategories: [],
      ishdl: "",
      rgmodel: "hdl",
      isTop: true,
      traits: [],
      isSetup: false,
      setParaInfo: {
        p_cor: [0.2, 1.2],
        n_cor: [-1.2, -0.2],
        p_cutoff: 0.05,
      },
    };
  },
  created() {
    this.gwas1_ids = [11];
    this.gwas2_ids = [625, 617, 632, 745, 27, 60, 579, 606, 151, 568];
    // this.gwas_ids.push(this.gwas1_ids)
    this.gwas_ids.push(this.gwas2_ids);
    this.traits = ["Type 2 Diabetes"];
  },
  mounted() {
    this.getInfo();
  },
  methods: {
    getInfo() {
      this.$refs.pairtable.getTables();
    },
    changeModel() {
      this.ishdl ? (this.rgmodel = "hdl") : (this.rgmodel = "ldsc");
      this.getInfo();
      this.$refs.rgtable.multiSel = [];
    },
    changeTrait2Model() {
      this.getInfo();
    },
    fig1aset() {
      this.isSetup = false;
      this.getInfo();
    },
    getPlotData(data) {
      this.heatMapData = data.heatmap.data;
      this.colHeatMapData = data.heatmap.col;
      this.netLinks = data.network.links;
      this.netNodes = data.network.nodes;
      this.netCategories = [
        {
          name: "类别0",
        },
      ];
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
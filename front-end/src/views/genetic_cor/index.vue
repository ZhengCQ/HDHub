<template>
  <el-container style="border: 1px solid #eee; padding-top: 55px">
    <el-aside
      width="250px"
      style="background-color: rgb(238, 241, 246); padding-top: 50px"
    >
      <el-menu
        :default-openeds="['1', '2', '3']"
        :default-active="this.$route.path"
        router
      >
        <el-submenu index="1">
          <template slot="title"
            ><i class="el-icon-setting"></i>Methods Selection</template
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
              :disabled="activeName !== 'first'"
            >
            </el-switch>
          </div>
        </el-submenu>

        <el-submenu index="2">
          <template slot="title"
            ><i class="el-icon-message"></i>Traits Information</template
          >

          <el-menu-item index="/"><i class="el-icon-back"></i> Back Home to Reselect</el-menu-item>

          <el-menu-item-group>
            <template slot="title">Trait1</template>
            <div style="text-align: center">
              <p>{{ traits[0] }}</p>
            </div>
          </el-menu-item-group>

          <el-menu-item-group>
            <template slot="title">Trait2</template>
            <div style="text-align: center">
              <el-switch
                style="display: block"
                v-model="isTop"
                active-color="#13ce66"
                inactive-color="#ff4949"
                active-text="Top"
                inactive-text="Optional"
                :disabled="activeName !== 'first'"
                @change="changeTrait2Model"
              >
              </el-switch>
            </div>
          </el-menu-item-group>
        </el-submenu>
        <el-submenu index="3">
          <template slot="title"
            ><i class="el-icon-menu"></i>Further Exploring</template
          >
          <el-menu-item @click="activeName = 'first'">BarPlot</el-menu-item>
          <el-menu-item
            @click="
              showTabs(1);
              activeName = 'second';
            "
            >Scatter of HDL VS LDSC</el-menu-item
          >
          <el-menu-item
            @click="
              showTabs(2);
              activeName = 'third';
            "
            >NetGraph</el-menu-item
          >
        </el-submenu>
      </el-menu>
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
            >Setup</i
          >
        </div>
      </el-header>

      <el-main>
        <el-tabs v-model="activeName" type="card" ref="tabs">
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
            <div v-show="scatterData">
              <pair-table
                @ScatterPlotData="getScatterData"
                :filterInfo="setParaInfo"
                ref="pairtable"
              >
              </pair-table>
            </div>
          </el-tab-pane>

          <el-tab-pane label="NetGraph" name="third">
            <div v-if="iswaiting" style="padding-top: 20px" align="center">
              <p>
                Your job is running.....</br>
                It may take 3-8 seconds for input items(limit to 20 items).</br>
                Please waiting the results patiently!!!
              </p>
            </div>
            <!--画图 开始-->

            <div v-if="isresults">
              <heat-map
                :className="traits[0]"
                :chart-data="heatMapData"
                :x-data="colHeatMapData"
                :y-data="colHeatMapData"
              />

              <net-graph
                :className="traits[0]"
                :nodes="netNodes"
                :links="netLinks"
                :categories="netCategories"
              />
            </div>

            <div v-show="isresults">
              <net-table
                @PlotData="getNetData"
                :gwasIds="gwas_ids"
                :rgModel="rgmodel"
                :filterInfo="setParaInfo"
                ref="nettable"
              >
              </net-table>
            </div>
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
import NetTable from "./pane3/table.vue";
import HeatMap from "./pane3/HeatMap.vue";
import NetGraph from "./pane3/NetGraph.vue";

export default {
  name: "Genetic_cor",
  components: {
    SetPara,
    SearchTraits,
    RgTable,
    BarPlot,
    PairTable,
    ErrorPairScatter,
    NetTable,
    HeatMap,
    NetGraph,
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
      scatterkey: [],
      iswaiting: true,
      isresults: false,
      job_step: 0,
      netkey: [],
      heatMapData: [],
      colHeatMapData: [],
      netNodes: [],
      netLinks: [],
      netCategories: [],
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
    this.hideTabs();
  },
  watch: {
    activeName: function (val) {
      if (val === "second") {
        this.getScatterInfo();
      }
      if (val === "first") {
        this.getBarInfo();
      }
      if (val === "third") {
        this.getNetInfo();
      }
    },
    colHeatMapData: function (val) {
      if (val.length == 0) {
        this.isresults = false;
        this.iswaiting = true;
      } else if (val.length > 0) {
        this.isresults = true;
        this.iswaiting = false;
      }
    },
  },
  methods: {
    getBarInfo() {
      this.timer = new Date().getTime();
      this.subName =
        "BarPlot of Genetic Correction (" + this.rgmodel.toUpperCase() + ")";
      this.$refs.rgtable.getTables(this.rgmodel);
    },
    getCurrentGwas() {
      var table_info = this.$refs.rgtable.bar_table;
      var target_gwas_ids = [table_info[1]["gwas1_id"]];
      for (var i of table_info) {
        target_gwas_ids.push(i["gwas2_id"]);
      }
      return target_gwas_ids;
    },
    getScatterInfo() {
      this.timer = new Date().getTime();
      var target_gwas_ids = this.getCurrentGwas();
      if (
        this.scatterkey.sort().toString() !== target_gwas_ids.sort().toString()
      ) {
        this.scatterkey = target_gwas_ids;
        this.$refs.pairtable.getTables(target_gwas_ids);
      }
    },
    resetNet() {
      (this.heatMapData = []),
        (this.colHeatMapData = []),
        (this.netNodes = []),
        (this.netLinks = []),
        (this.netCategories = []);
    },
    getNetInfo() {
      this.timer = new Date().getTime();
      var target_gwas_ids = this.getCurrentGwas();
      if (this.netkey.sort().toString() !== target_gwas_ids.sort().toString()) {
        this.netkey = target_gwas_ids;
        this.resetNet();
        this.$refs.nettable.getTables(target_gwas_ids);
      }
    },
    hideTabs() {
      // this.$refs.tabs.$children[0].$el.style.display = 'none';
      this.$nextTick(() => {
        this.$refs.tabs.$children[0].$refs.tabs[1].style.display = "none";
        this.$refs.tabs.$children[0].$refs.tabs[2].style.display = "none";
      });
    },
    showTabs(idx) {
      this.$nextTick(() => {
        this.$refs.tabs.$children[0].$refs.tabs[idx].style.display =
          "inline-block";
      });
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
    getNetData(data) {
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

/deep/ .el-submenu__title {
  font-size: 18px;
}
</style>

<template>
  <el-container style="border: 1px solid #eee; padding-top: 55px">
    <el-aside v-show="isaside" width="250px" style="background-color: rgb(238, 241, 246); padding-top: 60px">
      <el-menu :default-openeds="['1', '2', '3']" :default-active="this.$route.path" router>
        <el-submenu index="1">
          <template slot="title"><i class="el-icon-setting"></i>Methods Selection</template>
          <div style="text-align: center">
            <el-switch style="display: block" v-model="ishdl" active-color="#13ce66" inactive-color="#ff4949"
              active-text="HDL" inactive-text="LDSC" @change="changeModel" :disabled="activeName !== 'first' && activeName !== 'gwas' ">
            </el-switch>
          </div>

          <div v-show="activeName == 'first' || activeName == 'gwas' " style="text-align: center; margin-top:10px">
            <el-switch style="display: block" v-model="isrg" active-color="#13ce66" inactive-color="#ff4949"
              active-text="rg" inactive-text="h2" @change="changeRg">
            </el-switch>
          </div>
        </el-submenu>

        <el-submenu index="2" style="margin-bottom:20px;">
          <template slot="title"><i class="el-icon-message"></i>Traits Information</template>

          <el-menu-item @click="
              showTabs(0);
              hideTabs(1)
              hideTabs(2)
              hideTabs(3)
              isconfirmed=false;
              activeName = 'gwas';
            "> <i class="el-icon-edit"></i> ReSelect Traits </el-menu-item>


          <el-menu-item ><i class="el-icon-back"></i> Back Home to ReInput</el-menu-item>

          <el-menu-item-group>
            <template slot="title">Trait1</template>
            <div style="text-align: center">
              <p>{{ traits[0] }}</p>
            </div>
          </el-menu-item-group>

          <el-menu-item-group>
            <template slot="title">Trait2</template>
            <div style="text-align: center">
              <el-switch style="display: block" v-model="isTop" active-color="#13ce66" inactive-color="#ff4949"
                active-text="Top" inactive-text="Optional" :disabled="activeName !== 'first'"
                @change="changeTrait2Model">
              </el-switch>
            </div>
          </el-menu-item-group>
        </el-submenu>

        <el-submenu index="3" v-show='isconfirmed'>
          <template slot="title"><i class="el-icon-menu"></i>Further Exploring</template>
          <el-menu-item @click="activeName = 'first'">BarPlot of Trait1 vs Others</el-menu-item>
          <el-menu-item @click="
              showTabs(2);
              activeName = 'second';
            ">Scatter(rg) of HDL vs LDSC </el-menu-item>
          <el-menu-item @click="
              showTabs(3);
              activeName = 'third';
            ">NetGraph(rg) of Pairwise</el-menu-item>
        </el-submenu>
      </el-menu>
    </el-aside>

    <el-container>
      <set-para @fig1asetDialog="fig1aset" :isSetup="isSetup" :FormInfo="setParaInfo"></set-para>
      <el-header>

        <el-button v-if="isaside" plain type="success" @click="isaside=false;timer = new Date().getTime();">
          Close Left
        </el-button>
        <el-button v-else type="warning" plain @click="isaside=true;timer = new Date().getTime();">
          Show Left
        </el-button>
        <span v-show="activeName != 'third'" style="padding-left:20px;font-size: 16px">
          <i class="el-icon-setting" @click="isSetup = true">Setup</i>
        </span>
      </el-header>

      <el-main>
        <el-tabs v-model="activeName" type="card" ref="tabs" closable @tab-remove="removeTab">
          <el-tab-pane label="Traits Informations" name="gwas">
            <div style="padding-top: 20px; padding-bottom: 20px;" align="left">
              <h5>
                Trait1: {{traits[0]}} </br>
              </h5>
              <p>
                First Row ----> Trait1 </br>
              </p>
              <h5>
                Trait2: Others </br>
              </h5>
              <p>
                Others Row ----> Trait2 </br>
                if Trait2:
                Trait1 VS Trait2
                else:
                Trait1 vs all Traits in database
              </p>

              <h5>
                Try to Drag Table to ReOrder Traits.
              </h5>
            </div>

        <el-button
          round
          plain
          type="primary"
          icon="el-icon-check"
          style="margin-bottom: 30px"
          @click="toConfirm()"
          >Confirm and GO
        </el-button>

        <el-button
          round
          plain
          type="primary"
          icon="el-icon-edit"
          style="margin-bottom: 30px"
          @click="toEdit()"
          >Edit
        </el-button>
      
            <div v-if="isconfirmed">
                <gwas-table-show  :key="22" @gwasSel="getGwasSel" ref="gwastab"></gwas-table-show>

            </div>
             <div v-else>
                <gwas-table  :key="33" @gwasSel="getGwasSel" ref="gwastab"></gwas-table>
            </div>           

          </el-tab-pane>
          <el-tab-pane label="BarPlot" name="first">
            <el-row style="background: #fff; padding: 0px 0px 0px 0px; width: 100%">
              <div align="center" />
              <div v-if="barPlotData">
                <bar-plot :key="timer" :class-name="className" :subName="subName" :chart-data="barPlotData.data"
                  :col-data="barPlotData.col" :pval-data="barPlotData.pval" :error-data="barPlotData.se" />
              </div>
            </el-row>

            <rg-table :key="timer" @barPlotData="getBarData"  :rg_h2="rg_h2" :gwasIds="gwas_ids" :rgModel="rgmodel"
              :filterInfo="setParaInfoBar" :isTop="isTop" :in_bar_table="barTable" ref="rgtable"></rg-table>
          </el-tab-pane>

          <el-tab-pane label="Scatter" name="second">
            <div v-if="scatterData">
              <error-pair-scatter :key="timer" :class-name="traits[0]" :chart-data="scatterData" />
            </div>
            <div v-show="scatterData">
              <pair-table @ScatterPlotData="getScatterData" :filterInfo="setParaInfoScatter" ref="pairtable">
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
              <heat-map :key="timer" :className="traits[0]" :rgModel="rgmodel" :chart-data="heatMapData"
                :x-data="colHeatMapData" :y-data="colHeatMapData" />
              <net-graph :key="timer+1" :rgModel="rgmodel" :className="traits[0]" :nodes="netNodes" :links="netLinks"
                :categories="netCategories" />
            </div>

            <div v-show="isresults">
              <net-table @PlotData="getNetData" :gwasIds="gwas_ids" :rgModel="rgmodel" :filterInfo="setParaInfoNet"
                ref="nettable">
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
  import GwasTable from "./pane_gwas/GwasTable.vue";
  import GwasTableShow from "./pane_gwas/GwasTableShow.vue";
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
      GwasTable,
      GwasTableShow,
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
        isaside: true,
        traits: [],
        gwas_ids: [],
        isconfirmed: false,
        target_gwas_ids: [],
        ishdl: true,
        isrg: true,
        isTop: true,
        rgmodel: "hdl",
        rgmodel_pre: "hdl",
        rg_h2: "rg",
        subName: "",
        className: "",
        barPlotData: "",
        barTable: [],
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
        activeName: "gwas",
        isSetup: false,
        setParaInfo: {
          p_cor: [0.2, 1.2],
          n_cor: [-1.2, -0.2],
          p_cutoff: 0.05,
        },
        setParaInfoBar: {
          p_cor: [0.2, 1.2],
          n_cor: [-1.2, -0.2],
          p_cutoff: 0.05,
        },
        setParaInfoScatter: {
          p_cor: [0, 2],
          n_cor: [-2, 0],
          p_cutoff: 1,
        },
        setParaInfoNet: {
          p_cor: [0, 2],
          n_cor: [-2, 0],
          p_cutoff: 1,
        },
      };
    },
    created() {
      if (this.$route.params.traits) {
        // this.gwas_ids = this.$route.params.gwas;
        this.traits = this.$route.params.traits;
      }
      if (this.traits.length == 0) {
        // this.gwas_ids = [25, 11, 49, 7];
        this.traits = [
          "Coronary artery disease",
          "Extreme bmi",
          "Type 2 Diabetes",
          "HDL cholesterol",
          "Total cholesterol in large LDL",
          "Usual walking pace",
          "Vitamin and mineral supplements: Vitamin D"
        ];
      }
    },
    mounted() {
      this.getGwasInfo();
      this.hideTabs(1);
      this.hideTabs(2);
      this.hideTabs(3);
    },
    watch: {
      activeName: function (val) {
        if (val === "first") {
          this.getBarInfo();
          this.setParaInfo = this.setParaInfoBar;
        }
        if (val === "second") {
          this.getScatterInfo();
          this.setParaInfo = this.setParaInfoScatter;
        }
        if (val === "third") {
          this.getNetInfo();
          this.setParaInfo = this.setParaInfoNet;
        }
        if(val == 'gwas'){
          this.getGwasInfo()
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
      isconfirmed: function(val){
        if (this.isconfirmed){
          this.showTabs(1)
        }else{
          this.hideTabs(1)
          this.hideTabs(2)
          this.hideTabs(3)
          this.barTable = []
        }
      }

    },
    methods: {
      getGwasInfo() {
        this.$refs.gwastab.queryTraitsDetail(this.traits);
      },
      getGwasSel(data) {
        this.gwas_ids = [];
        this.traits = [];
        for (var i of data) {
          this.gwas_ids.push(i["id"]);
          this.traits.push(i["trait"]);
        }
      },
      toConfirm(){
        this.isconfirmed = true
        this.getBarInfo()
        this.activeName = 'first'
      },
      toEdit(){
        this.isconfirmed = false
        this.$confirm("You will edit and reselect traits and close all anlysis tabs?","Note",{
            type: "warnings",
          }).then(()=>{
        this.getGwasInfo()
          }
          ).catch(_ => {this.isconfirmed = true
            this.getBarInfo()
            this.activeName = 'first'
          })
      },
      getBarInfo() {
          this.timer = new Date().getTime();
          if (this.isrg) {
            this.className =
              "BarPlot of Genetic Correlation ( rg," +
              this.rgmodel.toUpperCase() +
              ")";
            this.subName = this.traits[0];
          } else {
            this.className =
              "BarPlot of Heritability  ( h2, " + this.rgmodel.toUpperCase() + ")";
            this.subName = "";
          }
      },
      getBarData(data) {
          this.barPlotData = data[0];
          this.barTable = data[1]
          if (this.barTable.length >1) {
            this.target_gwas_ids = [this.barTable[0]["gwas1_id"]];
            for (var i of this.barTable) {
              this.target_gwas_ids.push(i["gwas2_id"]);
            }
          }
      },
      getScatterInfo() {
        this.timer = new Date().getTime();
        this.$refs.pairtable.getTables(this.target_gwas_ids, this.rg_h2);
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
        if (this.netkey.sort().toString() !== this.target_gwas_ids.sort().toString() || this.rgmodel !== this.rgmodel_pre) {
          this.netkey = this.target_gwas_ids;
          this.rgmodel_pre = this.rgmodel
          this.resetNet();
          this.$refs.nettable.getTables(this.target_gwas_ids, this.rgmodel);
        }
      },
      hideTabs(idx) {
        // this.$refs.tabs.$children[0].$el.style.display = 'none';
        this.$nextTick(() => {
          this.$refs.tabs.$children[0].$refs.tabs[idx].style.display = "none";
          // this.$refs.tabs.$children[0].$refs.tabs[2].style.display = "none";
        });
      },
      showTabs(idx) {
        this.$nextTick(() => {
          this.$refs.tabs.$children[0].$refs.tabs[idx].style.display =
            "inline-block";
        });
      },
      removeTab(targetName) {
        if (targetName === "second") {
          this.hideTabs(2);
          this.activeName = "first";
        }
        if (targetName === "third") {
          this.hideTabs(3);
          this.netkey = [];
          this.resetNet();
          this.activeName = "first";
        }
        if (targetName === "first") {
          this.isconfirmed = false
          this.$confirm("You will close all anlysis tabs and return to traits tab?","Note",{
            type: "warnings",
          }).then(()=>{
            this.hideTabs(1)
            this.getGwasInfo()
            this.activeName='gwas'
          }
          ).catch(_ => {
            this.isconfirmed = true
          })
        }

      },
      changeModel() {
        this.ishdl ? (this.rgmodel = "hdl") : (this.rgmodel = "ldsc");
        this.getBarInfo();
      },
      changeRg() {
        this.isrg ? (this.rg_h2 = "rg") : (this.rg_h2 = "h2");
        this.getBarInfo();
      },
      changeTrait2Model() {
        this.getBarInfo();
      },
      getScatterData_rg(data) {
        var scatterData = [];
        for (var i of data) {
          var items = [
            i["trait1_x"] + " _vs_ " + i["trait2_x"],
            i["cor_HDL"],
            i["cor_LDSC"],
            i["cor_LDSC"] - i["cor_se_LDSC"] * 1.96,
            i["cor_LDSC"] + i["cor_se_LDSC"] * 1.96,
            i["cor_HDL"] - i["cor_se_HDL"] * 1.96,
            i["cor_HDL"] + i["cor_se_HDL"] * 1.96,
          ];
          scatterData.push(items);
        }
        return scatterData;
      },
      getScatterData_h2(data) {
        var scatterData = [];
        for (var i of data) {
          var items = [
            i["trait2_x"],
            i["h2_HDL"],
            i["h2_LDSC"],
            i["h2_LDSC"] - i["h2_se_LDSC"] * 1.96,
            i["h2_LDSC"] + i["h2_se_LDSC"] * 1.96,
            i["h2_HDL"] - i["h2_se_HDL"] * 1.96,
            i["h2_HDL"] + i["h2_se_HDL"] * 1.96,
          ];
          scatterData.push(items);
        }
        return scatterData;
      },
      getScatterData(data) {
        this.scatterData = this.getScatterData_rg(data);
        // this.scatterData = this.getScatterData_h2(data)
      },
      getNetData(data) {
        this.heatMapData = data.heatmap.data;
        this.colHeatMapData = data.heatmap.col;
        this.netLinks = data.network.links;
        this.netNodes = data.network.nodes;
        this.netCategories = [{
          name: "类别0",
        }, ];
      },
      fig1aset() {
        this.isSetup = false;
        if (this.activeName === "first") {
          this.getBarInfo();
        } else if (this.activeName === "second") {
          this.getScatterInfo();
        }
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

  /deep/ .el-menu-item-group__title {
    padding: 7px 0 7px 20px;
    font-size: 16px;
    color: #a0b85d;
  }

</style>

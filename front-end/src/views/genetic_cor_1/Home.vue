<template>
  <div class="container">
    <div style="padding-top: 160px">
      <div style="text-align: center">
        <h1>GWAS summary trait</h1>
      </div>
      <div>
        <div class="summit-form">
        <search-traits @traitsDetailData="getTraitsData"></search-traits>
        </div>
  
   <!-- GWAS性状筛选 开始-->
      <div v-if="traitsDetailData" align="center">
        <gwas-table ref="gwastab" @gwasSel="getGwasSel" :key ="timer" :tableinfo="traitsDetailData"></gwas-table>
        <!--表格 结束-->
        <div style="margin-top: 20px">
          <el-button @click="getTables();">Explore</el-button>
        </div>
      </div>
      <!-- GWAS性状筛选 结束-->
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
  import SearchTraits from './SearchTraits.vue'
  import GwasTable from './GwasTable.vue'
  
  export default {
    name: 'Home',
    
    components: {
      SearchTraits,
      GwasTable,
    },
    data() {
      return{
          traitsDetailData:"",
          timer:""
      }
    },
    methods:{
    getTraitsData(data){
      // timer 作为key，每次加载都重置
      this.timer = new Date().getTime()
      this.traitsDetailData = data
    },

    getGwasSel(data){
      this.multiSel = data
    },
    getTables() {
      var tgt_gwas = []
      this.multiSel.forEach((val) => {
        tgt_gwas.push(val.id)
     })
     this.$router.push({name:'Genetic_cor_new',params:{'gwas':tgt_gwas}});
    }
    }
  }

</script>


<style lang="scss" scoped>
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

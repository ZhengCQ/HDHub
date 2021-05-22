<template>
  <!--设置弹框 开始-->
  <el-dialog title="setup" :visible.sync="isSetup" :before-close="close">
    <el-form :model="FormInfo">
      <el-form-item label="Correlation(positive)">
        <div style="width: 80%; padding-left: 25%">
          <el-slider
            v-model="FormInfo.p_cor"
            :min="0"
            :max="3"
            range
            :step="0.1"
            >></el-slider
          >
          <el-input-number
            v-model="FormInfo.p_cor[0]"
            :min="0"
            :max="3"
            :step="0.1"
            placeholder="Min"
          />
          <el-input-number
            v-model="FormInfo.p_cor[1]"
            :min="0"
            :max="3"
            :step="0.1"
            placeholder="Max"
          />
        </div>
      </el-form-item>

      <el-form-item label="Correlation(negative)">
        <div style="width: 80%; padding-left: 25%">
          <el-slider
            v-model="FormInfo.n_cor"
            :min="-3"
            :max="0"
            range
            :step="0.1"
            >></el-slider
          >
          <el-input-number
            v-model="FormInfo.n_cor[0]"
            :min="-3"
            :max="0"
            :step="0.1"
            placeholder="Min"
          />
          <el-input-number
            v-model="FormInfo.n_cor[1]"
            :min="-3"
            :max="0"
            :step="0.1"
            placeholder="Max"
          />
        </div>
      </el-form-item>

      <el-form-item label="Pvalue" prop="p_cutoff">
        <div style="padding-left: 25%">
          <el-input-number
            v-model="FormInfo.p_cutoff"
            :min="0"
            :max="1"
            :step="0.01"
            placeholder="Max"
          />
        </div>
      </el-form-item>
    </el-form>
  </el-dialog>
  <!--设置弹框 结束-->
</template>

<script>
export default {
  props: {
      isSetup:{
          type: Boolean
      },
      FormInfo: {
        p_cor: [0.2, 1.2],
        n_cor: [-1.2, -0.2],
        p_cutoff: 0.05,
      },
  },
  data() {
    return {
    };
  },
  methods:{
      close(){
          this.$emit('fig1asetDialog')
      }
  }
};
</script>




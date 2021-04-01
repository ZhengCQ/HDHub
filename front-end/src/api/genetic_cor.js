import request from '@/utils/request'

export function queryInfo(data) {
  return request({
    url: `/api/queryinfo/traits`,
    method: 'get',
    params: data
  })
}

export function queryInfoDetail(data) {
  return request({
    url: `/api/queryinfodetail/traits`,
    method: 'post',
    data
  })
}

export function postPairCor(data,model) {
    return request({
      url: `/api/pair_genetic_cor/${model}`,
      method: 'post',
      data
    })
  }

  export function postCyclePairCor(data) {
    return request({
      url: `/api/cycle_pair_genetic_cor`,
      method: 'post',
      data
    })
  }

  export function getDetail(id) {
    return request({
      url: `/api/pair_genetic_cor/${id}`,
      method: 'get'
    })
  }

  export function postCluster(data) {
    return request({
      url: `/api/cluster`,
      method: 'post',
      data
    })
  }

  export function postHeatmap(data) {
    return request({
      url: `/api/heatmap`,
      method: 'post',
      data
    })
  }


  export function postNetwork(data) {
    return request({
      url: `/api/network`,
      method: 'post',
      data
    })
  }
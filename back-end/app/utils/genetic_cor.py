from app.models import Genetic_Cor_LDSC, Genetic_Cor_LDSC
from sqlalchemy import or_,and_
import pandas as pd
import numpy as np
import itertools
import seaborn as sns
from itertools import cycle
from matplotlib import colors
from collections import Counter

def fetch_paired_gwas(gwas1, gwas2_lst, filter_cut):
    if len(gwas2_lst)>0:
        gwas2_ids = [i.id for i in gwas2_lst]
        querys  = Genetic_Cor.query.filter(
            and_(
              or_(
                and_(Genetic_Cor.gwas1.in_(gwas2_ids),Genetic_Cor.gwas2 == gwas1.id),\
                and_(Genetic_Cor.gwas1 == gwas1.id, Genetic_Cor.gwas2.in_(gwas2_ids))
             ),
             Genetic_Cor.p <=filter_cut['p_cutoff']
            )
            )
    else:
        querys  = Genetic_Cor.query.filter(
            and_(
              or_(Genetic_Cor.gwas1 == gwas1.id,Genetic_Cor.gwas2 == gwas1.id),
              Genetic_Cor.p <= filter_cut['p_cutoff'],
              or_(
              and_(Genetic_Cor.cor >= filter_cut['p_cor'][0],Genetic_Cor.cor <= filter_cut['p_cor'][1]),
              and_(Genetic_Cor.cor >= filter_cut['n_cor'][0],Genetic_Cor.cor <= filter_cut['n_cor'][1])
              )
            ))
    return querys

def trans_order_table(gwas1,data):
    trans_data = []
    for each in data:
        if each['gwas2_id'] == gwas1:
            each['trait1'],each['trait2'] = each['trait2'],each['trait1']
            each['gwas1'],each['gwas2'] = each['gwas2'],each['gwas1']
            each['gwas1_id'],each['gwas2_id'] = each['gwas2_id'],each['gwas1_id']
        trans_data.append(each)
    return trans_data


def pre_heatmap(df):
    df_pivot_cor = pd.pivot_table(df, index='trait1',columns='trait2',values='cor')
    df_pivot_pval = pd.pivot_table(df, index='trait1',columns='trait2',values='p')
    hData = []
    hcol = list(df_pivot_cor.columns)
    for each in itertools.product(hcol, repeat=2):
        if each[0] == each[1]:
            hData.append([each[0],each[1],1])
        else:
            try:
                if not np.isnan(df_pivot_cor.at[each[0],each[1]]):
                    hData.append([each[0],each[1],df_pivot_cor.at[each[0],each[1]],df_pivot_pval.at[each[0],each[1]]])

                elif not np.isnan(df_pivot_cor.at[each[1],each[0]]):
                    hData.append([each[0],each[1],df_pivot_cor.at[each[1],each[0]],df_pivot_pval.at[each[1],each[0]]])
                else:
                    hData.append([each[0],each[1],0,1])
            except:

                hData.append([each[0],each[1],0,1])
    return hData,hcol

def pre_network(df):
    def get_nodes(df):
        counts = Counter(list(df['trait1']) + list(df['trait2'])).most_common()
        df_counts = pd.DataFrame(counts)
        df_counts = df_counts.sort_values(0,ascending=False).reset_index(drop=True)
        df_counts = df_counts.reset_index()
        df_counts.columns=['id','name','value']
        df_counts['symbolSize'] = np.log2(df_counts['value'])*10
        nodes=[]
        for each in df_counts.to_dict('records'):
            each.setdefault("itemStyle",{"normal": {"color": colors.to_hex(next(color_infos))}}),
            each.setdefault('category',0)
            each.setdefault('tooltip', f" Trait: {each['name']} <br>Number of Nodes: {int(each['value']/2)}")
            nodes.append(each)
        return nodes
    
    def get_links(df,name2id):
        links = []
        for idx,each in df.iterrows():
            tmp = {}
            tmp.setdefault('id',idx)
            tmp.setdefault('source',name2id[each['trait1']])
            tmp.setdefault('target',name2id[each['trait2']])

            if abs(each['cor'])>0.9:
                width = 3
            elif abs(each['cor'])>0.7:
                width= 2.5
            elif abs(each['cor'])>0.5:
                width= 2
            elif abs(each['cor'])>0.3:
                width= 1.5
            elif abs(each['cor'])>0.1:
                width= 1
            else:
                width= 0.5
            
            if each['cor']>0:
                tmp.setdefault("lineStyle",{"width": width,"color":'red'})
            else:
                tmp.setdefault("lineStyle",{"width": width,"color":'green'})
            tmp.setdefault('tooltip', f" Trait1: {each[0]} <br>Trait2: {each[1]}<br> rg: {each['cor']}")
            links.append(tmp)
        return links
    
    color_set = sns.color_palette(palette=None, n_colors=10)
    color_infos = cycle(color_set)
    df = df[(df['p'] <0.05)]
    nodes = get_nodes(df)
    name2id = {i[0]:i[1] for i in pd.DataFrame(nodes)[['name','id']].to_dict('split')['data']}
    links = get_links(df,name2id)
    return nodes,links
            


def pre_network_pre(df):
    color_set = sns.color_palette(palette=None, n_colors=10)
    color_infos = cycle(color_set)
    
    df_pivot = pd.pivot_table(df, index='trait1',columns='trait2',values='cor')
    df = df[(df['p'] <0.05)]
    hcol = list(df_pivot.columns)
    traits_ids_idx = [i for i,v in enumerate(hcol)]
    print(hcol)
    print(traits_ids_idx)
    nodes = []
    traits_idx=0
    for each in hcol:
        tmp_dic = {}
        tmp_dic.setdefault('id',traits_idx)
        tmp_dic.setdefault('name',each)
        tmp_dic.setdefault('value',100)
        tmp_dic.setdefault('label',{'normal': {'show': True}})
        tmp_dic.setdefault("itemStyle",{"normal": {"color": colors.to_hex(next(color_infos))}})
        tmp_dic.setdefault('category',0)
        nodes.append(tmp_dic)
        traits_idx+=1

    links = []
    for i in itertools.permutations(traits_ids_idx,2):
        each = (hcol[i[0]],hcol[i[1]])
        tmp={}
        if not np.isnan(df_pivot.at[each[0],each[1]]):
            if df_pivot.at[each[0],each[1]]>0:
                tmp.setdefault("lineStyle",{"width": abs(df_pivot.at[each[0],each[1]]),"color":'red'})
            else:
                tmp.setdefault("lineStyle",{"width": abs(df_pivot.at[each[0],each[1]]),"color":'green'})
            tmp.setdefault('tooltip', f" Trait1: {each[0]} Trait2: {each[1]} rg: {df_pivot.at[each[0],each[1]]}")
            tmp.setdefault('source',i[0])
            tmp.setdefault('target',i[1])
            links.append(tmp)
    return nodes,links
    
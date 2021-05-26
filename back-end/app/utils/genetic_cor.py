from app.models import Genetic_Cor_LDSC, Genetic_Cor_LDSC
from sqlalchemy import or_,and_
import pandas as pd
import numpy as np
import itertools
import seaborn as sns
from itertools import cycle
from matplotlib import colors

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
    color_set = sns.color_palette(palette=None, n_colors=10)
    color_infos = cycle(color_set)
    df_pivot = pd.pivot_table(df, index='trait1',columns='trait2',values='cor')
    hcol = list(df_pivot.columns)
    traits_ids_idx = [i for i,v in enumerate(hcol)]
    
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
    
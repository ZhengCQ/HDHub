import os

from numpy.core.numeric import outer
from app.extensions import db
from flask import jsonify,request
from app.api import bp
from app.models import *
import time
from sqlalchemy import or_,and_
import pandas as pd
import numpy as np
import itertools
import seaborn as sns
from itertools import cycle
from matplotlib import colors
import datetime

from app.utils.genetic_cor import fetch_paired_gwas, trans_order_table,pre_heatmap,pre_network

@bp.route('/queryinfo/traits', methods=['GET'])
def trait_queryinfo():
    '''从数据库中搜索表型'''
    name = request.args.get('value')
    data = []
    if name:
        Infos = GWAS2Traits.query.filter(GWAS2Traits.Trait.contains('{}'.format(name))).all()
        data = [each.Trait for each in Infos]
    return jsonify({'code': 200, 'data': data})


@bp.route('/queryinfodetail/traits', methods=['POST'])
def trait_queryinfodetail():
    '''从数据库中搜索表型详细信息'''
    data = request.get_json()
    traits = data['value']['traits']
    traits_infos = []
    for trait in traits:
        trait_info = GWAS2Traits.query.filter(GWAS2Traits.Trait == trait).all()
        traits_infos.extend([i.to_dict() for i in trait_info])
    return jsonify({'code': 200, 'data': traits_infos})


@bp.route('/pair_genetic_cor/<rgmodel>', methods=['POST'])
def query_geneticcor(rgmodel):
    data = request.get_json()
    query = data['query']
    value = data['value']
    filter_cut = data['filter']
    ### values from front
    page = query['page']
    page_size = query['page_size']
    ### Trait1 info
    starttime = datetime.datetime.now()
    in_gwas1 = value[0]
    in_gwas2 = value[1:]

    if rgmodel == 'hdl':
        if len(in_gwas2) == 0:
            outdata = Genetic_Cor_HDL().to_collection_dict(
            Genetic_Cor_HDL().query.filter(
                            and_(or_(Genetic_Cor_HDL.gwas1.in_(value),Genetic_Cor_HDL.gwas2.in_(value)),
                                Genetic_Cor_HDL.p <= filter_cut['p_cutoff'],
                            or_(
                                and_(Genetic_Cor_HDL.cor >= filter_cut['p_cor'][0],Genetic_Cor_HDL.cor <= filter_cut['p_cor'][1]),
                                and_(Genetic_Cor_HDL.cor >= filter_cut['n_cor'][0],Genetic_Cor_HDL.cor <= filter_cut['n_cor'][1]))
                                )).order_by(Genetic_Cor_HDL.cor.desc()),\
                    page, page_size)
        else:
            outdata = Genetic_Cor_HDL().to_collection_dict(
            Genetic_Cor_HDL().query.filter(
                            and_(or_(
                                    and_(Genetic_Cor_HDL.gwas1 == in_gwas1, Genetic_Cor_HDL.gwas2.in_(in_gwas2)),
                                    and_(Genetic_Cor_HDL.gwas1.in_(in_gwas2), Genetic_Cor_HDL.gwas2 == in_gwas1)),
                                Genetic_Cor_HDL.p <= filter_cut['p_cutoff'],
                            or_(
                                and_(Genetic_Cor_HDL.cor >= filter_cut['p_cor'][0],Genetic_Cor_HDL.cor <= filter_cut['p_cor'][1]),
                                and_(Genetic_Cor_HDL.cor >= filter_cut['n_cor'][0],Genetic_Cor_HDL.cor <= filter_cut['n_cor'][1]))
                                )).order_by(Genetic_Cor_HDL.cor.desc()),\
                    page, page_size)

        
    else:
        if len(in_gwas2) == 0:
            outdata = Genetic_Cor_LDSC().to_collection_dict(
            Genetic_Cor_LDSC().query.filter(
                            and_(or_(Genetic_Cor_LDSC.p1.in_(value),Genetic_Cor_LDSC.p2.in_(value)),
                                Genetic_Cor_LDSC.p <= filter_cut['p_cutoff'],
                            or_(
                                and_(Genetic_Cor_LDSC.rg >= filter_cut['p_cor'][0],Genetic_Cor_LDSC.rg <= filter_cut['p_cor'][1]),
                                and_(Genetic_Cor_LDSC.rg >= filter_cut['n_cor'][0],Genetic_Cor_LDSC.rg <= filter_cut['n_cor'][1]))
                                )).order_by(Genetic_Cor_LDSC.rg.desc()),\
                    page, page_size)
        else:
            outdata = Genetic_Cor_LDSC().to_collection_dict(
            Genetic_Cor_LDSC().query.filter(
                            and_(or_(
                                    and_(Genetic_Cor_LDSC.p1 == in_gwas1, Genetic_Cor_LDSC.p2.in_(in_gwas2)),
                                    and_(Genetic_Cor_LDSC.p1.in_(in_gwas2), Genetic_Cor_LDSC.p2 == in_gwas1)),
                                Genetic_Cor_LDSC.p <= filter_cut['p_cutoff'],
                            or_(
                                and_(Genetic_Cor_LDSC.rg >= filter_cut['p_cor'][0],Genetic_Cor_LDSC.rg <= filter_cut['p_cor'][1]),
                                and_(Genetic_Cor_LDSC.rg >= filter_cut['n_cor'][0],Genetic_Cor_LDSC.rg <= filter_cut['n_cor'][1]))
                                )).order_by(Genetic_Cor_LDSC.rg.desc()),\
                    page, page_size)
                
    outdata['items'] = trans_order_table(value[0],outdata['items'])
    endtime = datetime.datetime.now()
    print ((endtime - starttime))
    return jsonify({'code': 200,'data':outdata})

@bp.route('/pair_genetic_cor/<int:id>', methods=['GET'])
def query_detail(id):
    genetic_cor = Genetic_Cor.query.get_or_404(id)
    gwas1_info = GWAS2Traits.query.filter_by(id =GWAS2Traits.gwas1).first()
    return jsonify({'code': 200})


@bp.route('/cycle_pair_genetic_cor/<rgmodel>', methods=['POST'])
def query_cycle_geneticcor(rgmodel):
    data = request.get_json()
    query = data['query']
    gwaslst = data['value']
    #### top20
    gwaslst = gwaslst[0:20]
    filter_cut = data['filter']
    ### values from front
    page = query['page']
    page_size = query['page_size']
    starttime = datetime.datetime.now()
    if rgmodel == 'hdl':
        info_query = Gwaspairs2cor.query.filter(
            and_(Gwaspairs2cor.Trait1_id.in_(gwaslst),
                Gwaspairs2cor.Trait2_id.in_(gwaslst)
                )
            ).outerjoin(Genetic_Cor_HDL).filter(
                        and_(
                            Genetic_Cor_HDL.p <= filter_cut['p_cutoff'],
                            or_(
                                and_(Genetic_Cor_HDL.cor >= filter_cut['p_cor'][0],Genetic_Cor_HDL.cor <= filter_cut['p_cor'][1]),
                                and_(Genetic_Cor_HDL.cor >= filter_cut['n_cor'][0],Genetic_Cor_HDL.cor <= filter_cut['n_cor'][1])) 
                        )).order_by(Gwaspairs2cor.Trait1_id.desc())
    else:
        info_query = Gwaspairs2cor.query.filter(
            and_(Gwaspairs2cor.Trait1_id.in_(gwaslst),
                Gwaspairs2cor.Trait2_id.in_(gwaslst)
                )
            ).outerjoin(Genetic_Cor_LDSC).filter(
                        and_(
                            Genetic_Cor_LDSC.p <= filter_cut['p_cutoff'],
                            or_(
                                and_(Genetic_Cor_LDSC.rg >= filter_cut['p_cor'][0],Genetic_Cor_LDSC.rg <= filter_cut['p_cor'][1]),
                                and_(Genetic_Cor_LDSC.rg >= filter_cut['n_cor'][0],Genetic_Cor_LDSC.rg <= filter_cut['n_cor'][1])) 
                        )).order_by(Gwaspairs2cor.Trait1_id.desc())  
    outdata = Gwaspairs2cor.to_collection_dict_model(info_query,page, page_size, rgmodel)
    
    df = pd.DataFrame([i.to_dict(rgmodel) for i in info_query.all()])[['trait1','trait2','cor','p']]
    hData,hcol = pre_heatmap(df)
    nodes,links = pre_network(df)

    endtime = datetime.datetime.now()
    print ((endtime - starttime))
    return jsonify({'code': 200, 'data': outdata, 'heatmap':{'data':hData,'col':hcol},'network':{'nodes':nodes,'links':links}})


@bp.route('/hdl_ldscPairCor', methods=['POST'])
def query_hdl_ldsc_geneticcor():
    data = request.get_json()
    #query = data['query']
    value = data['value']
    filter_cut = data['filter']
    ### values from front
    #page = query['page']
    #page_size = query['page_size']
    ### Trait1 info
    starttime = datetime.datetime.now()
    gwas1 = value[0]
    gwas2 = value[1:]
    hdl_data = Genetic_Cor_HDL().to_collection_dict(
        Genetic_Cor_HDL().query.filter(
                        and_(or_(
                            and_(Genetic_Cor_HDL.gwas1 == gwas1,Genetic_Cor_HDL.gwas2.in_(gwas2)),
                            and_(Genetic_Cor_HDL.gwas1.in_(gwas2),Genetic_Cor_HDL.gwas2 == gwas1)
                            ),
                            Genetic_Cor_HDL.p <= filter_cut['p_cutoff'],
                         or_(
                            and_(Genetic_Cor_HDL.cor >= filter_cut['p_cor'][0],Genetic_Cor_HDL.cor <= filter_cut['p_cor'][1]),
                            and_(Genetic_Cor_HDL.cor >= filter_cut['n_cor'][0],Genetic_Cor_HDL.cor <= filter_cut['n_cor'][1]))
                            )).order_by(Genetic_Cor_HDL.cor.desc()),\
                1, len(gwas2))

    if len(hdl_data['items'])>=1:
        hdl_data['items'] = trans_order_table(gwas1,hdl_data['items'])
        df_hdl = pd.DataFrame(hdl_data['items'])
        df_hdl.columns = ([i if i in ['gwas1_id', 'gwas2_id', 'trait1', 'trait2', 'gwas1', 'gwas2'] else i + '_HDL' for i in df_hdl])
        df_hdl.drop(['gwas1','gwas2'],axis=1,inplace=True)
        df_hdl.set_index(['gwas1_id', 'gwas2_id'],inplace=True)
    else:
        return jsonify({'code': 400, 'message': 'There are not any value in HDL database with current filtering'})

    ldsc_data = Genetic_Cor_LDSC().to_collection_dict(
        Genetic_Cor_LDSC().query.filter(
                        and_(or_(
                            and_(Genetic_Cor_LDSC.p1 == gwas1,Genetic_Cor_LDSC.p2.in_(gwas2)),
                            and_(Genetic_Cor_LDSC.p1.in_(gwas2),Genetic_Cor_LDSC.p2 == gwas1)
                            ),
                            Genetic_Cor_LDSC.p <= filter_cut['p_cutoff'],
                         or_(
                            and_(Genetic_Cor_LDSC.rg >= filter_cut['p_cor'][0],Genetic_Cor_LDSC.rg <= filter_cut['p_cor'][1]),
                            and_(Genetic_Cor_LDSC.rg >= filter_cut['n_cor'][0],Genetic_Cor_LDSC.rg <= filter_cut['n_cor'][1]))
                            )).order_by(Genetic_Cor_LDSC.rg.desc()),\
                1, len(gwas2))
    
    if len(ldsc_data['items'])>=1:
        ldsc_data['items'] = trans_order_table(gwas1,ldsc_data['items'])
        df_ldsc = pd.DataFrame(ldsc_data['items'])
        df_ldsc.columns = ([i if i in ['gwas1_id', 'gwas2_id', 'trait1', 'trait2', 'gwas1', 'gwas2'] else i + '_LDSC' for i in df_ldsc])
        df_ldsc.drop(['gwas1','gwas2'],axis=1,inplace=True)
        df_ldsc.set_index(['gwas1_id', 'gwas2_id'],inplace=True)
    else:
        return jsonify({'code': 400, 'message': 'There are not any value in LDSC database with current filtering'})  

    df_m = df_hdl.merge(df_ldsc,left_index=True,right_index=True)
    items = df_m.reset_index().to_dict('records')
    total_items = df_m.shape[0]
    df_plot  = pd.DataFrame()
    df_plot['trait'] = df_m['trait1_x'] + '_vs_' + df_m['trait2_x']
    df_plot.loc[:,'cor_HDL'] = df_m['cor_HDL']
    df_plot.loc[:,'cor_LDSC'] = df_m['cor_LDSC']
    df_plot.loc[:,'cor_LDSC_min'] = df_plot['cor_LDSC']-df_m['cor_se_LDSC']*1.96
    df_plot.loc[:,'cor_LDSC_max'] = df_plot['cor_LDSC']+df_m['cor_se_LDSC']*1.96  
    df_plot.loc[:,'cor_HDL_min'] = df_plot['cor_HDL']-df_m['cor_se_HDL']*1.96
    df_plot.loc[:,'cor_HDL_max'] = df_plot['cor_HDL']+df_m['cor_se_HDL']*1.96
        
    data_plot = df_plot.to_dict('split')['data']

    return jsonify({'code': 200, 'data':{'items':items,'total_items':total_items, 'data_plot': data_plot}})


@bp.route('/cluster', methods=['POST'])
def info2cluster():
    indata = request.get_json()
    gwaslst = indata['value']
    filter_cut = indata['filter']
    starttime = datetime.datetime.now()

    infoall = Gwaspairs2cor.query.filter(
        and_(Gwaspairs2cor.Trait1_id.in_(gwaslst),
             Gwaspairs2cor.Trait2_id.in_(gwaslst)
            )
        ).all()

    df = pd.DataFrame([i.to_dict() for i in infoall])[['trait1','trait2','cor']]
    
    hData,hcol = pre_heatmap(df)
    nodes,links = pre_network(df)
    endtime = datetime.datetime.now()

    print ((endtime - starttime))
    return jsonify({'code': 200,  'heatmap':{'data':hData,'col':hcol},'network':{'nodes':nodes,'links':links}})

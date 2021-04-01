import os
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
    print(filter_cut)
    ### Trait1 info
    starttime = datetime.datetime.now()

    cor_ids = ([i.id for i in Genetic_Cor_HDL.query.filter(Genetic_Cor_HDL.gwas1.in_(value)).all()])
    """
    outdata = Gwaspairs2cor.to_collection_dict(
        Gwaspairs2cor.query.filter(
        and_(Gwaspairs2cor.Trait1_id.in_(value)
            )
        ).outerjoin(Genetic_Cor_HDL).filter(
                    and_(Genetic_Cor_HDL.p<0.05,Genetic_Cor_HDL.id.in_(cor_ids))).order_by(Genetic_Cor_HDL.cor.desc()),\
            page, page_size)
    """
    if rgmodel == 'hdl':
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
        outdata = Genetic_Cor_LDSC().to_collection_dict(
        Genetic_Cor_LDSC().query.filter(
                        and_(or_(Genetic_Cor_LDSC.p1.in_(value),Genetic_Cor_LDSC.p2.in_(value)),
                            Genetic_Cor_LDSC.p <= filter_cut['p_cutoff'],
                        or_(
                            and_(Genetic_Cor_LDSC.rg >= filter_cut['p_cor'][0],Genetic_Cor_LDSC.rg <= filter_cut['p_cor'][1]),
                            and_(Genetic_Cor_LDSC.rg >= filter_cut['n_cor'][0],Genetic_Cor_LDSC.rg <= filter_cut['n_cor'][1]))
                            )).order_by(Genetic_Cor_LDSC.rg.desc()),\
                page, page_size)       

    """
    data = Genetic_Cor.to_collection_dict(
        Genetic_Cor.query.filter(
                      and_(Genetic_Cor.id.in_(cor_ids),
                          Genetic_Cor.p <= filter_cut['p_cutoff'],
                        or_(
                            and_(Genetic_Cor.cor >= filter_cut['p_cor'][0],Genetic_Cor.cor <= filter_cut['p_cor'][1]),
                            and_(Genetic_Cor.cor >= filter_cut['n_cor'][0],Genetic_Cor.cor <= filter_cut['n_cor'][1])) 
                     )).order_by(Genetic_Cor.cor.desc()),\
                page, page_size)
    """
    endtime = datetime.datetime.now()
    print ((endtime - starttime))
    return jsonify({'code': 200,'data':outdata})

@bp.route('/pair_genetic_cor/<int:id>', methods=['GET'])
def query_detail(id):
    genetic_cor = Genetic_Cor.query.get_or_404(id)
    gwas1_info = GWAS2Traits.query.filter_by(id =GWAS2Traits.gwas1).first()
    return jsonify({'code': 200})


@bp.route('/cycle_pair_genetic_cor', methods=['POST'])
def query_cycle_geneticcor():
    data = request.get_json()
    query = data['query']
    gwaslst = data['value']
    filter_cut = data['filter']
    ### values from front
    page = query['page']
    page_size = query['page_size']

    starttime = datetime.datetime.now()
    
    outdata = Gwaspairs2cor.to_collection_dict(
        Gwaspairs2cor.query.filter(
        and_(Gwaspairs2cor.Trait1_id.in_(gwaslst),
             Gwaspairs2cor.Trait2_id.in_(gwaslst)
            )
        ).outerjoin(Genetic_Cor).filter(
                      and_(
                          Genetic_Cor.p <= filter_cut['p_cutoff'],
                        or_(
                            and_(Genetic_Cor.cor >= filter_cut['p_cor'][0],Genetic_Cor.cor <= filter_cut['p_cor'][1]),
                            and_(Genetic_Cor.cor >= filter_cut['n_cor'][0],Genetic_Cor.cor <= filter_cut['n_cor'][1])) 
                     )).order_by(Gwaspairs2cor.Trait1_id.desc()),\
                page, page_size)
                
    endtime = datetime.datetime.now()

    print ((endtime - starttime))
    return jsonify({'code': 200, 'data': outdata})

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
    return jsonify({'code': 200, 'heatmap':{'data':hData,'col':hcol},'network':{'nodes':nodes,'links':links}})

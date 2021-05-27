from app.extensions import db
import numpy as np
import pandas as pd

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, **kwargs):
        # 如果当前没有任何资源时，或者前端请求的 page 越界时，都会抛出 404 错误
        # 由 @bp.app_errorhandler(404) 自动处理，即响应 JSON 数据：{ error: "Not Found" }
        resources = query.paginate(page, per_page)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            }
        }
        return data

    def to_collection_dict_model(query, page, per_page, model, **kwargs):
        # 如果当前没有任何资源时，或者前端请求的 page 越界时，都会抛出 404 错误
        # 由 @bp.app_errorhandler(404) 自动处理，即响应 JSON 数据：{ error: "Not Found" }
        resources = query.paginate(page, per_page)
        data = {
            'items': [item.to_dict(model) for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            }
        }
        return data

class Gwaspairs2cor(PaginatedAPIMixin,db.Model):
    __tablename__ = 'gwaspairs2cor_all'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    Trait1_id = db.Column(db.Integer,db.ForeignKey("gwas2traits.id"))
    Trait2_id = db.Column(db.Integer,db.ForeignKey("gwas2traits2.id"))
    hdl_id = db.Column(db.Integer)
    ldsc_id = db.Column(db.Integer)
    hdl_id = db.Column(db.Integer,db.ForeignKey("genetic_cor_hdl.id"))
    ldsc_id = db.Column(db.Integer,db.ForeignKey("genetic_cor_ldsc.id"))

    trait1 = db.relationship('GWAS2Traits')
    trait2 = db.relationship('GWAS2Traits2')
    cor_hdl = db.relationship('Genetic_Cor_HDL')
    cor_ldsc = db.relationship('Genetic_Cor_LDSC')
    
    def to_dict(self,model):
        data = {
            'id': self.id,
            'gwas1_id':self.trait1.id,
            'gwas2_id':self.trait2.id,
            'trait1':self.trait1.Trait,
            'trait2':self.trait2.Trait,
            'gwas1': self.trait1.Filename,
            'gwas2': self.trait2.Filename,
            'cov': self.cor_hdl.cov if not pd.isnull(self.cor_hdl) and model == 'hdl' else self.cor_ldsc.gcov_int if not pd.isnull(self.cor_ldsc) else 0,
            'cov_se': self.cor_hdl.cov_se if not pd.isnull(self.cor_hdl) and model == 'hdl' else self.cor_ldsc.gcov_int_se if not pd.isnull(self.cor_ldsc) else 0,
            'cor': self.cor_hdl.cor if not pd.isnull(self.cor_hdl) and model == 'hdl' else self.cor_ldsc.rg if not pd.isnull(self.cor_ldsc) else 0,
            'cor_se': self.cor_hdl.cor_se if not pd.isnull(self.cor_hdl) and model == 'hdl' else self.cor_ldsc.se if not pd.isnull(self.cor_ldsc) else 0,
            'p': self.cor_hdl.p if not pd.isnull(self.cor_hdl) and model == 'hdl' else self.cor_ldsc.p if not pd.isnull(self.cor_ldsc) else 1,
            'h1': self.cor_hdl.h1 if not pd.isnull(self.cor_hdl) and model == 'hdl' else self.cor_ldsc.h2_obs_p1 if not pd.isnull(self.cor_ldsc) else 0,
            'h1_se': self.cor_hdl.h1_se if not pd.isnull(self.cor_hdl) and model == 'hdl' else self.cor_ldsc.h2_obs_se_p1 if not pd.isnull(self.cor_ldsc) else 0,
            'h2': self.cor_hdl.h2 if not pd.isnull(self.cor_hdl) and model == 'hdl' else self.cor_ldsc.h2_obs_p2 if not pd.isnull(self.cor_ldsc) else 0,
            'h2_se': self.cor_hdl.h2_se if not pd.isnull(self.cor_hdl) and model == 'hdl' else self.cor_ldsc.h2_obs_se_p2 if not pd.isnull(self.cor_ldsc) else 0,        
        }
        return data

class GWAS2Traits2(db.Model):
    __tablename__ = 'gwas2traits2'
    __table_args__ = {"extend_existing": True}
    id          = db.Column(db.Integer, primary_key=True)
    Filename    = db.Column(db.String(128))
    Trait       = db.Column(db.String(128))


class GWAS2Traits(db.Model):
    __tablename__ = 'gwas2traits'
    __table_args__ = {"extend_existing": True}
    id          = db.Column(db.Integer, primary_key=True)
    Filename    = db.Column(db.String(128))
    Trait       = db.Column(db.String(128))
    Ethnic      = db.Column(db.String(64))
    Sex         = db.Column(db.String(64))
    Ncase       = db.Column(db.Integer)
    Ncontrol    = db.Column(db.Integer)
    Sample_size = db.Column(db.Integer)
    
    ## genetic_cor = db.relationship('Genetic_Cor', secondary=gwaspairs2cor,lazy='dynamic')

    def to_dict(self):
        data = {
            'id': self.id,
            'trait': self.Trait,
            'filename': self.Filename,
            'ethnic': self.Ethnic,
            'sex': self.Sex,
            'ncase':  self.Ncase,
            'ncontrol': self.Ncontrol,
            'sampel_size': self.Sample_size
        }
        return data


class Genetic_Cor_HDL(PaginatedAPIMixin,db.Model):
    __tablename__ = 'genetic_cor_hdl'
    id    = db.Column(db.Integer, primary_key=True)
    gwas1 = db.Column(db.Integer)
    gwas2 = db.Column(db.Integer)
    h1   = db.Column(db.REAL)
    h1_se = db.Column(db.REAL)
    h2   = db.Column(db.REAL)
    h2_se = db.Column(db.REAL)   
    cov   = db.Column(db.REAL)
    cov_se = db.Column(db.REAL)
    cor   = db.Column(db.REAL)
    cor_se = db.Column(db.REAL)
    p = db.Column(db.REAL)
    pairs = db.relationship('Gwaspairs2cor', lazy='dynamic')

    def to_dict(self):
        gwas1_info = self.pairs.first().trait1
        gwas2_info = self.pairs.first().trait2
        data = {
            'id': self.id,
            'gwas1_id':gwas1_info.id,
            'gwas2_id':gwas2_info.id,
            'trait1':gwas1_info.Trait,
            'trait2':gwas2_info.Trait,
            'gwas1': gwas1_info.Filename,
            'gwas2': gwas2_info.Filename,
            'h1':self.h1,
            'h1_se':self.h1_se,
            'h2':self.h2,
            'h2_se':self.h2_se,
            'cov': self.cov,
            'cov_se': self.cov_se,
            'cor': self.cor,
            'cor_se': self.cor_se,
            'p': self.p
        }
        return data


class Genetic_Cor_LDSC(PaginatedAPIMixin,db.Model):
    __tablename__ = 'genetic_cor_ldsc'
    id    = db.Column(db.Integer, primary_key=True)
    p1 = db.Column(db.Integer)
    p2 = db.Column(db.Integer)
    rg   = db.Column(db.REAL)
    se   = db.Column(db.REAL)
    z   = db.Column(db.REAL)
    p = db.Column(db.REAL)
    h2_obs_p1  = db.Column(db.REAL)
    h2_obs_se_p1  = db.Column(db.REAL)
    h2_int_p1  = db.Column(db.REAL)
    h2_int_se_p1   = db.Column(db.REAL)
    h2_obs_p2   = db.Column(db.REAL)
    h2_obs_se_p2   = db.Column(db.REAL)
    h2_int_p2   = db.Column(db.REAL)
    h2_int_se_p2   = db.Column(db.REAL)
    gcov_int = db.Column(db.REAL)
    gcov_int_se = db.Column(db.REAL)
    pairs = db.relationship('Gwaspairs2cor', lazy='dynamic')

    def to_dict(self):
        gwas1_info = self.pairs.first().trait1
        gwas2_info = self.pairs.first().trait2
        data = {
            'id': self.id,
            'gwas1_id':gwas1_info.id,
            'gwas2_id':gwas2_info.id,
            'trait1':gwas1_info.Trait,
            'trait2':gwas2_info.Trait,
            'gwas1': gwas1_info.Filename,
            'gwas2': gwas2_info.Filename,
            'h1':self.h2_obs_p1,
            'h1_se':self.h2_obs_se_p1,
            'h2':self.h2_obs_p2,
            'h2_se':self.h2_obs_se_p2,
            'cov': self.gcov_int,
            'cov_se': self.gcov_int_se,
            'cor': self.rg,
            'cor_se': self.se,
            'p': self.p
        }
        return data
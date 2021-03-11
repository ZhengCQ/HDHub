from app.extensions import db

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
"""
gwaspairs2cor = db.Table('gwaspairs2cor',
                       db.Column('Trait1_id',db.Integer,db.ForeignKey("gwas2traits.id")),
                       db.Column('Trait2_id',db.Integer,db.ForeignKey("gwas2traits2.id")),
                       db.Column('Cor_id',db.Integer,db.ForeignKey("genetic_cor.id"))
                       )
"""

class Gwaspairs2cor(PaginatedAPIMixin,db.Model):
    __tablename__ = 'gwaspairs2cor'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    Trait1_id = db.Column(db.Integer,db.ForeignKey("gwas2traits.id"))
    Trait2_id = db.Column(db.Integer,db.ForeignKey("gwas2traits2.id"))
    Cor_id = db.Column(db.Integer,db.ForeignKey("genetic_cor.id"))
    trait1 = db.relationship('GWAS2Traits')
    trait2 = db.relationship('GWAS2Traits2')
    cor = db.relationship('Genetic_Cor')
    
    def to_dict(self):
        data = {
            'id': self.id,
            'gwas1_id':self.trait1.id,
            'gwas2_id':self.trait2.id,
            'trait1':self.trait1.Trait,
            'trait2':self.trait2.Trait,
            'gwas1': self.trait1.Filename,
            'gwas2': self.trait2.Filename,
            'cov': self.cor.cov,
            'cov_se': self.cor.cov_se,
            'cor': self.cor.cor,
            'cor_se': self.cor.cor_se,
            'p': self.cor.p
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


class Genetic_Cor(PaginatedAPIMixin,db.Model):
    __tablename__ = 'genetic_cor'
    id    = db.Column(db.Integer, primary_key=True)
    gwas1 = db.Column(db.Integer)
    gwas2 = db.Column(db.Integer)
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
            'cov': self.cov,
            'cov_se': self.cov_se,
            'cor': self.cor,
            'cor_se': self.cor_se,
            'p': self.p
        }
        return data


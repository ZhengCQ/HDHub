import click
import os
import sys
from flask_babel import gettext as _
from app import create_app
from app.extensions import db
from app.models import  GWAS2Traits, Genetic_Cor, GWAS2Traits2, Gwaspairs2cor
from config import Config

app = create_app(Config)
db.create_all(app=app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)

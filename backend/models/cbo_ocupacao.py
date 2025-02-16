from flask_restful import fields

from helpers.database import db

cbo_ocupacao_fields = {
    "id": fields.Integer,
    "titulo": fields.String
}

class Cbo_ocupacao_Model(db.Model):
    __tablename__ = "cbo_ocupacao"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    titulo = db.Column(db.Text, nullable=False)
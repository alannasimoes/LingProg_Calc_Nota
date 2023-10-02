from . import db
from flask_login import UserMixin


class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno = db.Column(db.String(150))
    nota_trabalho = db.relationship('NotaTrabalho')
    nota_lista = db.relationship('NotaLista')
  

class NotaLista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_aluno = db.Column(db.Integer, db.ForeignKey('aluno.id'))
    id_lista = db.Column(db.Integer, db.ForeignKey('lista.id'))
    nota_lista = db.Column(db.Float)
    
    
class NotaTrabalho(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_aluno = db.Column(db.Integer, db.ForeignKey('aluno.id'))
    id_trabalho = db.Column(db.Integer, db.ForeignKey('trabalho.id'))
    nota_trabalho = db.Column(db.Float)


class Trabalho(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trabalho = db.Column(db.String(150))
    nota = db.relationship('NotaTrabalho')


class Lista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lista = db.Column(db.String(150))
    nota = db.relationship('NotaLista') 


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(150), unique=True)
    senha = db.Column(db.String(150))
    nome = db.Column(db.String(150))

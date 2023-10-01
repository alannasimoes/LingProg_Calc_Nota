from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def criar_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Segredo'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .pags import pags
    from .auth import auth

    app.register_blueprint(pags, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Usuario, Aluno, Lista, Trabalho, NotaLista, NotaTrabalho
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Usuario.query.get(int(id))

    return app


def create_database(app):
    from .models import Trabalho
    
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        novo_trabalho = Trabalho(trabalho='Trabalho 1')
        db.session.add(novo_trabalho)
        db.session.commit()
        novo_trabalho = Trabalho(trabalho='Trabalho 2')
        db.session.add(novo_trabalho)
        db.session.commit()
        
        print('Base de dados criada!')

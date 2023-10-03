'''Código para as páginas referentes ao login e cadastro de usuários'''

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''Função para login de usuários já cadastrados'''
    
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        user = Usuario.query.filter_by(usuario=usuario).first() #verifica se o usuário existe
        if user != None:
            if check_password_hash(user.senha, senha): #verifica a senha
                flash('Logado com sucesso!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('pags.areaLogada')) #redireciona para a área logada
            else:
                flash('Senha incorreta, tente de novo.', category='error')
        else:
            flash('Esse usuário não existe.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    '''Função para logout do usuário'''
    
    logout_user()
    return redirect(url_for('auth.login')) #redireciona para a página de login


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    '''Função para cadastro de novos usuários'''
    
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        nome = request.form.get('nome')
        senha1 = request.form.get('senha1')
        senha2 = request.form.get('senha2') #confirmação da senha

        user = Usuario.query.filter_by(usuario=usuario).first() #verifica se o usuário já existe
        if user != None:
            flash('Esse usuário já existe.', category='error')
        elif len(usuario) < 4: #verifica o tamanho do noome de usuário
            flash('O nome de usuário deve ter mais de 3 caracteres.', category='error')
        elif len(nome) < 2: #verifica o tamanho do nome
            flash('O nome deve ter mais de 1 caracter.', category='error')
        elif senha1 != senha2: #verifica se as duas senhas são iguais
            flash('As senhas não são iguais.', category='error')
        elif len(senha1) < 4: #verifica o tamanho da senha
            flash('A senha deve ter pelo menos 4 caracteres.', category='error')
        else:
            new_user = Usuario(usuario=usuario, 
                               nome=nome, 
                               senha=generate_password_hash(
                               senha1, method='sha256')) #cria o novo usuário
            db.session.add(new_user)
            db.session.commit() #adiciona as informações à base de dados
            login_user(new_user, remember=True)
            flash('Conta criada!', category='success')
            return redirect(url_for('pags.areaLogada')) #redireciona para a área logada

    return render_template("sign_up.html", user=current_user)

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        user = Usuario.query.filter_by(usuario=usuario).first()
        if user:
            if check_password_hash(user.senha, senha):
                flash('Logado com sucesso!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('pags.areaLogada'))
            else:
                flash('Senha incorreta, tente de novo.', category='error')
        else:
            flash('Esse usuário não existe.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        nome = request.form.get('nome')
        senha1 = request.form.get('senha1')
        senha2 = request.form.get('senha2')

        user = Usuario.query.filter_by(usuario=usuario).first()
        if user:
            flash('Esse usuário já existe.', category='error')
        elif len(usuario) < 4:
            flash('O nome de usuário deve ter mais de 3 caracteres.', category='error')
        elif len(nome) < 2:
            flash('O nome deve ter mais de 1 caracter.', category='error')
        elif senha1 != senha2:
            flash('As senhas não são iguais.', category='error')
        elif len(senha1) < 4:
            flash('A senha deve ter pelo menos 4 caracteres.', category='error')
        else:
            new_user = Usuario(usuario=usuario, 
                               nome=nome, 
                               senha=generate_password_hash(
                               senha1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Conta criada!', category='success')
            return redirect(url_for('pags.areaLogada'))

    return render_template("sign_up.html", user=current_user)

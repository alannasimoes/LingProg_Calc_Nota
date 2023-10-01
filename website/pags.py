from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Lista, Aluno, Trabalho, NotaLista, NotaTrabalho
from . import db

pags = Blueprint('pags', __name__)


@pags.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)


@pags.route('/areaLogada', methods=['GET', 'POST'])
@login_required
def areaLogada():
    if request.method == 'POST': 
        if request.form['botao'] == 'Adicionar lista':
            return redirect(url_for('pags.addLista')) 
        
        elif request.form['botao'] == 'Adicionar nota da lista':
            return redirect(url_for('pags.addNotaLista'))
        
        elif request.form['botao'] == 'Adicionar nota do trabalho':
            return redirect(url_for('pags.addNotaTrab'))
        
        else:
            return redirect(url_for('pags.calcSituacao'))

    return render_template("area_logada.html", user=current_user)


@pags.route('/areaLogada/addLista', methods=['GET', 'POST'])
@login_required
def addLista():
    if request.method == 'POST':
        lista = request.form.get('lista')

        verif_lista = Lista.query.filter_by(lista=lista).first()
        
        if verif_lista:
            flash('Essa tarefa já existe.', category='error')
        elif len(lista) < 3:
            flash('O nome da lista deve ter mais de 2 caracteres', category='error')
        else:
            nova_lista = Lista(lista=lista)
            db.session.add(nova_lista)
            db.session.commit()
            flash('Lista criada!', category='success')

    return render_template("add_lista.html", user=current_user)


@pags.route('/areaLogada/addNotaLista', methods=['GET', 'POST'])
@login_required
def addNotaLista():
    if request.method == 'POST':
        aluno = request.form.get('aluno')
        lista = request.form.get('lista')
        nota = request.form.get('nota')

        verif_aluno = Aluno.query.filter_by(aluno=aluno).first()
        verif_lista = Lista.query.filter_by(lista=lista).first()

        id_aluno = Aluno(aluno=aluno).id
        id_lista = Lista(id_aluno=id_aluno, lista=lista).id
        
        if not verif_aluno:
            novo_aluno = Aluno(aluno=aluno)
            db.session.add(novo_aluno)
            db.session.commit()
        
        if not verif_lista:
            flash('Essa tarefa não existe, você deve criá-la antes de adicionar notas.', category='error')

        elif not NotaLista(id_lista=id_lista):
            flash('Esse aluno já possui nota nessa tarefa.', category='error')
        
        else:
            nova_nota = NotaLista(id_lista=id_lista)
            db.session.add(nova_nota)
            db.session.commit()
            flash('Nota adicionada!', category='success')

    return render_template("add_nota_lista.html", user=current_user)


@pags.route('/areaLogada/addNotaTrab', methods=['GET', 'POST'])
@login_required
def addNotaTrab():
    if request.method == 'POST':
        aluno = request.form.get('aluno')
        trabalho = request.form.get('trabalho')
        nota = request.form.get('nota')

        verif_aluno = Aluno.query.filter_by(nome_aluno=aluno).first()
        verif_tarefa = Trabalho.query.filter_by(trabalho=trabalho).first()
        
        id_aluno = Aluno(aluno=aluno).id
        id_trabalho = Trabalho(id_aluno=id_aluno, trabalho=trabalho).id
        
        if not verif_aluno:
            novo_aluno = Aluno(nome_aluno=aluno)
            db.session.add(novo_aluno)
            db.session.commit()
        
        if not verif_tarefa:
            flash('Essa tarefa não existe, você deve criá-la antes de adicionar notas.', category='error')

        elif not NotaLista(id_trabalho=id_trabalho):
            flash('Esse aluno já possui nota nessa tarefa.', category='error')
        else:
            nova_nota = NotaTrabalho(id_trabalho=id_trabalho, nota=nota)
            db.session.add(nova_nota)
            db.session.commit()
            flash('Nota adicionada!', category='success')

    return render_template("add_nota_trab.html", user=current_user)

@pags.route('/areaLogada/calcSituacao', methods=['GET', 'POST'])
@login_required
def calcSituacao():
    return render_template("calc_situacao.html", user=current_user)

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
        print(verif_aluno)
        verif_lista = Lista.query.filter_by(lista=lista).first()
        print(verif_lista)

        id_aluno = Aluno.query.filter_by(aluno=aluno).first()
        if id_aluno != None:
            id_aluno = id_aluno.id
            print(aluno)
            print(id_aluno)
            
        id_lista = Lista.query.filter_by(lista=lista).first()
        if id_lista != None:
            id_lista = id_lista.id
            print(lista)
            print(id_lista)
        
        if verif_aluno == None:
            novo_aluno = Aluno(aluno=aluno)
            db.session.add(novo_aluno)
            db.session.commit()
            id_aluno = Aluno.query.filter_by(aluno=aluno).first().id
        
        if verif_lista == None:
            flash('Essa tarefa não existe, você deve criá-la antes de adicionar notas.', category='error')

        elif NotaLista.query.filter_by(id_aluno=id_aluno, id_lista=id_lista).first() != None:
            flash('Esse aluno já possui nota nessa tarefa.', category='error')
        
        else:
            nova_nota = NotaLista(id_aluno=id_aluno, id_lista=id_lista, nota=nota)
            db.session.add(nova_nota)
            db.session.commit()
            print(NotaLista.query.filter_by(id_aluno=id_aluno, id_lista=id_lista).first())
            flash('Nota adicionada!', category='success')

    return render_template("add_nota_lista.html", user=current_user)


@pags.route('/areaLogada/addNotaTrab', methods=['GET', 'POST'])
@login_required
def addNotaTrab():
    if request.method == 'POST':
        aluno = request.form.get('aluno')
        trabalho = request.form.get('trabalho')
        nota = request.form.get('nota')
        print(trabalho)
        
        verif_aluno = Aluno.query.filter_by(aluno=aluno).first()
        
        id_aluno = Aluno.query.filter_by(aluno=aluno).first()
        if id_aluno != None:
            id_aluno = id_aluno.id
            
        id_trabalho = Trabalho.query.filter_by(trabalho=trabalho).first()
        if id_trabalho == None:
            novo_trabalho = Trabalho(trabalho=trabalho)
            db.session.add(novo_trabalho)
            db.session.commit()
            id_trabalho = Trabalho.query.filter_by(trabalho=trabalho).first().id
        else:
            id_trabalho = id_trabalho.id
        
        if verif_aluno == None:
            novo_aluno = Aluno(aluno=aluno)
            db.session.add(novo_aluno)
            db.session.commit()
            id_aluno = Aluno.query.filter_by(aluno=aluno).first().id

        if trabalho == None:
            flash('Escolha um trabalho.', category='error')
            
        elif NotaTrabalho.query.filter_by(id_aluno=id_aluno, id_trabalho=id_trabalho).first() != None:
            flash('Esse aluno já possui nota nesse trabalho.', category='error')
        
        else:
            nova_nota = NotaTrabalho(id_aluno=id_aluno, id_trabalho=id_trabalho, nota=nota)
            db.session.add(nova_nota)
            db.session.commit()
            flash('Nota adicionada!', category='success')

    return render_template("add_nota_trab.html", user=current_user)


@pags.route('/areaLogada/calcSituacao', methods=['GET', 'POST'])
@login_required
def calcSituacao():
    return render_template("calc_situacao.html", user=current_user)

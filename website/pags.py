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
        
        elif request.form['botao'] == 'Adicionar aluno':
            return redirect(url_for('pags.addAluno'))
        
        else:
            return redirect(url_for('pags.calcSituacao'))

    return render_template("area_logada.html", user=current_user)


@pags.route('/areaLogada/addLista', methods=['GET', 'POST'])
@login_required
def addLista():
    if request.method == 'POST':
        lista = request.form.get('lista')

        verif_lista = Lista.query.filter(Lista.lista==lista).first()
        
        if verif_lista != None:
            flash('Essa tarefa já existe.', category='error')
        elif len(lista) < 3:
            flash('O nome da lista deve ter mais de 2 caracteres', category='error')
        else:
            nova_lista = Lista(lista=lista)
            db.session.add(nova_lista)
            db.session.commit()
            flash('Lista criada!', category='success')

    return render_template("add_lista.html", user=current_user)


@pags.route('/areaLogada/addAluno', methods=['GET', 'POST'])
@login_required
def addAluno():
    if request.method == 'POST':
        aluno = request.form.get('aluno')
        
        verif_aluno = Aluno.query.filter(Aluno.aluno==aluno).first()
        
        if verif_aluno != None:
            flash('Essa aluno já existe.', category='error')
        elif len(aluno) < 3:
            flash('O nome da lista deve ter mais de 2 caracteres', category='error')
        else:
            novo_aluno = Aluno(aluno=aluno)
            db.session.add(novo_aluno)
            db.session.commit()
            flash('Aluno adicionado!', category='success')
    
    return render_template("add_aluno.html", user=current_user)   


@pags.route('/areaLogada/addNotaLista', methods=['GET', 'POST'])
@login_required
def addNotaLista():
    if request.method == 'POST':
        aluno = request.form.get('aluno')
        lista = request.form.get('lista')
        nota = request.form.get('nota')

        id_aluno = Aluno.query.filter(Aluno.aluno==aluno).first().id      
        id_lista = Lista.query.filter(Lista.lista==lista).first().id

        if NotaLista.query.filter(NotaLista.id_aluno==id_aluno, NotaLista.id_lista==id_lista).first() != None:
            flash('Esse aluno já possui nota nessa tarefa.', category='error')
        
        else:
            nova_nota = NotaLista(id_aluno=id_aluno, id_lista=id_lista, nota_lista=nota)
            db.session.add(nova_nota)
            db.session.commit()
            flash('Nota adicionada!', category='success')

    busca= Lista.query.all()
    listas = []
    for lista in busca:
        listas.append(lista.lista)
        
    busca= Aluno.query.all()
    alunos = []
    for aluno in busca:
        alunos.append(aluno.aluno)
        
    return render_template("add_nota_lista.html", user=current_user, listas=listas, alunos=alunos)


@pags.route('/areaLogada/addNotaTrab', methods=['GET', 'POST'])
@login_required
def addNotaTrab():
    if request.method == 'POST':
        aluno = request.form.get('aluno')
        trabalho = request.form.get('trabalho')
        nota = request.form.get('nota')
        
        id_aluno = Aluno.query.filter(Aluno.aluno==aluno).first().id
            
        id_trabalho = Trabalho.query.filter(Trabalho.trabalho==trabalho).first()
        if id_trabalho == None:
            novo_trabalho = Trabalho(trabalho=trabalho)
            db.session.add(novo_trabalho)
            db.session.commit()
            id_trabalho = Trabalho.query.filter(Trabalho.trabalho==trabalho).first().id
        else:
            id_trabalho = id_trabalho.id
            
        if NotaTrabalho.query.filter(NotaTrabalho.id_aluno==id_aluno, NotaTrabalho.id_trabalho==id_trabalho).first() != None:
            flash('Esse aluno já possui nota nesse trabalho.', category='error')
        
        else:
            nova_nota = NotaTrabalho(id_aluno=id_aluno, id_trabalho=id_trabalho, nota_trabalho=nota)
            db.session.add(nova_nota)
            db.session.commit()
            flash('Nota adicionada!', category='success')

    busca= Aluno.query.all()
    alunos = []
    for aluno in busca:
        alunos.append(aluno.aluno)

    return render_template("add_nota_trab.html", user=current_user, alunos=alunos)


@pags.route('/areaLogada/calcSituacao', methods=['GET', 'POST'])
@login_required
def calcSituacao():
    if request.method == 'POST':
        aluno = request.form.get('aluno')
        
        verif_aluno = Aluno.query.filter(Aluno.aluno==aluno).first()
        
        if verif_aluno != None:
            id_aluno = verif_aluno.id
        else:
            flash('Esse aluno não existe.', category='error')
            return render_template("calc_situacao.html", user=current_user)
        
        if NotaTrabalho.query.filter(NotaTrabalho.id_aluno==id_aluno).first() == None:
            flash('Não é possível calcular situção, adicione a nota de pelo menos um trabalho.', category='error')
            return render_template("calc_situacao.html", user=current_user)
        
        parte_trabalhos = 0
        quant = 0
        for nota in NotaTrabalho.query.filter(NotaTrabalho.id_aluno==id_aluno):
            parte_trabalhos += nota.nota_trabalho
            quant += 1
        parte_trabalhos = (parte_trabalhos/quant)*0.8  
        
        if NotaLista.query.filter(NotaLista.id_aluno==id_aluno).first() == None:
            flash('Não é possível calcular situção, adicione a nota de pelo menos uma lista.', category='error')
            return render_template("calc_situacao.html", user=current_user)
        
        parte_listas = 0
        quant = 0
        for nota in NotaLista.query.filter(NotaLista.id_aluno==id_aluno):
            parte_listas += nota.nota_lista
            quant += 1
        parte_listas = (parte_listas/quant)*0.2
        
        media = parte_trabalhos + parte_listas
        media = round(media, 1)
        
        if media >= 7:
            situacao = 'Aprovado'
        elif media >= 3:
            situacao = 'Prova final'
        else:
            situacao = 'Reprovado'
        
        exibir_situacao = True
        
        # return render_template("calc_situacao.html", 
        #                        user=current_user, 
        #                        media=media, 
        #                        aluno=aluno, 
        #                        situacao=situacao,
        #                        exibir_situacao=exibir_situacao)
    else:
        media = None
        aluno = None
        situacao = None
        exibir_situacao = False
        
    busca= Aluno.query.all()
    alunos = []
    for busca_aluno in busca:
        alunos.append(busca_aluno.aluno)
             
    return render_template("calc_situacao.html", 
                            user=current_user, 
                            media=media, 
                            nome_aluno=aluno, 
                            situacao=situacao,
                            exibir_situacao=exibir_situacao,
                            alunos=alunos)

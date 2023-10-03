'''Código para as páginas e ações da área logada do usúario'''

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Lista, Aluno, Trabalho, NotaLista, NotaTrabalho
from . import db

pags = Blueprint('pags', __name__)


@pags.route('/', methods=['GET', 'POST'])
def home():
    '''Função para a página inicial'''
    return render_template("home.html", user=current_user)


@pags.route('/areaLogada', methods=['GET', 'POST'])
@login_required
def areaLogada():
    '''Função para a área logada'''
    nome_usuario = current_user.nome
    
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

    return render_template("area_logada.html", user=current_user, nome_usuario=nome_usuario)


@pags.route('/areaLogada/addLista', methods=['GET', 'POST'])
@login_required
def addLista():
    '''Função para adicionar novas listas'''
    
    if request.method == 'POST':
        lista = request.form.get('lista').title()

        verif_lista = Lista.query.filter(Lista.lista==lista).first() #verifica se a lista já existe
        
        if verif_lista != None:
            flash('Essa tarefa já existe.', category='error')
        elif len(lista) < 3: #verifica o tamanho do nome da lista
            flash('O nome da lista deve ter mais de 2 caracteres', category='error')
        else:
            nova_lista = Lista(lista=lista) #cria nova lista
            db.session.add(nova_lista)
            db.session.commit() #adiciona nova lista à base de dados
            flash('Lista criada!', category='success')

    return render_template("add_lista.html", user=current_user)


@pags.route('/areaLogada/addAluno', methods=['GET', 'POST'])
@login_required
def addAluno():
    '''Função para adicionar novos alunos'''
    
    if request.method == 'POST':
        aluno = request.form.get('aluno').title()
        
        verif_aluno = Aluno.query.filter(Aluno.aluno==aluno).first() #verifica se o aluno já existe
        
        if verif_aluno != None:
            flash('Essa aluno já existe.', category='error')
        elif len(aluno) < 3: #verifica o tamanho do nome do aluno
            flash('O nome da lista deve ter mais de 2 caracteres', category='error')
        else:
            novo_aluno = Aluno(aluno=aluno) #cria novo aluno
            db.session.add(novo_aluno)
            db.session.commit() #adiciona novo aluno à base de dados
            flash('Aluno adicionado!', category='success')
    
    return render_template("add_aluno.html", user=current_user)   


@pags.route('/areaLogada/addNotaLista', methods=['GET', 'POST'])
@login_required
def addNotaLista():
    '''Função para adicionar nota a uma lista'''
    
    if request.method == 'POST':
        aluno = request.form.get('aluno')
        lista = request.form.get('lista')
        nota = request.form.get('nota')

        id_aluno = Aluno.query.filter(Aluno.aluno==aluno).first().id #procura o id do aluno na base de dados    
        id_lista = Lista.query.filter(Lista.lista==lista).first().id #procura o id da lista na base de dados

        if NotaLista.query.filter(NotaLista.id_aluno==id_aluno, NotaLista.id_lista==id_lista).first() != None: #verifica se a lista já tem nota
            flash('Esse aluno já possui nota nessa tarefa.', category='error')  
        else:
            nova_nota = NotaLista(id_aluno=id_aluno, id_lista=id_lista, nota_lista=nota) #cria nova nota
            db.session.add(nova_nota)
            db.session.commit() #adiciona nova nota à base de dados
            flash('Nota adicionada!', category='success')

    busca = Lista.query.all() #busca todas as colunas da tabela Lista
    listas = []
    for lista in busca:
        listas.append(lista.lista) #adiciona na lista todas as linhas da coluna lista
        
    busca = Aluno.query.all() #busca todas as colunas da tabela Aluno
    alunos = []
    for aluno in busca:
        alunos.append(aluno.aluno) #adiciona na lista todas as linhas da coluna aluno
        
    return render_template("add_nota_lista.html", user=current_user, listas=listas, alunos=alunos)


@pags.route('/areaLogada/addNotaTrab', methods=['GET', 'POST'])
@login_required
def addNotaTrab():
    '''Função para adicionar nota a um trabalho'''
    
    if request.method == 'POST':
        aluno = request.form.get('aluno')
        trabalho = request.form.get('trabalho')
        nota = request.form.get('nota')
        
        id_aluno = Aluno.query.filter(Aluno.aluno==aluno).first().id #procura o id do aluno no banco de dados

        id_trabalho = Trabalho.query.filter(Trabalho.trabalho==trabalho).first() #verifica se o trabalho já existe
        if id_trabalho == None: #caso não exista
            novo_trabalho = Trabalho(trabalho=trabalho) #cria um novo trabalho
            db.session.add(novo_trabalho)
            db.session.commit() #adiciona o novo trabalho à base de dados
            id_trabalho = Trabalho.query.filter(Trabalho.trabalho==trabalho).first().id
        else: #caso já exista
            id_trabalho = id_trabalho.id #armazena na variável o id do trabalho
            
        if NotaTrabalho.query.filter(NotaTrabalho.id_aluno==id_aluno, NotaTrabalho.id_trabalho==id_trabalho).first() != None: #verifica se a nota já existe
            flash('Esse aluno já possui nota nesse trabalho.', category='error')
        else:
            nova_nota = NotaTrabalho(id_aluno=id_aluno, id_trabalho=id_trabalho, nota_trabalho=nota) #cria nova nota
            db.session.add(nova_nota)
            db.session.commit() #adiciona noca nota à base de dados
            flash('Nota adicionada!', category='success')

    busca= Aluno.query.all() #busca todas as colunas da tabela Aluno
    alunos = []
    for aluno in busca:
        alunos.append(aluno.aluno) #adiciona na lista todas as linhas da coluna aluno

    return render_template("add_nota_trab.html", user=current_user, alunos=alunos)


@pags.route('/areaLogada/calcSituacao', methods=['GET', 'POST'])
@login_required
def calcSituacao():
    '''Função para calcular situação do aluno e sua média'''
    
    if request.method == 'POST':
        aluno = request.form.get('aluno')
        
        id_aluno = Aluno.query.filter(Aluno.aluno==aluno).first().id #procura o id do aluno no banco de dados
        
        if NotaTrabalho.query.filter(NotaTrabalho.id_aluno==id_aluno).first() == None: #verifica se existe algum trabalho com nota
            flash('Não é possível calcular situção, adicione a nota de pelo menos um trabalho.', category='error')
            return render_template("calc_situacao.html", user=current_user)
        
        parte_trabalhos = 0
        quant = 0
        for nota in NotaTrabalho.query.filter(NotaTrabalho.id_aluno==id_aluno): #cada nota de trabalho é somada
            parte_trabalhos += nota.nota_trabalho
            quant += 1
        parte_trabalhos = (parte_trabalhos/quant)*0.8 #é feita a média das notas e o resultado multiplicado por 0.8 
        
        if NotaLista.query.filter(NotaLista.id_aluno==id_aluno).first() == None: #verifica se existe alguma lista com nota
            flash('Não é possível calcular situção, adicione a nota de pelo menos uma lista.', category='error')
            return render_template("calc_situacao.html", user=current_user)
        
        parte_listas = 0
        quant = 0
        for nota in NotaLista.query.filter(NotaLista.id_aluno==id_aluno): #cada nota de lista é somada
            parte_listas += nota.nota_lista
            quant += 1
        parte_listas = (parte_listas/quant)*0.2 #é feita a média das notas e o resultado multiplicado por 0.8
        
        media = parte_trabalhos + parte_listas #os valores obtidos para as listas e trabalhos são somados
        media = round(media, 1) #o valor da média é arredondado para 1 casa decimal
        
        if media >= 7: #caso a média seja maior ou igual a 7
            situacao = 'Aprovado'
        elif media >= 3: #caso a média seja maior ou igual a 3
            situacao = 'Prova final'
        else: #caso a média seja menor que 3
            situacao = 'Reprovado'
        
        exibir_situacao = True #variável para permitir a exibição do texto com a situção do aluno

    else: #caso a página seja acessada através do método 'GET'
        media = None
        aluno = None
        situacao = None
        exibir_situacao = False
        
    busca= Aluno.query.all() #busca todas as colunas da tabela Aluno
    alunos = []
    for busca_aluno in busca:
        alunos.append(busca_aluno.aluno) #adiciona na lista todas as linhas da coluna aluno
             
    return render_template("calc_situacao.html", 
                            user=current_user, 
                            media=media, 
                            nome_aluno=aluno, 
                            situacao=situacao,
                            exibir_situacao=exibir_situacao,
                            alunos=alunos)
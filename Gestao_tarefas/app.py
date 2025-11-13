# Importa as bibliotecas necessárias do Flask
from flask import Flask, request, render_template, redirect, url_for
import json
import os

# Cria uma instância da aplicação Flask
app = Flask(__name__)

# Nome do arquivo JSON para persistência dos dados
ARQUIVO_JSON = 'tarefas.json'

# Lista global que armazena todas as tarefas cadastradas
# Cada tarefa é um dicionário com: id, texto e completa
tarefas = []

# Contador global que gera IDs únicos e incrementais para cada nova tarefa
proximo_id = 1


def carregar_tarefas():
    """
    Carrega as tarefas do arquivo JSON se ele existir.
    
    Esta função verifica se o arquivo JSON existe, lê seu conteúdo
    e restaura a lista de tarefas e o contador de IDs.
    
    Retorna:
        None: A função modifica as variáveis globais tarefas e proximo_id
    """
    global tarefas, proximo_id
    # Verifica se o arquivo JSON existe
    if os.path.exists(ARQUIVO_JSON):
        try:
            # Abre e lê o arquivo JSON
            with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                # Restaura a lista de tarefas
                tarefas = dados.get('tarefas', [])
                # Restaura o contador de IDs (pega o maior ID + 1)
                if tarefas:
                    proximo_id = max(tarefa['id'] for tarefa in tarefas) + 1
                else:
                    proximo_id = 1
        except (json.JSONDecodeError, IOError) as e:
            # Se houver erro ao ler o arquivo, inicia com lista vazia
            print(f"Erro ao carregar tarefas: {e}")
            tarefas = []
            proximo_id = 1


def salvar_tarefas():
    """
    Salva as tarefas atuais no arquivo JSON.
    
    Esta função escreve a lista de tarefas e o contador de IDs
    no arquivo JSON para persistência dos dados.
    
    Retorna:
        None: A função apenas salva os dados no arquivo
    """
    global tarefas, proximo_id
    try:
        # Cria um dicionário com os dados a serem salvos
        dados = {
            'tarefas': tarefas,
            'proximo_id': proximo_id
        }
        # Escreve no arquivo JSON
        with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
    except IOError as e:
        # Se houver erro ao salvar, imprime mensagem
        print(f"Erro ao salvar tarefas: {e}")


def adicionar_tarefa(texto):
    """
    Adiciona uma nova tarefa à lista global de tarefas.
    
    Esta função cria um novo dicionário representando uma tarefa com:
    - id: número único gerado automaticamente
    - texto: descrição da tarefa fornecida pelo usuário
    - completa: status inicial sempre False (tarefa pendente)
    
    Parâmetros:
        texto (str): O texto/descrição da tarefa a ser adicionada
    
    Retorna:
        dict: O dicionário da tarefa recém-criada com id, texto e completa
    """
    global proximo_id, tarefas
    # Cria um dicionário representando a nova tarefa
    tarefa = {
        'id': proximo_id,
        'texto': texto,
        'completa': False
    }
    # Adiciona a tarefa à lista global
    tarefas.append(tarefa)
    # Incrementa o contador para o próximo ID
    proximo_id += 1
    # Salva as tarefas no arquivo JSON
    salvar_tarefas()
    return tarefa


def completar_tarefa(id):
    """
    Marca uma tarefa como completa baseado no seu ID.
    
    Esta função percorre a lista de tarefas procurando pelo ID fornecido.
    Quando encontra, altera o status 'completa' para True.
    
    Parâmetros:
        id (int): O ID da tarefa que deve ser marcada como completa
    
    Retorna:
        dict ou None: Retorna o dicionário da tarefa se encontrada e marcada,
                     ou None se a tarefa não for encontrada
    """
    global tarefas
    # Percorre todas as tarefas procurando pelo ID
    for tarefa in tarefas:
        if tarefa['id'] == id:
            # Marca a tarefa como completa
            tarefa['completa'] = True
            # Salva as tarefas no arquivo JSON
            salvar_tarefas()
            return tarefa
    # Retorna None se a tarefa não foi encontrada
    return None


def excluir_tarefa(id):
    """
    Exclui uma tarefa da lista baseado no seu ID.
    
    Esta função percorre a lista de tarefas procurando pelo ID fornecido.
    Quando encontra, remove a tarefa da lista.
    
    Parâmetros:
        id (int): O ID da tarefa que deve ser excluída
    
    Retorna:
        bool: Retorna True se a tarefa foi encontrada e excluída,
              ou False se a tarefa não foi encontrada
    """
    global tarefas
    # Percorre todas as tarefas procurando pelo ID
    for i, tarefa in enumerate(tarefas):
        if tarefa['id'] == id:
            # Remove a tarefa da lista
            tarefas.pop(i)
            # Salva as tarefas no arquivo JSON
            salvar_tarefas()
            return True
    # Retorna False se a tarefa não foi encontrada
    return False


def editar_tarefa(id, novo_texto):
    """
    Edita o texto de uma tarefa baseado no seu ID.
    
    Esta função percorre a lista de tarefas procurando pelo ID fornecido.
    Quando encontra, atualiza o texto da tarefa.
    
    Parâmetros:
        id (int): O ID da tarefa que deve ser editada
        novo_texto (str): O novo texto para a tarefa
    
    Retorna:
        dict ou None: Retorna o dicionário da tarefa se encontrada e editada,
                     ou None se a tarefa não for encontrada
    """
    global tarefas
    # Percorre todas as tarefas procurando pelo ID
    for tarefa in tarefas:
        if tarefa['id'] == id:
            # Atualiza o texto da tarefa
            tarefa['texto'] = novo_texto
            # Salva as tarefas no arquivo JSON
            salvar_tarefas()
            return tarefa
    # Retorna None se a tarefa não foi encontrada
    return None


@app.route('/')
def exibir_tarefas():
    """
    Rota principal que exibe a página inicial com todas as tarefas.
    
    Esta função renderiza o template HTML (index.html) que mostra:
    - Lista de todas as tarefas cadastradas com seus status (Completa/Pendente)
    - Link para completar tarefas pendentes
    - Formulário para adicionar novas tarefas
    
    Retorna:
        str: HTML renderizado do template index.html com a lista de tarefas
    """
    # Renderiza o template index.html passando a lista de tarefas como contexto
    return render_template('index.html', tarefas=tarefas)


@app.route('/adicionar')
def adicionar():
    """
    Rota que processa a adição de uma nova tarefa.
    
    Esta função recebe o parâmetro 'texto' da URL (via método GET),
    valida se não está vazio, chama a função adicionar_tarefa() e
    redireciona para a página principal.
    
    Retorna:
        redirect: Redireciona para a rota principal após adicionar a tarefa
    """
    # Obtém o parâmetro 'texto' da URL (query string)
    texto = request.args.get('texto', '')
    # Verifica se o texto não está vazio
    if texto:
        # Chama a função para adicionar a tarefa à lista
        adicionar_tarefa(texto)
        # Redireciona para a página principal para exibir a lista atualizada
        return redirect(url_for('exibir_tarefas'))
    # Se o texto estiver vazio, também redireciona (pode adicionar tratamento de erro depois)
    return redirect(url_for('exibir_tarefas'))


@app.route('/completar/<int:id>')
def completar(id):
    """
    Rota que processa a marcação de uma tarefa como completa.
    
    Esta função recebe o ID da tarefa pela URL, chama completar_tarefa()
    para marcar como completa e redireciona para a página principal.
    
    Parâmetros:
        id (int): O ID da tarefa a ser completada (vem da URL)
    
    Retorna:
        redirect: Redireciona para a rota principal após completar a tarefa
    """
    # Chama a função para marcar a tarefa como completa
    tarefa = completar_tarefa(id)
    # Redireciona para a página principal para exibir a lista atualizada
    # (independente de ter encontrado ou não a tarefa)
    return redirect(url_for('exibir_tarefas'))


@app.route('/excluir/<int:id>')
def excluir(id):
    """
    Rota que processa a exclusão de uma tarefa.
    
    Esta função recebe o ID da tarefa pela URL, chama excluir_tarefa()
    para remover a tarefa e redireciona para a página principal.
    
    Parâmetros:
        id (int): O ID da tarefa a ser excluída (vem da URL)
    
    Retorna:
        redirect: Redireciona para a rota principal após excluir a tarefa
    """
    # Chama a função para excluir a tarefa
    excluir_tarefa(id)
    # Redireciona para a página principal para exibir a lista atualizada
    return redirect(url_for('exibir_tarefas'))


@app.route('/editar', methods=['GET', 'POST'])
def editar():
    """
    Rota que processa a edição do texto de uma tarefa.
    
    Esta função recebe o ID e o novo texto via GET ou POST,
    chama editar_tarefa() para atualizar a tarefa e redireciona
    para a página principal.
    
    Retorna:
        redirect: Redireciona para a rota principal após editar a tarefa
    """
    # Obtém o ID e o novo texto da requisição
    if request.method == 'POST':
        id = request.form.get('id', type=int)
        novo_texto = request.form.get('texto', '')
    else:
        id = request.args.get('id', type=int)
        novo_texto = request.args.get('texto', '')
    
    # Verifica se ambos os parâmetros foram fornecidos
    if id and novo_texto:
        # Chama a função para editar a tarefa
        editar_tarefa(id, novo_texto)
    
    # Redireciona para a página principal para exibir a lista atualizada
    return redirect(url_for('exibir_tarefas'))


# Bloco que executa o servidor Flask quando o script é executado diretamente
if __name__ == '__main__':
    # Carrega as tarefas do arquivo JSON ao iniciar a aplicação
    carregar_tarefas()
    # Inicia o servidor Flask com:
    # - debug=True: ativa modo debug (recarrega automaticamente e mostra erros detalhados)
    # - host='0.0.0.0': permite acesso de qualquer IP na rede
    # - port=5000: define a porta 5000 para o servidor
    app.run(debug=True, host='0.0.0.0', port=5000)


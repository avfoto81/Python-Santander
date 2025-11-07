"""
Analisador de Dados CSV

Este módulo fornece funcionalidades para:
- Ler arquivos CSV com detecção automática de delimitadores
- Calcular estatísticas (média, mediana, desvio padrão)
- Gerar gráficos de dispersão e de barras
- Interface gráfica (GUI) para análise interativa de dados

Autor: André Luiz com Python Santander
"""

import csv

# ============================================================================
# SEÇÃO: Funções de Geração de Gráficos
# ============================================================================

def plot_disp(colunas, x_col, y_col):
    """
    Gera um gráfico de dispersão (scatter plot) entre duas colunas.
    
    Esta função cria um gráfico de dispersão para visualizar a relação
    entre duas variáveis numéricas do conjunto de dados.
    
    Args:
        colunas (dict): Dicionário com nome das colunas como chaves e listas
                       de valores numéricos como valores.
        x_col (str): Nome da coluna a ser exibida no eixo X.
        y_col (str): Nome da coluna a ser exibida no eixo Y.
    
    Raises:
        RuntimeError: Se o matplotlib não estiver instalado.
        ValueError: Se uma ou ambas as colunas não existirem ou se tiverem
                   tamanhos diferentes.
    
    Returns:
        None: A função exibe o gráfico em uma janela separada.
    """
    try:
        import matplotlib
        matplotlib.use('TkAgg')
        import matplotlib.pyplot as plt
    except ImportError:
        raise RuntimeError("matplotlib não está instalado. Instale-o para gerar gráficos (pip install matplotlib).")

    if x_col not in colunas or y_col not in colunas:
        raise ValueError("Uma ou ambas as colunas não existem.")
    if len(colunas[x_col]) != len(colunas[y_col]):
        raise ValueError("As colunas selecionadas não têm o mesmo número de valores.")

    plt.scatter(colunas[x_col], colunas[y_col])
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f"Gráfico de Dispersão: {x_col} vs {y_col}")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_barras_medias(colunas):
    """
    Gera um gráfico de barras comparando as médias de todas as colunas.
    
    Esta função calcula a média de cada coluna numérica e exibe os resultados
    em um gráfico de barras, permitindo comparar visualmente as médias entre
    diferentes colunas do conjunto de dados.
    
    Args:
        colunas (dict): Dicionário com nome das colunas como chaves e listas
                       de valores numéricos como valores.
    
    Raises:
        RuntimeError: Se o matplotlib não estiver instalado.
    
    Returns:
        None: A função exibe o gráfico em uma janela separada.
    """
    try:
        import matplotlib
        matplotlib.use('TkAgg')
        import matplotlib.pyplot as plt
    except ImportError:
        raise RuntimeError("matplotlib não está instalado. Instale-o para gerar gráficos (pip install matplotlib).")

    medias = {nome: media(valores) for nome, valores in colunas.items()}
    nomes = list(medias.keys())
    valores_medias = list(medias.values())

    plt.bar(nomes, valores_medias, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'][:len(nomes)])
    plt.xlabel("Colunas")
    plt.ylabel("Média")
    plt.title("Gráfico de Barras - Média por Coluna")
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.show()

def plot_barras_coluna(colunas, coluna_escolhida):
    """
    Gera um gráfico de barras exibindo todos os valores de uma coluna específica.
    
    Esta função cria um gráfico de barras onde cada barra representa um valor
    individual da coluna selecionada, útil para visualizar a distribuição
    completa dos dados de uma única variável.
    
    Args:
        colunas (dict): Dicionário com nome das colunas como chaves e listas
                       de valores numéricos como valores.
        coluna_escolhida (str): Nome da coluna cujos valores serão exibidos.
    
    Raises:
        RuntimeError: Se o matplotlib não estiver instalado.
        ValueError: Se a coluna especificada não existir.
    
    Returns:
        None: A função exibe o gráfico em uma janela separada.
    """
    try:
        import matplotlib
        matplotlib.use('TkAgg')
        import matplotlib.pyplot as plt
    except ImportError:
        raise RuntimeError("matplotlib não está instalado. Instale-o para gerar gráficos (pip install matplotlib).")

    if coluna_escolhida not in colunas:
        raise ValueError("Coluna não encontrada.")

    valores = colunas[coluna_escolhida]
    indices = range(len(valores))

    plt.bar(indices, valores, color='steelblue', alpha=0.7)
    plt.xlabel("Índice")
    plt.ylabel(coluna_escolhida)
    plt.title(f"Gráfico de Barras - {coluna_escolhida}")
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.show()

# ============================================================================
# SEÇÃO: Funções de Leitura e Processamento de Dados
# ============================================================================

def ler_csv(caminho_arquivo):
    """
    Lê um arquivo CSV e retorna os dados como uma lista de dicionários.
    
    Esta função realiza leitura inteligente de arquivos CSV com as seguintes
    capacidades:
    - Detecção automática de delimitador (vírgula ou ponto e vírgula)
    - Detecção automática de presença de cabeçalho
    - Criação automática de nomes de colunas se não houver cabeçalho
    - Remoção de colunas vazias
    
    Args:
        caminho_arquivo (str): Caminho completo ou relativo para o arquivo CSV.
    
    Returns:
        list: Lista de dicionários, onde cada dicionário representa uma linha
              do CSV com as chaves sendo os nomes das colunas.
    
    Example:
        >>> dados = ler_csv("dados.csv")
        >>> print(dados[0])
        {'Coluna_1': '23,00', 'Coluna_2': '101,00'}
    """
    with open(caminho_arquivo, newline='', encoding='utf-8') as csvfile:
        # Lê a primeira linha para detectar delimitador e verificar se há cabeçalho
        primeira_linha = csvfile.readline().strip()
        csvfile.seek(0)  # Volta ao início do arquivo para ler novamente
        
        # Detecta o delimitador: ponto e vírgula (formato brasileiro/Europeu) ou vírgula
        if ';' in primeira_linha:
            delimitador = ';'
        else:
            delimitador = ','
        
        # Verifica se a primeira linha parece ser numérica (dados) ou texto (cabeçalho)
        primeira_linha_split = primeira_linha.split(delimitador)
        tem_cabecalho = True
        
        # Se todos os valores da primeira linha forem numéricos, não há cabeçalho
        try:
            for valor in primeira_linha_split:
                if valor.strip():  # Ignora valores vazios
                    float(valor.replace(',', '.'))  # Tenta converter (suporta formato brasileiro)
            # Se chegou aqui, todos são numéricos - não há cabeçalho
            tem_cabecalho = False
        except (ValueError, AttributeError):
            # Se não conseguir converter, provavelmente há cabeçalho textual
            tem_cabecalho = True
        
        # Cria o leitor CSV com ou sem cabeçalho
        if tem_cabecalho:
            # Usa os cabeçalhos do arquivo
            leitor = csv.DictReader(csvfile, delimiter=delimitador)
        else:
            # Cria nomes genéricos para as colunas (Coluna_1, Coluna_2, etc.)
            num_colunas = len([v for v in primeira_linha_split if v.strip()])
            leitor = csv.DictReader(csvfile, delimiter=delimitador,
                                   fieldnames=[f'Coluna_{i+1}' for i in range(num_colunas)])
        
        # Processa cada linha do arquivo
        dados = []
        for linha in leitor:
            # Remove colunas vazias (chaves None ou vazias)
            linha_limpa = {k: v for k, v in linha.items() 
                          if k is not None and (isinstance(k, str) and k.strip())}
            if linha_limpa:  # Só adiciona se houver dados válidos
                dados.append(linha_limpa)
    return dados

def converter_colunas_para_float(dados):
    """
    Converte colunas de dados texto para valores numéricos (float).
    
    Esta função processa os dados lidos do CSV e converte apenas as colunas
    que contêm valores numéricos válidos. Suporta formato brasileiro de números
    (vírgula como separador decimal) e ignora valores não numéricos.
    
    Args:
        dados (list): Lista de dicionários retornada pela função ler_csv().
    
    Returns:
        dict: Dicionário onde as chaves são nomes de colunas numéricas e os
              valores são listas de números (float). Colunas não numéricas
              são automaticamente excluídas.
    
    Example:
        >>> dados = [{'Coluna_1': '23,50', 'Coluna_2': '101,00'}]
        >>> colunas = converter_colunas_para_float(dados)
        >>> print(colunas)
        {'Coluna_1': [23.5], 'Coluna_2': [101.0]}
    """
    colunas = {}
    # Itera sobre todas as colunas presentes nos dados
    for chave in dados[0]:
        valores_convertidos = []
        # Tenta converter cada valor da coluna para float
        for linha in dados:
            valor = linha[chave].strip() if linha[chave] else ''
            if valor:
                try:
                    # Converte vírgula para ponto (formato brasileiro: 23,50 -> 23.50)
                    valor_float = float(valor.replace(',', '.'))
                    valores_convertidos.append(valor_float)
                except ValueError:
                    # Se não conseguir converter, ignora esse valor específico
                    continue
        # Só adiciona a coluna se houver pelo menos um valor válido convertido
        if valores_convertidos:
            colunas[chave] = valores_convertidos
    return colunas

# ============================================================================
# SEÇÃO: Funções de Cálculo Estatístico
# ============================================================================

def media(valores):
    """
    Calcula a média aritmética de uma lista de valores numéricos.
    
    A média é calculada como a soma de todos os valores dividida pela
    quantidade de valores. Retorna 0 se a lista estiver vazia.
    
    Args:
        valores (list): Lista de números (int ou float).
    
    Returns:
        float: Média aritmética dos valores. Retorna 0 se a lista estiver vazia.
    
    Example:
        >>> media([1, 2, 3, 4, 5])
        3.0
        >>> media([23.5, 24.0, 25.5])
        24.333333333333332
    """
    return sum(valores) / len(valores) if valores else 0

def mediana(valores):
    """
    Calcula a mediana de uma lista de valores numéricos.
    
    A mediana é o valor que divide a lista ordenada ao meio. Se a quantidade
    de elementos for ímpar, retorna o valor central. Se for par, retorna a
    média dos dois valores centrais.
    
    Args:
        valores (list): Lista de números (int ou float).
    
    Returns:
        float: Mediana dos valores. Retorna 0 se a lista estiver vazia.
    
    Example:
        >>> mediana([1, 3, 5, 7, 9])  # Quantidade ímpar
        5.0
        >>> mediana([1, 2, 3, 4])     # Quantidade par
        2.5
    """
    n = len(valores)
    valores_ordenados = sorted(valores)
    if n == 0:
        return 0
    elif n % 2 == 1:
        # Se a quantidade é ímpar, retorna o valor central
        return valores_ordenados[n // 2]
    else:
        # Se a quantidade é par, retorna a média dos dois valores centrais
        return (valores_ordenados[n // 2 - 1] + valores_ordenados[n // 2]) / 2

def desvio_padrao(valores):
    """
    Calcula o desvio padrão amostral de uma lista de valores numéricos.
    
    O desvio padrão mede a dispersão dos dados em relação à média. Esta
    função utiliza a fórmula do desvio padrão amostral (n-1 no denominador).
    
    Args:
        valores (list): Lista de números (int ou float).
    
    Returns:
        float: Desvio padrão amostral. Retorna 0 se a lista tiver menos de
               2 elementos ou estiver vazia.
    
    Example:
        >>> desvio_padrao([1, 2, 3, 4, 5])
        1.5811388300841898
    """
    if not valores or len(valores) < 2:
        return 0
    # Calcula a média dos valores
    m = media(valores)
    # Calcula o desvio padrão amostral: sqrt(soma((x - média)²) / (n - 1))
    return (sum((x - m) ** 2 for x in valores) / (len(valores)-1)) ** 0.5

def mostrar_estatisticas(colunas):
    """
    Exibe estatísticas descritivas para cada coluna numérica.
    
    Esta função calcula e imprime a média, mediana e desvio padrão para
    cada coluna numérica presente no dicionário de colunas. Útil para
    análise rápida dos dados via terminal.
    
    Args:
        colunas (dict): Dicionário com nome das colunas como chaves e listas
                       de valores numéricos como valores.
    
    Returns:
        None: A função apenas imprime as estatísticas no console.
    
    Example:
        >>> colunas = {'Coluna_1': [1, 2, 3, 4, 5], 'Coluna_2': [10, 20, 30]}
        >>> mostrar_estatisticas(colunas)
        Coluna: Coluna_1
          Média: 3.0000
          Mediana: 3.0000
          Desvio padrão: 1.5811
        ------------------------------
        Coluna: Coluna_2
          Média: 20.0000
          Mediana: 20.0000
          Desvio padrão: 10.0000
        ------------------------------
    """
    for nome, valores in colunas.items():
        print(f"Coluna: {nome}")
        print(f"  Média: {media(valores):.4f}")
        print(f"  Mediana: {mediana(valores):.4f}")
        print(f"  Desvio padrão: {desvio_padrao(valores):.4f}")
        print("-" * 30)

# ============================================================================
# SEÇÃO: Função de Geração de Gráficos (Modo Console - Deprecada)
# ============================================================================

def gerar_grafico(colunas):
    """
    Gera gráficos interativamente via terminal (modo console).
    
    NOTA: Esta função está mantida para compatibilidade, mas o modo principal
    de uso agora é através da interface gráfica (GUI). Esta função permite
    escolher entre gráfico de dispersão e gráfico de barras através de
    interação via terminal.
    
    Args:
        colunas (dict): Dicionário com nome das colunas como chaves e listas
                       de valores numéricos como valores.
    
    Returns:
        None: A função exibe gráficos em janelas separadas ou imprime mensagens
              de erro no console.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib não está instalado. Instale-o para gerar gráficos (pip install matplotlib).")
        return

    nomes_colunas = list(colunas.keys())
    print("\nColunas numéricas disponíveis:", nomes_colunas)
    print("\nTipos de gráfico disponíveis:")
    print("1 - Gráfico de Dispersão")
    print("2 - Gráfico de Barras")
    
    tipo_grafico = input("\nEscolha o tipo de gráfico (1 ou 2): ").strip()
    
    if tipo_grafico == "1":
        # Gráfico de Dispersão
        x_col = input("Digite o nome da coluna para o eixo X: ")
        y_col = input("Digite o nome da coluna para o eixo Y: ")
        if x_col not in colunas or y_col not in colunas:
            print("Uma ou ambas as colunas não existem.")
            return

        if len(colunas[x_col]) != len(colunas[y_col]):
            print("As colunas selecionadas não têm o mesmo número de valores.")
            return

        plt.scatter(colunas[x_col], colunas[y_col])
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title(f"Gráfico de Dispersão: {x_col} vs {y_col}")
        plt.grid(True, alpha=0.3)
        plt.show()
        
    elif tipo_grafico == "2":
        # Gráfico de Barras
        print("\nOpções para gráfico de barras:")
        print("1 - Comparar todas as colunas (média de cada coluna)")
        print("2 - Exibir uma coluna específica")
        
        opcao = input("Escolha uma opção (1 ou 2): ").strip()
        
        if opcao == "1":
            # Gráfico de barras comparando médias de todas as colunas
            medias = {nome: media(valores) for nome, valores in colunas.items()}
            nomes = list(medias.keys())
            valores_medias = list(medias.values())
            
            plt.bar(nomes, valores_medias, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'])
            plt.xlabel("Colunas")
            plt.ylabel("Média")
            plt.title("Gráfico de Barras - Média por Coluna")
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            plt.show()
            
        elif opcao == "2":
            # Gráfico de barras de uma coluna específica
            coluna_escolhida = input("Digite o nome da coluna: ")
            if coluna_escolhida not in colunas:
                print("Coluna não encontrada.")
                return
            
            valores = colunas[coluna_escolhida]
            indices = range(len(valores))
            
            plt.bar(indices, valores, color='steelblue', alpha=0.7)
            plt.xlabel("Índice")
            plt.ylabel(coluna_escolhida)
            plt.title(f"Gráfico de Barras - {coluna_escolhida}")
            plt.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            plt.show()
        else:
            print("Opção inválida.")
    else:
        print("Tipo de gráfico inválido.")

# ============================================================================
# SEÇÃO: Interface Gráfica (GUI)
# ============================================================================

def iniciar_gui():
    """
    Inicia a interface gráfica (GUI) para análise interativa de dados CSV.
    
    Esta função cria uma janela gráfica usando Tkinter que permite:
    - Selecionar e carregar arquivos CSV
    - Visualizar estatísticas descritivas (média, mediana, desvio padrão)
    - Gerar gráficos de dispersão e de barras de forma interativa
    - Selecionar colunas através de menus dropdown (Combobox)
    
    A interface é composta por:
    - Campo de seleção de arquivo com botão "Procurar..."
    - Botão "Carregar" para processar o arquivo selecionado
    - Área de texto para exibir estatísticas
    - Controles para seleção de colunas e geração de gráficos
    
    Returns:
        None: A função executa o loop principal da interface gráfica até
              que a janela seja fechada.
    
    Raises:
        Exception: Se houver problemas ao importar tkinter ou suas dependências.
    """
    # Importa as bibliotecas necessárias para a interface gráfica
    try:
        import tkinter as tk
        from tkinter import ttk, filedialog, messagebox
    except Exception as e:
        print(f"Falha ao iniciar GUI: {e}")
        return

    # Cria a janela principal da aplicação
    app = tk.Tk()
    app.title("Analisador de Dados CSV")
    app.geometry("720x520")

    # Estado da aplicação: armazena os dados carregados e colunas processadas
    dados_estado = {"dados": None, "colunas": None}

    # ========================================================================
    # Frame superior: Seleção de arquivo
    # ========================================================================
    frame_top = ttk.Frame(app, padding=10)
    frame_top.pack(fill=tk.X)

    # Variável para armazenar o caminho do arquivo
    caminho_var = tk.StringVar()
    ttk.Label(frame_top, text="Arquivo CSV:").pack(side=tk.LEFT)
    entrada = ttk.Entry(frame_top, textvariable=caminho_var, width=60)
    entrada.pack(side=tk.LEFT, padx=5)

    def escolher_arquivo():
        """Abre diálogo para selecionar arquivo CSV."""
        caminho = filedialog.askopenfilename(filetypes=[("CSV", "*.csv"), ("Todos", "*.*")])
        if caminho:
            caminho_var.set(caminho)

    ttk.Button(frame_top, text="Procurar...", command=escolher_arquivo).pack(side=tk.LEFT)

    # ========================================================================
    # Frame central: Área de exibição de estatísticas
    # ========================================================================
    frame_mid = ttk.Frame(app, padding=10)
    frame_mid.pack(fill=tk.BOTH, expand=True)

    texto = tk.Text(frame_mid, height=12)
    texto.pack(fill=tk.BOTH, expand=True)

    # ========================================================================
    # Frame inferior: Opções de gráficos
    # ========================================================================
    frame_opts = ttk.Frame(app, padding=10)
    frame_opts.pack(fill=tk.X)

    # Comboboxes para seleção de colunas (serão preenchidos após carregar dados)
    colunas_combo_x = ttk.Combobox(frame_opts, state="readonly")
    colunas_combo_y = ttk.Combobox(frame_opts, state="readonly")
    colunas_combo_coluna = ttk.Combobox(frame_opts, state="readonly")

    def atualizar_combos(nomes):
        """
        Atualiza os menus dropdown (Combobox) com os nomes das colunas disponíveis.
        
        Args:
            nomes (list): Lista com os nomes das colunas numéricas encontradas.
        """
        colunas_combo_x["values"] = nomes
        colunas_combo_y["values"] = nomes
        colunas_combo_coluna["values"] = nomes
        # Seleciona automaticamente os primeiros valores
        if nomes:
            colunas_combo_x.current(0)
            colunas_combo_y.current(min(1, len(nomes)-1))  # Segunda coluna, se existir
            colunas_combo_coluna.current(0)

    def carregar():
        """
        Carrega e processa o arquivo CSV selecionado.
        
        Esta função lê o arquivo CSV, converte as colunas numéricas,
        exibe as estatísticas na área de texto e atualiza os menus
        de seleção de colunas para os gráficos.
        """
        caminho = caminho_var.get().strip()
        if not caminho:
            messagebox.showwarning("Aviso", "Escolha um arquivo CSV.")
            return
        try:
            # Lê o arquivo CSV e converte para formato numérico
            dados = ler_csv(caminho)
            colunas = converter_colunas_para_float(dados)
            if not colunas:
                messagebox.showinfo("Informação", "Não foram encontradas colunas numéricas no arquivo.")
                return
            
            # Armazena os dados no estado da aplicação
            dados_estado["dados"] = dados
            dados_estado["colunas"] = colunas

            # Exibe estatísticas na área de texto
            texto.delete("1.0", tk.END)
            for nome, valores in colunas.items():
                texto.insert(tk.END, f"Coluna: {nome}\n")
                texto.insert(tk.END, f"  Média: {media(valores):.4f}\n")
                texto.insert(tk.END, f"  Mediana: {mediana(valores):.4f}\n")
                texto.insert(tk.END, f"  Desvio padrão: {desvio_padrao(valores):.4f}\n")
                texto.insert(tk.END, "-" * 30 + "\n")

            # Atualiza os menus de seleção de colunas
            atualizar_combos(list(colunas.keys()))
        except FileNotFoundError:
            messagebox.showerror("Erro", f"Arquivo '{caminho}' não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    ttk.Button(frame_top, text="Carregar", command=carregar).pack(side=tk.LEFT, padx=5)

    # ========================================================================
    # Funções wrapper para tratamento de erros nos gráficos
    # ========================================================================
    def gerar_dispersao():
        """
        Gera gráfico de dispersão com tratamento de erros para a interface gráfica.
        
        Esta função verifica se os dados foram carregados e tenta gerar o gráfico
        de dispersão usando as colunas selecionadas nos menus dropdown. Exibe
        mensagens de erro apropriadas em caso de falha.
        
        Returns:
            None: A função exibe o gráfico ou uma mensagem de erro.
        """
        if dados_estado["colunas"] is None:
            messagebox.showwarning("Aviso", "Carregue um arquivo CSV primeiro.")
            return
        try:
            plot_disp(dados_estado["colunas"], colunas_combo_x.get(), colunas_combo_y.get())
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar gráfico de dispersão: {e}")

    def gerar_barras_medias():
        """
        Gera gráfico de barras de médias com tratamento de erros para a interface gráfica.
        
        Esta função verifica se os dados foram carregados e gera um gráfico de barras
        comparando as médias de todas as colunas numéricas. Exibe mensagens de erro
        apropriadas em caso de falha.
        
        Returns:
            None: A função exibe o gráfico ou uma mensagem de erro.
        """
        if dados_estado["colunas"] is None:
            messagebox.showwarning("Aviso", "Carregue um arquivo CSV primeiro.")
            return
        try:
            plot_barras_medias(dados_estado["colunas"])
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar gráfico de barras: {e}")

    def gerar_barras_coluna():
        """
        Gera gráfico de barras de uma coluna específica com tratamento de erros.
        
        Esta função verifica se os dados foram carregados e gera um gráfico de barras
        exibindo todos os valores da coluna selecionada no menu dropdown. Exibe
        mensagens de erro apropriadas em caso de falha.
        
        Returns:
            None: A função exibe o gráfico ou uma mensagem de erro.
        """
        if dados_estado["colunas"] is None:
            messagebox.showwarning("Aviso", "Carregue um arquivo CSV primeiro.")
            return
        try:
            plot_barras_coluna(dados_estado["colunas"], colunas_combo_coluna.get())
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar gráfico de barras: {e}")

    # ========================================================================
    # Controles de gráficos: Linha 1 - Gráfico de Dispersão
    # ========================================================================
    linha1 = ttk.Frame(frame_opts)
    linha1.pack(fill=tk.X, pady=4)
    ttk.Label(linha1, text="X:").pack(side=tk.LEFT)
    colunas_combo_x.pack(side=tk.LEFT, padx=5)
    ttk.Label(linha1, text="Y:").pack(side=tk.LEFT)
    colunas_combo_y.pack(side=tk.LEFT, padx=5)
    ttk.Button(linha1, text="Dispersão", command=gerar_dispersao).pack(side=tk.LEFT, padx=10)

    # ========================================================================
    # Controles de gráficos: Linha 2 - Gráficos de Barras
    # ========================================================================
    linha2 = ttk.Frame(frame_opts)
    linha2.pack(fill=tk.X, pady=4)
    # Botão para gráfico de barras com médias de todas as colunas
    ttk.Button(linha2, text="Barras (médias)", command=gerar_barras_medias).pack(side=tk.LEFT)

    # Controles para gráfico de barras de uma coluna específica
    ttk.Label(linha2, text="Coluna:").pack(side=tk.LEFT, padx=(12,4))
    colunas_combo_coluna.pack(side=tk.LEFT)
    ttk.Button(linha2, text="Barras (coluna)", command=gerar_barras_coluna).pack(side=tk.LEFT, padx=10)

    # Inicia o loop principal da interface gráfica
    app.mainloop()

# ============================================================================
# SEÇÃO: Função Principal
# ============================================================================

def main():
    """
    Função principal do programa.
    
    Esta função é o ponto de entrada do programa e inicia a interface gráfica
    para análise de dados CSV. Quando o script é executado diretamente,
    esta função é chamada automaticamente.
    
    Returns:
        None: A função inicia a GUI e mantém a aplicação rodando até que
              o usuário feche a janela.
    """
    # Inicia a interface gráfica ao invés de CLI
    iniciar_gui()

if __name__ == "__main__":
    # Executa a função principal quando o script é chamado diretamente
    main()

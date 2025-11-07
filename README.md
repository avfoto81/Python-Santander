# Analisador de Dados CSV

Aplicação em Python que lê arquivos CSV, calcula estatísticas básicas (média, mediana e desvio padrão) e oferece visualizações interativas em gráficos de dispersão e barras. Uma interface gráfica intuitiva, construída com Tkinter, facilita o carregamento de dados e a geração dos gráficos.

## Recursos Principais
- Detecção automática do delimitador (`;` ou `,`) e da presença de cabeçalho.
- Conversão inteligente de números em formato brasileiro (vírgula como separador decimal).
- Cálculo de média, mediana e desvio padrão para cada coluna numérica.
- Interface gráfica (GUI) com seleção de arquivo, visualização de estatísticas e geração de gráficos.
- Três tipos de visualização:
  - Gráfico de dispersão entre duas colunas.
  - Gráfico de barras comparando a média de todas as colunas.
  - Gráfico de barras com todos os valores de uma coluna específica.

## Pré-requisitos
- Python 3.10 ou superior (testado com Python 3.13).
- Ambiente virtual (recomendado).
- Sistema operacional Windows (testado) – outros sistemas podem exigir ajustes mínimos.

## Instalação
```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd <pasta-do-repositorio>

# 2. Crie e ative o ambiente virtual (Windows)
python -m venv venv
venv\Scripts\activate

# 2.1 (Linux/Mac, caso utilize)
python3 -m venv venv
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt
```

> Caso o arquivo `requirements.txt` ainda não exista, instale manualmente:
```bash
pip install matplotlib
```

## Uso
```bash
# Com o ambiente virtual ativo, execute o aplicativo
python analizar_dados.py
```

### Passos na Interface Gráfica
1. Clique em **“Procurar…”** e selecione o arquivo CSV.
2. Pressione **“Carregar”** para exibir as estatísticas no painel central.
3. Escolha:
   - **Dispersão**: selecione duas colunas (X e Y) e gere o gráfico.
   - **Barras (médias)**: compare as médias de todas as colunas.
   - **Barras (coluna)**: visualize os valores de uma coluna específica.

Os gráficos são exibidos em janelas separadas utilizando `matplotlib`.

## Formato de Dados Recomendado
- Arquivos `.csv` com colunas numéricas.
- Aceita separador por vírgula ou ponto e vírgula.
- Valores numéricos com vírgula decimal serão convertidos automaticamente.
- Caso não exista cabeçalho, o programa cria nomes genéricos (`Coluna_1`, `Coluna_2`, ...).

## Estrutura do Projeto
```
analizar_dados.py   # Código principal com GUI e funções auxiliares
README.md           # Este arquivo
venv/               # Ambiente virtual (opcional, não incluído no controle de versão)
```

## Autor
Projeto desenvolvido por **André Luiz** com base no curso **Santander one Academy**.



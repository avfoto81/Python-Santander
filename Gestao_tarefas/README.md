# 📋 Gerenciador de Tarefas

Uma aplicação web simples para gerenciar tarefas, desenvolvida com Flask (Python) e HTML/CSS/JavaScript. Permite adicionar, editar, completar e excluir tarefas, com persistência de dados em arquivo JSON.

## 🚀 Funcionalidades

- ✅ **Adicionar tarefas**: Crie novas tarefas com descrição personalizada
- ✅ **Completar tarefas**: Marque tarefas como concluídas
- ✅ **Editar tarefas**: Modifique o texto de tarefas existentes
- ✅ **Excluir tarefas**: Remova tarefas da lista
- ✅ **Persistência**: Dados salvos automaticamente em arquivo JSON
- ✅ **Interface moderna**: Design responsivo e intuitivo

## 📦 Requisitos

- Python 3.7 ou superior
- Flask 3.0.0 ou superior

## 🔧 Instalação

1. Clone ou baixe o projeto
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

Ou instale o Flask diretamente:

```bash
pip install Flask
```

## ▶️ Como Executar

1. Navegue até a pasta do projeto:

```bash
cd Gestao_tarefas
```

2. Execute o aplicativo:

```bash
python app.py
```

3. Acesse no navegador:

```
http://localhost:5000
ou
http://127.0.0.1:5000
```

## 📁 Estrutura do Projeto

```
Gestao_tarefas/
├── app.py                 # Código principal da aplicação Flask
├── templates/
│   └── index.html        # Template HTML da interface
├── tarefas.json          # Arquivo de persistência (criado automaticamente)
├── requirements.txt      # Dependências do projeto
├── .gitignore           # Arquivos ignorados pelo Git
└── README.md            # Este arquivo
```

## 📝 Estrutura do Código (app.py)

### Variáveis Globais

- `tarefas`: Lista que armazena todas as tarefas (cada tarefa é um dicionário com `id`, `texto` e `completa`)
- `proximo_id`: Contador para gerar IDs únicos e incrementais
- `ARQUIVO_JSON`: Nome do arquivo JSON para persistência (`tarefas.json`)

### Funções de Persistência

- **`carregar_tarefas()`**: Carrega as tarefas do arquivo JSON ao iniciar a aplicação
- **`salvar_tarefas()`**: Salva as tarefas no arquivo JSON após cada operação

### Funções de Gerenciamento

- **`adicionar_tarefa(texto)`**: Cria uma nova tarefa com ID único e status pendente
- **`completar_tarefa(id)`**: Marca uma tarefa como completa pelo ID
- **`editar_tarefa(id, novo_texto)`**: Atualiza o texto de uma tarefa
- **`excluir_tarefa(id)`**: Remove uma tarefa da lista

### Rotas Flask

- **`/`**: Página principal que exibe todas as tarefas
- **`/adicionar`**: Processa a adição de nova tarefa (método GET)
- **`/completar/<id>`**: Marca uma tarefa como completa
- **`/editar`**: Processa a edição de uma tarefa (métodos GET e POST)
- **`/excluir/<id>`**: Remove uma tarefa da lista

## 💾 Persistência de Dados

As tarefas são salvas automaticamente no arquivo `tarefas.json` após cada operação (adicionar, editar, completar, excluir). O arquivo é criado automaticamente na primeira execução e carregado sempre que a aplicação é iniciada.

**Estrutura do JSON:**
```json
{
  "tarefas": [
    {
      "id": 1,
      "texto": "Exemplo de tarefa",
      "completa": false
    }
  ],
  "proximo_id": 2
}
```

## 🎨 Interface

A interface foi desenvolvida com:
- Design responsivo e moderno
- Gradientes e animações suaves
- Modal para edição de tarefas
- Confirmação antes de excluir tarefas
- Indicadores visuais de status (Completa/Pendente)

## 🔒 Segurança

⚠️ **Nota**: Esta é uma aplicação de desenvolvimento. Para uso em produção, considere:
- Implementar autenticação de usuários
- Usar um banco de dados adequado (SQLite, PostgreSQL, etc.)
- Adicionar validação e sanitização de dados
- Usar HTTPS
- Implementar rate limiting

## 📄 Licença

Este projeto é de código aberto e está disponível para uso educacional.

## 👨‍💻 Autor: André Luiz de Andrade Silva

Desenvolvido como projeto de aprendizado em Python e Flask com curso Santander Open Academy.

---

**Versão**: 1.0.0  
**Última atualização**: 2024


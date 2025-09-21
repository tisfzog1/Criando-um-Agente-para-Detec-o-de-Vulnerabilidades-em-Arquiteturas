# STRIDE Threat Model Analyzer

Este projeto realiza análise de ameaças baseada no modelo STRIDE usando FastAPI no backend, um frontend HTML/JS e visualização interativa com Cytoscape.js.

## Funcionalidades

- Formulário para envio de dados da aplicação e imagem de arquitetura.
- Backend FastAPI que utiliza Azure OpenAI para gerar o modelo de ameaças.
- Visualização do modelo de ameaças em tabela e grafo interativo (Cytoscape.js).
- Sugestões de melhoria automáticas para segurança.

## Como rodar localmente

### Pré-requisitos

- Python 3.10+
- Node.js (opcional, apenas para desenvolvimento frontend)
- Conta e chave do Azure OpenAI (com deployment ativo)
- Git

### Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/stride-threat-model.git
cd stride-threat-model
```

2. Instale as dependências do backend:

```bash
cd stride-demo/backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. Configure o arquivo `.env` com suas credenciais do Azure OpenAI:

```env
AZURE_OPENAI_KEY=coloque_sua_chave_aqui
AZURE_OPENAI_VERSION=2023-05-15
AZURE_OPENAI_ENDPOINT=https://seu-endpoint.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=nome_do_seu_deployment
```

4. Inicie o backend:

```bash
uvicorn main:app --reload
```

5. Abra o frontend:
   - Basta abrir o arquivo `stride-demo/frontend/index.html` no navegador.

## Estrutura do Projeto

```text
stride-demo/
  backend/
    main.py
    requirements.txt
    .env
  frontend/
    index.html
    script.js
    style.css
```text

## Tecnologias

- FastAPI
- Azure OpenAI
- Cytoscape.js
- HTML, CSS, JavaScript

## Licença

MIT

---

> Projeto desenvolvido para análise e visualização de ameaças STRIDE de forma interativa.

import os
import base64
import shutil
import tempfile
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from openai import AzureOpenAI

# 🔹 Carregar variáveis do .env
load_dotenv()

app = FastAPI()

# 🔹 Configuração do CORS (permite acesso do frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em produção, restringir ao domínio do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Cliente Azure OpenAI
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT")

@app.get("/")
def home():
    return {"status": "ok", "message": "API STRIDE rodando 🚀"}

# ==============================
# 📌 Endpoint de análise STRIDE
# ==============================

@app.post("/api/analise")
async def analisar_ameacas(
    image: UploadFile,
    tipo_app: str = Form(...),
    autenticacao: str = Form(...),
    internet: str = Form(...),
    dados_sensiveis: str = Form(...),
    descricao: str = Form(...)
):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            shutil.copyfileobj(image.file, tmp)
            tmp_path = tmp.name

        with open(tmp_path, "rb") as f:
            encoded_image = base64.b64encode(f.read()).decode("ascii")

        prompt = f"""
Haja como um especialista em cibersegurança com mais de 20 anos de experiência,
utilizando a metodologia de ameaças STRIDE para construir modelos de ameaça abrangentes
para uma ampla gama de aplicações. 

Sua tarefa é analisar o resumo do código e/ou o desenho de arquitetura fornecido
para produzir uma lista de ameaças específicas da aplicação.

Preste atenção especial no conteúdo do README, descrição da aplicação, detalhes técnicos e na imagem da arquitetura.

Para cada categoria do STRIDE:
- Spoofing (falsificação de identidade)
- Tampering (violação da integridade)
- Repudiation (não repúdio)
- Information disclosure (vazamento de informações)
- Denial of service (negação de serviço)
- Elevation of privilege (elevação de privilégios)

Liste múltiplas ameaças credíveis. Para cada ameaça, forneça uma situação plausível e o potencial impacto no contexto da aplicação.

Apresente a lista de ameaças no seguinte formato de tabela com as seguintes colunas, Ao fornecer os modelos e as respostas em JSON:
- JSON com a chave "stride_model"
- Um array de objetos, cada objeto contendo:

    - "stride_type": Tipo de ameaça (Spoofing, Tampering, etc.)
    - "scenario": Cenário plausível
    - "potential_impact": Impacto esperado
- Sugestões de melhoria para detalhar lacunas na descrição da aplicação, como arquiteturas, fluxos de autenticação, exposição à internet, dados sensíveis, etc.
- Não forneça recomendações genéricas de segurança, foque apenas no que ajudaria a criar um modelo de ameaças mais eficiente.
Ao fornecer o modelo de ameaça, utilize uma resposta em JSON com as chaves "threat_model" e "improvement_suggestions".
Em "threat_model", forneça um array de objetos, cada objeto contendo "stride_type", "scenario" e "potential_impact".

Informações da aplicação fornecidas:
- Tipo de aplicação: {tipo_app}
- Autenticação: {autenticacao}
- Acesso à internet: {internet}
- Dados sensíveis: {dados_sensiveis}
- Descrição da aplicação: {descricao}
- Imagem da arquitetura (base64): {encoded_image}
"""


        # 🔹 Chamada ao Azure OpenAI
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "Você é um especialista em cibersegurança com 20 anos de experiência."},
                {"role": "user", "content": prompt},
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{encoded_image}"}}
                ]}
            ],
            max_tokens=1200,
        )

        # 🔹 Limpar imagem temporária
        os.remove(tmp_path)

        return {"status": "ok", "result": response.choices[0].message.content}

    except Exception as e:
        return {"status": "erro", "detalhes": str(e)}

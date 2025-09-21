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
        # 🔹 Salvar imagem temporária
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            shutil.copyfileobj(image.file, tmp)
            tmp_path = tmp.name

        # 🔹 Converter imagem para Base64
        with open(tmp_path, "rb") as f:
            encoded_image = base64.b64encode(f.read()).decode("ascii")

        # 🔹 Prompt STRIDE
        prompt = f"""
Haja como um especialista em cibersegurança com mais de 20 anos de experiência,
utilizando a metodologia STRIDE para construir modelos de ameaça abrangentes.

Analise a arquitetura e forneça ameaças plausíveis.

Informações da aplicação fornecidas:
- Tipo de aplicação: {tipo_app}
- Autenticação: {autenticacao}
- Acesso à internet: {internet}
- Dados sensíveis: {dados_sensiveis}
- Descrição da aplicação: {descricao}
"""

        # 🔹 Chamada ao Azure OpenAI
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "Você é um especialista em cibersegurança com 20 anos de experiência."},
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": f"data:image/png;base64,{encoded_image}"}
                ]}
            ],
            max_tokens=1200,
        )

        # 🔹 Limpar imagem temporária
        os.remove(tmp_path)

        return {"status": "ok", "result": response.choices[0].message.content}

    except Exception as e:
        return {"status": "erro", "detalhes": str(e)}

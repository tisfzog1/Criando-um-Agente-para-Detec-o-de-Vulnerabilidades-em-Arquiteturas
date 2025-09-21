from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="3GNxKvtsjoyJe98ZHZkywCXnSKviMDx90Vj4RbJNnKss7fztktN1JQQJ99BIACHYHv6XJ3w3AAAAACOGqnNQ",
   api_version="2024-12-01-preview",

    azure_endpoint="https://tisfz-mftttqkx-eastus2.cognitiveservices.azure.com"
 )

response = client.chat.completions.create(
     model="gpt-4o-mini",
     messages=[{"role": "user", "content": "Olá, está funcionando?"}]
 )
print(response.choices[0].message.content)
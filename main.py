import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")


# busca os contatos no Supabase
def buscar_contatos():
    url = f"{SUPABASE_URL}/rest/v1/contatos?select=nome,telefone&limit=3"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# envia a mensagem para um contato via Z-API
def enviar_mensagem(nome, telefone):
    url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"
    mensagem = f"Olá, {nome} tudo bem com você?"

    payload = {
        "phone": telefone,
        "message": mensagem
    }
    headers = {
        "Content-Type": "application/json",
        "Client-Token": ZAPI_CLIENT_TOKEN
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# busca os contatos e envia a mensagem para cada um
def main():
    contatos = buscar_contatos()
    for contato in contatos:
        resultado = enviar_mensagem(contato["nome"], contato["telefone"])
        print(resultado)


if __name__ == "__main__":
    main()
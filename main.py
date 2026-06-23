import os
import requests
from dotenv import load_dotenv
import logging

load_dotenv()
#Responsável por configurar o formato dos logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")


# Função que busca os contatos no Supabase
def buscar_contatos():
    url = f"{SUPABASE_URL}/rest/v1/contatos?select=nome,telefone&limit=3"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Função envia a mensagem para um contato via Z-API
def enviar_mensagem(nome, telefone):
    url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"
    mensagem = f"Olá, {nome} tudo bem com você?"

    payload = {
        "phone": telefone,
        "message": mensagem
    }
    headers = {
        "Content-Type": "application/json",
        "Client-Token": ZAPI_CLIENT_TOKEN # Foi exigido pelo Z-API, sem ele dá o erro 400
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

# Função que busca os contatos e envia a mensagem para cada um
def main():
    try:
        contatos = buscar_contatos()
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao buscar contatos no Supabase: {e}")
        return 
    for contato in contatos:
        try:
            enviar_mensagem(contato["nome"], contato["telefone"])
            logging.info(f"Mensagem enviada com sucesso para {contato['nome']}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao enviar mensagem para {contato['nome']}: {e}")



if __name__ == "__main__":
    main()
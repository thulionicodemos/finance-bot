import requests
import os

def enviar_mensagem_whatsapp(telefone, texto):
    token = os.getenv("WHATSAPP_TOKEN")
    phone_number_id = os.getenv("PHONE_NUMBER_ID")

    url = f"https://graph.facebook.com/v22.0/1006843012503318/messages"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": telefone,
        "type": "text",
        "text": {
            "body": texto
        }
    }

    requests.post(url, headers=headers, json=payload)

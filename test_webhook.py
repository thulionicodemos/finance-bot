import requests

url = "http://127.0.0.1:5000/webhook"

payload = {
    "entry": [
        {
            "changes": [
                {
                    "value": {
                        "messages": [
                            {"type": "text", "text": {"body": "compra mercado 45.90"}}
                        ]
                    }
                }
            ]
        }
    ]
}

response = requests.post(url, json=payload)
print(response.status_code)
print(response.json())

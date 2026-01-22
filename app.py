from flask import Flask, request, jsonify
from parser import parse_mensagem
from sheets_service import SheetsService


app = Flask(__name__)

VERIFY_TOKEN = "EAAVZAimZBniQcBQTOmitZCAMXbSIA32oD5skAWjkgQNeZCZBZBDvyxMh7GkQBbPYe4qx2P432tZCYfuaQz8QtyZBKu53w0TXgg4I45KzOKNeaiv2inJqQc5F3J1o8GxtyO1ClBUSuFt82bwtxk8xDztvpJEam3k9ZCYG4dovo3qC12WZBrOiNp6o3YI1AqDFTvf1NeRCHU5ZBj38aZBCId4WdvriMTAFDgvsgyZANX4HKHWoXyUMR2KlROKZBpSStwxj2336IxXaDZB2LfvfRjRCNNqXMAz"

sheets = SheetsService(nome_planilha="FINANCAS_2026")


@app.route("/webhook", methods=["GET", "POST"])
def webhook():

    # Verificação do webhook
    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return jsonify({"status": "error", "message": "Token inválido"}), 403

    # Recebimento de mensagens
    if request.method == "POST":
        data = request.json

        try:
            message = data["entry"][0]["changes"][0]["value"].get("messages")
            if not message:
                return jsonify({"status": "ok"}), 200

            msg = message[0]

            if msg["type"] != "text":
                return jsonify({"status": "ok"}), 200

            texto = msg["text"]["body"]

            try:
                lancamento = parse_mensagem(texto)
                sheets.inserir_lancamento(lancamento)

                print("Lançamento salvo:", lancamento)

                return jsonify({"status": "success", "message": lancamento}), 200

            except ValueError as e:
                print("Erro de parsing:", e)
                return jsonify({"status": "error", "message": str(e)}), 400

        except Exception as e:
            print("Erro geral:", e)
            return jsonify({"status": "error", "message": "Erro interno"}), 500

        return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run()

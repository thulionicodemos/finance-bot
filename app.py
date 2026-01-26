from flask import Flask, request, jsonify
from parser import parse_mensagem
from sheets_service import SheetsService


app = Flask(__name__)

VERIFY_TOKEN = "EAAVZAimZBniQcBQo7qIelVOdVqxmWqTQvMQCrZBcIfOZC2sdKVf47mFGdT4gLAU9EBSSZCXtPKpweXk8doJancwZCyaywJpcHO0hZBlBI2Hcejhn2G7gIYGxTt2I5IvqKINNTjdxZCjRpBmsbrNOuxcprZAi4vZAo4UhyNOfQFNZCCGOGbnDCh45Fx74Piemk1nET9wBw5S2xK0dAsIaRVQqP7040N2Tp7GEYxBgd3mREfSjBX0mMsdrcUxnKpNuEJps7UkN0WWAbYGGmiyhpZAAHJfVePoo"

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

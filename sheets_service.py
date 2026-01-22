import os
import json
import gspread
from google.oauth2.service_account import Credentials


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


class SheetsService:
    def __init__(self, credenciais_path: str, nome_planilha: str):
        creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")

        if not creds_json:
            raise RuntimeError("Variável GOOGLE_CREDENTIALS_JSON não definida")

        creds_dict = json.loads(creds_json)
        
        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open(nome_planilha).worksheet("LANCAMENTOS_ONLINE")

    def inserir_lancamento(self, lancamento: dict):
        linha = [
            lancamento["data"],
            lancamento["descricao"],
            lancamento["tipo"],
            lancamento["pagamento"],
            lancamento["valor"],
        ]
        self.sheet.append_row(linha)

from sheets_service import SheetsService

sheets = SheetsService(
    credenciais_path="credenciais.json", nome_planilha="FINANCAS_2026"
)

lancamento_teste = {
    "data": "2026-01-04",
    "tipo": "gasto",
    "descricao": "teste sheets",
    "valor": 12.34,
    "pagamento": "pix",
}

sheets.inserir_lancamento(lancamento_teste)

print("Teste concluído com sucesso")

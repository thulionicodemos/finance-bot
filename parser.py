from datetime import date

MEIOS_PAGAMENTO = {"pix", "cartão", "dinheiro", "credito", "debito"}


def parse_mensagem(texto: str) -> dict:
    partes = texto.lower().split()

    if len(partes) < 3:
        raise ValueError("Mensagem incompleta")

    tipo = partes[0]
    if tipo not in {
        "Despesa",
        "despesa",
        "Gasto",
        "gasto",
        "Compra",
        "compra",
        "Comprei",
        "comprei",
        "Receita",
        "receita",
        "Recebi",
        "recebi",
    }:
        raise ValueError("Tipo inválido")

    # Valor sempre será o último número da frase
    valor = None
    for parte in partes:
        if parte.replace(",", ".").replace(".", "", 1).isdigit():
            valor = float(parte.replace(",", "."))
            break

    if valor is None:
        raise ValueError("Valor não encontrado")

    # Descrição = tudo entre tipo e valor
    idx_valor = partes.index(parte)
    descricao = " ".join(partes[1:idx_valor])

    pagamento = "não informado"
    if idx_valor + 1 < len(partes):
        if partes[idx_valor + 1] in MEIOS_PAGAMENTO:
            pagamento = partes[idx_valor + 1]

    return {
        "tipo": tipo,
        "descricao": descricao,
        "valor": valor,
        "pagamento": pagamento,
        "data": date.today().isoformat(),
    }

from parser import parse_mensagem

testes = ["gasto mercado 50", "gasto ifood 89,90 cartão", "receita salario 3500"]

for t in testes:
    try:
        resultado = parse_mensagem(t)
        print("OK:", resultado)
    except Exception as e:
        print("ERRO:", t, e)

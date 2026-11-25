# # inicio busca de resiltado de pagamentos pendentes


# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# token = os.getenv("MERCADO_PAGO_ACCESS_TOKEN")
# print("Token carregado:", bool(token))
# print("Prefixo:", token[:10] if token else "vazio")

# payment_id = "3743185873-e79e16c1-5af9-48e8-8f53-eb589b20a3f3"

# url = f"https://api.mercadopago.com/checkout/preferences/{preference_id}"

# headers = {
#     "Authorization": f"Bearer {token}"
# }

# resposta = requests.get(
#     url,
#     headers=headers,
#     timeout=30
# )

# print("HTTP:", resposta.status_code)

# if resposta.status_code == 200:
#     dados = resposta.json()

#     print("Preference ID:", dados.get("id"))
#     print("Referência:", dados.get("external_reference"))
#     print("Itens:", dados.get("items"))
#     print("Payer:", dados.get("payer"))
# else:
#     print(resposta.text)

# # fim busca de resiltado de pagamentos pendentes

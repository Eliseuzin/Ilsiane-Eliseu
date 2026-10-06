from flask import Blueprint, render_template
from lista_presentes import presentes
from estudos.models import Pagamento, db


routes = Blueprint("routes", __name__)


@routes.route("/")
def inicio():
    print("========== ENTROU NA ROTA INICIO ==========")
    print("PRESENTES:", presentes)

    return render_template(
        "index.html",
        presentes=presentes
    )


# incio integração com o Mercado Pago


# pip install python-dotenv
# pip freeze > requirements.txt
from mercadopay import API_MERCADO_PAGO_ACCESS_TOKEN
# print("========== API_MERCADO_PAGO_ACCESS_TOKEN ==========")
# print(API_MERCADO_PAGO_ACCESS_TOKEN)

# pip install mercadopago
# pip freeze > requirements.txt
# print("Token carregado:", bool(API_MERCADO_PAGO_ACCESS_TOKEN))

import mercadopago

from mercadopay import API_MERCADO_PAGO_ACCESS_TOKEN
sdk = mercadopago.SDK(API_MERCADO_PAGO_ACCESS_TOKEN)


# @routes.route("/criar_pagamento", methods=["POST"])
# def criar_pagamento():

#     preference_data = {
#         "items": [
#             {
#                 "title": "Presente de casamento",
#                 "quantity": 1,
#                 "unit_price": 10.00
#             }
#         ]
#     }

#     preference_response = sdk.preference().create(preference_data)

#     print("====================================")
#     print("RESPOSTA DO MERCADO PAGO:")
#     print(preference_response)
#     print("====================================")

#     return preference_response

from flask import Blueprint, render_template, request

@routes.route("/criar_pagamento", methods=["POST"])
def criar_pagamento():

    dados = request.get_json()

    itens_carrinho = dados.get("presentes", [])

    if not itens_carrinho:
        return {
            "erro": "Carrinho vazio"
        }, 400

    itens_mp = []

    for item in itens_carrinho:

        id_presente = int(item["id"])
        quantidade = int(item["quantity"])

        # Procura o presente verdadeiro na lista_presente.py
        presente = next(
            (
                presente
                for presente in presentes
                if presente["id"] == id_presente
            ),
            None
        )

        if presente is None:
            return {
                "erro": f"Presente com ID {id_presente} não encontrado."
            }, 400

        itens_mp.append({
            "title": presente["nome"].strip(),
            "quantity": quantidade,
            "unit_price": presente["preco"]
        })

    preference_data = {
        "items": itens_mp
    }

    preference_response = sdk.preference().create(preference_data)

    preference = preference_response["response"]

    return {
        "id": preference["id"],
        "link": preference["init_point"]
    }




# fim integração com o Mercado Pago
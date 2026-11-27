# from unittest.mock import MagicMock, patch

# from app import app
# import estudos.routes as rotas


# def test_preco_adulterado_nao_e_utilizado():

#     presente_oficial = {
#         "id": 1,
#         "nome": "Liquidificador",
#         "preco": 180.99
#     }

#     compra_fake = MagicMock()
#     compra_fake.id = 123
#     compra_fake.referencia = "TESTE-SEGURANCA-123"

#     resposta_fake_mp = {
#         "status": 201,
#         "response": {
#             "id": "PREF-TESTE-123",
#             "init_point": "https://teste.local"
#         }
#     }

#     preference_mock = MagicMock()
#     preference_mock.create.return_value = resposta_fake_mp

#     with app.test_client() as cliente, \
#          patch.object(rotas, "presentes", [presente_oficial]), \
#          patch.object(rotas, "Compra", return_value=compra_fake), \
#          patch.object(rotas, "ItemCompra"), \
#          patch.object(rotas.db.session, "add"), \
#          patch.object(rotas.db.session, "flush"), \
#          patch.object(rotas.db.session, "commit"), \
#          patch.object(rotas.db.session, "rollback"), \
#          patch.object(rotas.sdk, "preference", return_value=preference_mock):

#         resposta = cliente.post(
#             "/criar_pagamento",
#             json={
#                 "presentes": [
#                     {
#                         "id": 1,
#                         "quantity": 1,
#                         "preco": 0.01
#                     }
#                 ]
#             }
#         )

#     assert resposta.status_code == 200

#     dados_preferencia = preference_mock.create.call_args[0][0]

#     preco_enviado_mp = dados_preferencia["items"][0]["unit_price"]

#     assert preco_enviado_mp == 180.99
#     assert preco_enviado_mp != 0.01

#     print("Preço enviado ao Mercado Pago:", preco_enviado_mp)
#     print("Teste de manipulação de preço aprovado!")




from decimal import Decimal
from unittest.mock import MagicMock, patch

from app import app
import estudos.routes as rotas


def test_preco_adulterado_nao_e_utilizado():

    # Utiliza a lista real de presentes do projeto.
    presente_real = next(
        p for p in rotas.presentes
        if p["id"] == 1
    )

    preco_oficial = Decimal(str(presente_real["preco"]))

    compra_fake = MagicMock()
    compra_fake.id = 123
    compra_fake.referencia = "TESTE-SEGURANCA-123"

    resposta_fake_mp = {
        "status": 201,
        "response": {
            "id": "PREF-TESTE-123",
            "init_point": "https://teste.local"
        }
    }

    preference_mock = MagicMock()
    preference_mock.create.return_value = resposta_fake_mp

    with app.test_client() as cliente, \
         patch.object(rotas, "Compra", return_value=compra_fake), \
         patch.object(rotas, "ItemCompra"), \
         patch.object(rotas.db.session, "add"), \
         patch.object(rotas.db.session, "flush"), \
         patch.object(rotas.db.session, "commit"), \
         patch.object(rotas.db.session, "rollback"), \
         patch.object(rotas.sdk, "preference", return_value=preference_mock):

        resposta = cliente.post(
            "/criar_pagamento",
            json={
                "presentes": [
                    {
                        "id": presente_real["id"],
                        "quantity": 1,
                        "preco": 0.01
                    }
                ]
            }
        )

    assert resposta.status_code == 200

    dados_preferencia = preference_mock.create.call_args[0][0]

    preco_enviado_mp = Decimal(
        str(dados_preferencia["items"][0]["unit_price"])
    )

    assert preco_enviado_mp == preco_oficial
    assert preco_enviado_mp != Decimal("0.01")

    print("Preço oficial:", preco_oficial)
    print("Preço enviado ao Mercado Pago:", preco_enviado_mp)
    print("Teste de manipulação de preço aprovado!")
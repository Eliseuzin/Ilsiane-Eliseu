from flask import Blueprint, render_template
from lista_presentes import presentes
from estudos.models import Pagamento, db


routes = Blueprint("routes", __name__)


@routes.route("/")
def inicio():
    # print("========== ENTROU NA ROTA INICIO ==========")
    # print("PRESENTES:", presentes)

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

# from mercadopay import API_MERCADO_PAGO_ACCESS_TOKEN
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

from estudos.models import Compra, ItemCompra, db
from decimal import Decimal


@routes.route("/criar_pagamento", methods=["POST"])
def criar_pagamento():
    dados = request.get_json(silent=True) or {}
    itens_carrinho = dados.get("presentes", [])

    if not isinstance(itens_carrinho, list) or not itens_carrinho:
        return {"erro": "Carrinho vazio ou inválido."}, 400

    itens_mp = []
    itens_banco = []
    valor_total = Decimal("0.00")

    try:
        for item in itens_carrinho:
            id_presente = int(item["id"])
            quantidade = int(item["quantity"])

            if quantidade <= 0:
                return {"erro": "A quantidade deve ser maior que zero."}, 400

            # Busca o presente na lista oficial do projeto.
            presente = next(
                (
                    p for p in presentes
                    if p["id"] == id_presente
                ),
                None
            )

            if presente is None:
                return {
                    "erro": f"Presente com ID {id_presente} não encontrado."
                }, 400

            # O preço vem do servidor, não do navegador.
            preco = Decimal(str(presente["preco"]))
            subtotal = preco * quantidade
            valor_total += subtotal

            itens_mp.append({
                "title": presente["nome"].strip(),
                "quantity": quantidade,
                "unit_price": float(preco),
                "currency_id": "BRL"
            })

            itens_banco.append({
                "presente_id": id_presente,
                "nome_presente": presente["nome"].strip(),
                "quantidade": quantidade,
                "valor_unitario": preco,
                "subtotal": subtotal
            })

    except (KeyError, TypeError, ValueError, ArithmeticError):
        return {"erro": "Os dados dos presentes são inválidos."}, 400

    try:
        # Cria a compra no banco.
        compra = Compra(
            valor_total=valor_total,
            status="pendente"
        )

        db.session.add(compra)
        db.session.flush()

        # Associa cada presente à compra criada.
        for item_banco in itens_banco:
            item_banco["compra_id"] = compra.id
            db.session.add(ItemCompra(**item_banco))

        preference_data = {
            "items": itens_mp,

            # Permite localizar esta compra no webhook.
            "external_reference": compra.referencia,

            "back_urls": {
                "success": (
                    "https://convite-para-nosso-casamento.onrender.com/"
                    "pagamento/sucesso"
                ),
                "pending": (
                    "https://convite-para-nosso-casamento.onrender.com/"
                    "pagamento/pendente"
                ),
                "failure": (
                    "https://convite-para-nosso-casamento.onrender.com/"
                    "pagamento/falha"
                )
            },

            "auto_return": "approved",

            "notification_url": (
                "https://convite-para-nosso-casamento.onrender.com/"
                "webhook/mercadopago"
            )
        }

        # Solicita a criação do checkout ao Mercado Pago.
        resposta_mp = sdk.preference().create(preference_data)

        if resposta_mp.get("status") not in (200, 201):
            db.session.rollback()
            logger.error(
                "Falha ao criar preferência: HTTP %s",
                resposta_mp.get("status")
            )
            return {
                "erro": "Não foi possível iniciar o pagamento."
            }, 502

        preference = resposta_mp.get("response", {})
        preference_id = preference.get("id")
        link_pagamento = preference.get("init_point")

        if not preference_id or not link_pagamento:
            db.session.rollback()
            logger.error("Resposta incompleta ao criar preferência.")
            return {
                "erro": "O Mercado Pago não retornou o link de pagamento."
            }, 502

        # Guarda a preferência e confirma a compra no banco.
        compra.preference_id = str(preference_id)
        db.session.commit()

        return {
            "id": preference_id,
            "link": link_pagamento
        }

    except Exception:
        db.session.rollback()
        logger.exception("Erro ao registrar compra ou criar pagamento.")

        return {
            "erro": "Ocorreu um erro ao iniciar o pagamento."
        }, 500

# fim integração com o Mercado Pago

# inicio rotas de sucesso, falha e pendente do pagamento

@routes.route("/pagamento/sucesso")
def pagamento_sucesso():
    return render_template("pagamento/sucesso.html")


@routes.route("/pagamento/pendente")
def pagamento_pendente():
    return render_template("pagamento/pendente.html")


@routes.route("/pagamento/falha")
def pagamento_falha():
    return render_template("pagamento/falha.html")

# fim rotas de sucesso, falha e pendente do pagamento


from flask import request, jsonify
import logging

logger = logging.getLogger(__name__)

# inicio webhook do Mercado Pago para receber notificações de pagamento

@routes.route("/webhook/mercadopago", methods=["POST"])
def webhook_mercadopago():
    dados = request.get_json(silent=True) or {}

    tipo = (
        dados.get("type")
        or request.args.get("type")
        or request.args.get("topic")
    )

    payment_id = (
        dados.get("data", {}).get("id")
        or request.args.get("data.id")
        or (
            request.args.get("id")
            if tipo == "payment"
            else None
        )
    )

    logger.info(
        "Webhook recebido: tipo=%s, payment_id=%s",
        tipo,
        payment_id
    )

    # Ignora notificações que não sejam de pagamento.
    if tipo != "payment":
        return jsonify({
            "status": "notificacao_ignorada"
        }), 200

    if not payment_id:
        return jsonify({
            "erro": "ID do pagamento ausente"
        }), 400

    try:
        # Consulta o pagamento diretamente ao Mercado Pago.
        resposta = sdk.payment().get(str(payment_id))

        if resposta.get("status") != 200:
            logger.error(
                "Falha ao consultar pagamento %s",
                payment_id
            )
            return jsonify({
                "erro": "Falha ao consultar pagamento"
            }), 502

        pagamento = resposta.get("response", {})
        status_pagamento = pagamento.get("status")

        logger.info(
            "Pagamento %s: status=%s",
            payment_id,
            status_pagamento
        )

        # Identifica a compra criada antes do checkout.
        referencia = pagamento.get("external_reference")

        if not referencia:
            logger.error(
                "Pagamento %s sem external_reference",
                payment_id
            )
            return jsonify({
                "status": "referencia_ausente"
            }), 200

        compra = Compra.query.filter_by(
            referencia=referencia
        ).first()

        if compra is None:
            logger.error(
                "Compra não encontrada para a referência %s",
                referencia
            )
            return jsonify({
                "status": "compra_nao_encontrada"
            }), 200

        # Impede que o mesmo pagamento seja associado
        # a duas compras diferentes.
        outra_compra = Compra.query.filter_by(
            mercado_pago_id=str(payment_id)
        ).first()

        if outra_compra and outra_compra.id != compra.id:
            logger.error(
                "Pagamento %s associado a outra compra",
                payment_id
            )
            return jsonify({
                "status": "pagamento_ja_associado"
            }), 200

        # Não permite substituir o ID de pagamento
        # de uma compra por outro ID.
        if (
            compra.mercado_pago_id
            and compra.mercado_pago_id != str(payment_id)
        ):
            logger.error(
                "Compra %s já possui outro pagamento associado",
                compra.id
            )
            return jsonify({
                "status": "pagamento_divergente"
            }), 200

        # Se a compra já foi aprovada, não a reprocessa.
        if compra.status == "approved":
            if compra.mercado_pago_id == str(payment_id):
                return jsonify({
                    "status": "ja_processado",
                    "compra_id": compra.id
                }), 200

        # Registra outros estados, sem substituir uma
        # aprovação já confirmada por um estado inferior.
        if status_pagamento != "approved":
            if compra.status != "approved":
                compra.status = status_pagamento or "desconhecido"
                db.session.commit()

            return jsonify({
                "status": status_pagamento or "desconhecido",
                "compra_id": compra.id
            }), 200

        # Confere o valor e a moeda antes de aprovar a compra.
        try:
            valor_pago = Decimal(
                str(pagamento.get("transaction_amount"))
            ).quantize(Decimal("0.01"))

            valor_compra = Decimal(
                str(compra.valor_total)
            ).quantize(Decimal("0.01"))
        except Exception:
            logger.exception(
                "Valor inválido no pagamento %s",
                payment_id
            )
            return jsonify({
                "status": "valor_invalido"
            }), 200

        moeda = pagamento.get("currency_id")

        if moeda != "BRL" or valor_pago != valor_compra:
            logger.error(
                "Divergência no pagamento %s: "
                "valor_pago=%s, valor_compra=%s, moeda=%s",
                payment_id,
                valor_pago,
                valor_compra,
                moeda
            )
            return jsonify({
                "status": "revisao_necessaria"
            }), 200

        # Salva a aprovação confirmada pela API.
        compra.status = "approved"
        compra.mercado_pago_id = str(payment_id)

        # Guarda os dados do pagador para a futura
        # implementação dos e-mails.
        pagador = pagamento.get("payer") or {}

        nome = " ".join(
            parte for parte in [
                pagador.get("first_name"),
                pagador.get("last_name")
            ]
            if parte
        ).strip()

        if nome:
            compra.nome_convidado = nome

        if pagador.get("email"):
            compra.email_convidado = pagador["email"]

        db.session.commit()

        logger.info(
            "Compra %s aprovada e salva. Pagamento: %s",
            compra.id,
            payment_id
        )

        return jsonify({
            "status": "approved",
            "compra_id": compra.id,
            "payment_id": str(payment_id)
        }), 200

    except Exception:
        db.session.rollback()

        logger.exception(
            "Erro ao processar webhook do pagamento %s",
            payment_id
        )

        return jsonify({
            "erro": "Erro ao processar o pagamento"
        }), 500

# fim webhook do Mercado Pago para receber notificações de pagamento
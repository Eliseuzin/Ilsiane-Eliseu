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
from app import app
from flask import render_template
from lista_presentes import presentes

print("========== ROUTES.PY FOI CARREGADO ==========")
print("PRESENTES:", presentes)


@app.route("/")
def inicio():
    print("========== ENTROU NA ROTA INICIO ==========")

    return render_template(
        "index.html",
        presentes=presentes
    )
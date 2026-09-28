from estudos import app
from flask import render_template, url_for, redirect
from lista_presentes import presentes

@app.route("/")
def convite():
    print("chegamos ate aqui")
    return render_template(
        "index.html", presentes=presentes
    )
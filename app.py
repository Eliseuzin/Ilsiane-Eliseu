from flask import Flask
from estudos.models import db

app = Flask(
    __name__,
    template_folder="estudos/templates",
    static_folder="estudos/static"
)


# Configuração do banco de dados

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///casamento.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializa o banco
db.init_app(app)

from estudos.routes import routes

app.register_blueprint(routes)


# Cria as tabelas
with app.app_context():
     db.create_all()

# print(app.url_map)

if __name__ == "__main__":
    app.run(debug=True)
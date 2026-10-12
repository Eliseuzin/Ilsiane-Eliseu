
import os
from flask import Flask
from estudos.models import db

app = Flask(
    __name__,
    template_folder="estudos/templates",
    static_folder="estudos/static"
)

# Configuração do banco de dados
database_url = os.getenv("DATABASE_URL")

# Compatibilidade com URLs antigas do PostgreSQL
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://",
        "postgresql://",
        1
    )

app.config["SQLALCHEMY_DATABASE_URI"] = (
    database_url or "sqlite:///casamento.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializa o banco
db.init_app(app)

from estudos.routes import routes
app.register_blueprint(routes)

# Cria as tabelas que ainda não existem
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
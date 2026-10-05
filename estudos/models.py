from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Pagamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    presente_id = db.Column(db.Integer, nullable=False)

    nome_presente = db.Column(db.String(200), nullable=False)

    valor = db.Column(db.Float, nullable=False)

    nome_convidado = db.Column(db.String(150), nullable=True)

    email_convidado = db.Column(db.String(150), nullable=True)

    status = db.Column(
        db.String(50),
        nullable=False,
        default="pendente"
    )

    mercado_pago_id = db.Column(
        db.String(100),
        nullable=True
    )

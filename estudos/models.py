
from datetime import datetime

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
        nullable=True,
        unique=True
    )

    criado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    email_casal_enviado = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    email_convidado_enviado = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )



from datetime import datetime
import uuid


class Compra(db.Model):
    __tablename__ = "compra"

    id = db.Column(db.Integer, primary_key=True)

    referencia = db.Column(
        db.String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4())
    )

    mercado_pago_id = db.Column(
        db.String(100),
        unique=True,
        nullable=True
    )

    preference_id = db.Column(db.String(100), nullable=True)

    valor_total = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="pendente")

    nome_convidado = db.Column(db.String(150), nullable=True)
    email_convidado = db.Column(db.String(150), nullable=True)

    criado_em = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    email_casal_enviado = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    email_convidado_enviado = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    itens = db.relationship(
        "ItemCompra",
        back_populates="compra",
        cascade="all, delete-orphan"
    )


class ItemCompra(db.Model):
    __tablename__ = "item_compra"

    id = db.Column(db.Integer, primary_key=True)

    compra_id = db.Column(
        db.Integer,
        db.ForeignKey("compra.id"),
        nullable=False,
        index=True
    )

    presente_id = db.Column(db.Integer, nullable=False)
    nome_presente = db.Column(db.String(200), nullable=False)

    quantidade = db.Column(db.Integer, nullable=False)

    valor_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)

    compra = db.relationship(
        "Compra",
        back_populates="itens"
    )
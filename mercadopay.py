import os   
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

API_MERCADO_PAGO_ACCESS_TOKEN=os.getenv("MERCADO_PAGO_ACCESS_TOKEN")
import os
from dotenv import load_dotenv

load_dotenv()

API_MERCADO_PAGO_ACCESS_TOKEN = os.getenv(
    "API_MERCADO_PAGO_ACCESS_TOKEN"
)

print(
    "TOKEN EXISTE:",
    API_MERCADO_PAGO_ACCESS_TOKEN is not None
)

print(
    "TOKEN É STRING:",
    isinstance(API_MERCADO_PAGO_ACCESS_TOKEN, str)
)

print(
    "TOKEN TEM VALOR:",
    bool(API_MERCADO_PAGO_ACCESS_TOKEN)
)
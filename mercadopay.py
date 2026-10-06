import os   
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

API_MERCADO_PAGO_ACCESS_TOKEN=os.getenv("MERCADO_PAGO_ACCESS_TOKEN")

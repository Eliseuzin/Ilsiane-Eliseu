import os
import time
import uuid
import hmac
import hashlib
import requests

from dotenv import load_dotenv

load_dotenv()

import os
import time
import uuid
import hmac
import hashlib
import requests

from dotenv import load_dotenv

load_dotenv()

segredo = os.getenv("MP_WEBHOOK_SECRET")
segredo = segredo.strip() if segredo else None

print("Segredo carregado:", bool(segredo))
print("Tamanho do segredo:", len(segredo) if segredo else 0)

if not segredo:
    raise ValueError("MP_WEBHOOK_SECRET não encontrado no .env")

payment_id = "189592147793"

request_id = str(uuid.uuid4())
timestamp = str(int(time.time()))

manifesto = (
    f"id:{payment_id.lower()};"
    f"request-id:{request_id};"
    f"ts:{timestamp};"
)

assinatura = hmac.new(
    segredo.encode("utf-8"),
    manifesto.encode("utf-8"),
    hashlib.sha256
).hexdigest()

url = (
    "https://convite-para-nosso-casamento.onrender.com"
    "/webhook/mercadopago"
)

params = {
    "data.id": payment_id,
    "type": "payment"
}

headers = {
    "x-signature": f"ts={timestamp},v1={assinatura}",
    "x-request-id": request_id,
    "Content-Type": "application/json"
}

payload = {
    "action": "payment.updated",
    "type": "payment",
    "data": {
        "id": payment_id
    }
}

resposta = requests.post(
    url,
    params=params,
    headers=headers,
    json=payload,
    timeout=30
)

print("HTTP:", resposta.status_code)
print("Resposta:", resposta.text)
import json
from datetime import datetime
from src.predict import prever_fraude
from src.schemas import OprInput

MODEL_VERSION = "v1"

def lambda_handler(event, context):
    resultados = []
    for record in event['Records']:
        body = json.loads(record['body'])
        transaction_id = body["transaction_id"]
        features = body["features"]

        # Validação com Pydantic
        opr = OprInput(**features)
        dados_validados = opr.model_dump()

        # Predição
        resultado = prever_fraude(dados_validados)

        resultados.append({
            "transaction_id": transaction_id,
            "fraud_score": resultado["prob_fraude"],
            "prediction": resultado["resultado"],
            "model_version": MODEL_VERSION,
            "processed_at": datetime.now().isoformat()
        })

    # Resposta 
    return {
        "resultado": "success",
        "results": resultados,
    }
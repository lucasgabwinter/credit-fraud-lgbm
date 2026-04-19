from datetime import datetime
from src.predict import prever_fraude
from src.schemas import OprInput

MODEL_VERSION = "v1"

def lambda_handler(event, context):
    try:
        transaction_id = event["transaction_id"]
        features = event["features"]

        # Validação com Pydantic
        opr = OprInput(**features)
        dados_validados = opr.model_dump()

        # Predição
        resultado = prever_fraude(dados_validados)

        # Resposta padronizada
        return {
            "transaction_id": transaction_id,
            "fraud_score": resultado["prob_fraude"],
            "prediction": resultado["resultado"],
            "model_version": MODEL_VERSION,
            "processed_at": datetime.now().isoformat()
        }

    except Exception as e:
        return {
            "error": str(e)
        }
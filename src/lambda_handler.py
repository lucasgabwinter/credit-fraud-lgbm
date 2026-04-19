import json
import os
from datetime import datetime
from src.predict import prever_fraude
from src.schemas import OprInput
import boto3
from decimal import Decimal

_TABLE = None
def get_table():
    global _TABLE
    if _TABLE is None:
        dynamodb = boto3.resource("dynamodb")
        _TABLE = dynamodb.Table(os.environ["RESULTS_TABLE_NAME"])
    return _TABLE

def to_dynamodb_item(value):
    return json.loads(json.dumps(value), parse_float=Decimal)

MODEL_VERSION = "v1"

def lambda_handler(event, context):
    table = get_table()
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

        # Formato para armazenar no DynamoDB
        item = {
            "transaction_id": transaction_id,
            "features": to_dynamodb_item(dados_validados),
            "fraud_score": Decimal(str(resultado["prob_fraude"])),
            "prediction": resultado["resultado"],
            "threshold": Decimal(str(resultado["threshold"])),
            "model_version": MODEL_VERSION,
            "processed_at": datetime.now().isoformat()
        }
        table.put_item(Item=item,)

        # Formato para retornar no Lambda
        resultados.append({
            "transaction_id": transaction_id,
            "features": dados_validados,
            "fraud_score": float(resultado["prob_fraude"]),
            "prediction": resultado["resultado"],
            "threshold": float(resultado["threshold"]),
            "model_version": MODEL_VERSION,
            "processed_at": item["processed_at"]
        })

    # Resposta 
    return {
        "resultado": "success",
        "results": resultados,
    }
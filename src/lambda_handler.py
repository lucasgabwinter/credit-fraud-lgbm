import json
import os
from datetime import datetime
import boto3
from decimal import Decimal
from src.predict import prever_fraude
from src.schemas import OprInput

_TABLE = None
_SNS_CLIENT = None


def get_table():
    global _TABLE
    if _TABLE is None:
        dynamodb = boto3.resource("dynamodb")
        _TABLE = dynamodb.Table(os.environ["RESULTS_TABLE_NAME"])
    return _TABLE


def get_sns_client():
    global _SNS_CLIENT
    if _SNS_CLIENT is None:
        _SNS_CLIENT = boto3.client("sns")
    return _SNS_CLIENT


def to_dynamodb_item(value):
    return json.loads(json.dumps(value), parse_float=Decimal)


def publish_fraud_alert(result_item):
    topic_arn = os.environ.get("SNS_TOPIC_ARN")
    if not topic_arn:
        return

    subject = f"Alerta de fraude detectada: {result_item['transaction_id']}"

    message = f"""
    Alerta de fraude detectada!
    Código da operação: {result_item['transaction_id']}
    Resultado do modelo: {result_item['prediction']}
    Probabilidade de Fraude: {result_item['fraud_score']:.4f}
    Threshold: {result_item['threshold']:.4f}
    Versão do modelo: {result_item['model_version']}
    Processado em: {result_item['processed_at']}
    Modelo e sistemas criados por Lucas Winter.
    """.strip()

    get_sns_client().publish(
        TopicArn=topic_arn,
        Subject=subject,
        Message=message,
    )


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

        if resultados[-1]["prediction"] == "fraude":
            publish_fraud_alert(resultados[-1])

    # Resposta 
    return {
        "resultado": "success",
        "results": resultados,
    }

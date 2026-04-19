## Projeto para Deteccao de Fraude

### API local

Instale as dependencias no ambiente virtual e suba a API:

```bash
uvicorn main:app --reload
```

### Lambda local com SAM

O projeto usa Lambda com container image para suportar o LightGBM e a dependencia nativa `libgomp`.

```bash
sam build
sam local invoke FraudScoringFunction -e events/event.json
```

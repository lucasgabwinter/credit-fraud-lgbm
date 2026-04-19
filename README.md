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

### Alertas por e-mail via SNS

Ao fazer o deploy, voce pode informar um e-mail para receber alertas quando a predicao for `fraude`.

```bash
sam deploy --parameter-overrides AlertEmail=seu-email@exemplo.com
```

Depois do deploy, confirme a inscricao no e-mail recebido da AWS SNS.

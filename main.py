from fastapi import FastAPI, HTTPException
from src.predict import prever_fraude
from src.schemas import OprInput, PredicaoOutput


app = FastAPI(
    title="API de Predição de Probabilidade de Fraude",
    description="Modelo LightGBM para detecção de Fraude.",
    version="1.0.0",
)

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/predict", response_model=PredicaoOutput)
def predict(opr: OprInput):
    try:
        dict_fraude = prever_fraude(opr.model_dump())
        return PredicaoOutput(prob_fraude=dict_fraude['prob_fraude'], resultado=dict_fraude['resultado'])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
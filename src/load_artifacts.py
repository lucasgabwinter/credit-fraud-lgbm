from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = BASE_DIR / 'artifacts'

def carregar_artefatos() -> dict:
    artifacts = {
        'modelo_lbm' : joblib.load(ARTIFACTS_DIR / 'modelo_lbm.pkl'),
        'colunas_modelo' : joblib.load(ARTIFACTS_DIR / 'colunas_modelo.pkl'),
        'threshold' : joblib.load(ARTIFACTS_DIR / 'threshold.pkl'),
    }
    return artifacts
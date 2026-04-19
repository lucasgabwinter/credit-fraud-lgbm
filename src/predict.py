import pandas as pd
from .load_artifacts import carregar_artefatos

ARTIFACTS = carregar_artefatos()

modelo_lbm = ARTIFACTS['modelo_lbm']
colunas_modelo = ARTIFACTS['colunas_modelo']
threshold = ARTIFACTS['threshold']

def prever_fraude(nova_opr: dict) -> dict:
    campos_necessarios = []
    for i in range(1, 29):
        campos_necessarios.append(f'V{i}')
    campos_necessarios.append('Amount')

    faltando = [col for col in campos_necessarios if col not in nova_opr]
    if faltando:
        raise ValueError(f'Campos ausentes: {faltando}')
    
    dict_return = {
        'prob_fraude': 0,
        'resultado': '',
        'threshold': threshold
    }

    df = pd.DataFrame([nova_opr])
    df = df[colunas_modelo]

    dict_return['prob_fraude'] = modelo_lbm.predict(df)[0]
    dict_return['resultado'] = 'fraude' if dict_return['prob_fraude'] >= threshold else 'nao_fraude'

    return dict_return
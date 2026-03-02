import joblib
import pandas as pd
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

import math
import joblib
import pandas as pd

def _clean(v):
    # converte NaN -> None (JSON aceita null)
    if isinstance(v, float) and math.isnan(v):
        return None
    return v

def build_payload_from_csv():
    df = pd.read_csv("data/dataset_modelo.csv")
    row = df.iloc[0].to_dict()

    # remove colunas que não são entrada
    for c in ["Risco", "Target", "IAN"]:
        row.pop(c, None)

    # alinhar com o que o modelo espera
    model = joblib.load("app/artifacts/model.joblib")
    expected = list(model.feature_names_in_)

    aligned = {k: _clean(row.get(k, None)) for k in expected}
    return {"data": aligned}


def test_predict_returns_expected_fields():
    payload = build_payload_from_csv()
    r = client.post("/predict", json=payload)
    assert r.status_code == 200

    body = r.json()
    assert "risco" in body
    assert "probabilidade" in body

    assert body["risco"] in [0, 1]
    assert isinstance(body["probabilidade"], float)
    assert 0.0 <= body["probabilidade"] <= 1.0

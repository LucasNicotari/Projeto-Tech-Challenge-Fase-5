import math
import pandas as pd
import requests

BASE_URL = "http://127.0.0.1:8004"

DROP_INPUT_COLS = {"Risco", "Target", "IAN"}  # nunca mandar isso pra API

def clean_value(v):
    # pandas NaN -> None (vira null no JSON)
    if isinstance(v, float) and math.isnan(v):
        return None
    return v

def test_health():
    url = f"{BASE_URL}/health"
    r = requests.get(url, timeout=10)
    print("\n[HEALTH]")
    print("status:", r.status_code)
    print("body:", r.text)

def test_predict():
    df = pd.read_csv("data/dataset_modelo.csv")
    row = df.iloc[0].to_dict()

    # remove colunas proibidas
    for c in list(row.keys()):
        if c in DROP_INPUT_COLS:
            row.pop(c, None)

    payload = {"data": {k: clean_value(v) for k, v in row.items()}}

    url = f"{BASE_URL}/predict"
    r = requests.post(url, json=payload, timeout=30)

    print("\n[PREDICT]")
    print("status:", r.status_code)
    print("body:", r.text)

    if r.status_code != 200:
        print("\n⚠️ Se o erro for 422, significa 'faltou campo' ou tipo errado.")
        print("Vamos ajustar o formato do request de acordo com o schema da sua API.")

def main():
    test_health()
    test_predict()

if __name__ == "__main__":
    main()

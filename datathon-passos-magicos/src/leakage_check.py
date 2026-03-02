import pandas as pd
import numpy as np
from src.config import settings

def cramers_v(x: pd.Series, y: pd.Series) -> float:
    """
    Cramér's V (simples): mede associação entre duas colunas categóricas.
    Retorna um valor de 0 a 1 (quanto mais perto de 1, mais "colado").
    """
    # trata nulos como string "NA" para contar
    x = x.fillna("NA").astype(str)
    y = y.fillna("NA").astype(str)

    ct = pd.crosstab(x, y)
    n = ct.values.sum()
    if n == 0:
        return 0.0

    # qui-quadrado (manual, sem scipy)
    expected = np.outer(ct.sum(axis=1).values, ct.sum(axis=0).values) / n
    chi2 = ((ct.values - expected) ** 2 / (expected + 1e-12)).sum()

    r, k = ct.shape
    if min(r - 1, k - 1) == 0:
        return 0.0
    return float(np.sqrt((chi2 / n) / min(r - 1, k - 1)))

def main():
    df = pd.read_csv(settings.DATA_PATH)

    # y = target (alvo)
    y = df[settings.TARGET_COL]

    # X = dados de entrada
    X = df.drop(columns=[settings.TARGET_COL], errors="ignore")

    print("Dataset:", settings.DATA_PATH)
    print("Target:", settings.TARGET_COL)
    print("Linhas/Colunas:", df.shape)

    suspicious = []

    for col in X.columns:
        s = X[col]

        # 1) se a coluna tem no nome algo suspeito
        name_lower = col.lower()
        if any(word in name_lower for word in ["defas", "risco", "target"]):
            suspicious.append((col, "nome_suspeito", None))
            continue

        # 2) se a coluna é numérica, ver correlação com o target
        if pd.api.types.is_numeric_dtype(s):
            s2 = pd.to_numeric(s, errors="coerce")
            y2 = pd.to_numeric(y, errors="coerce")
            corr = s2.corr(y2)
            if corr is not None and abs(corr) >= 0.95:
                suspicious.append((col, "corr_alta", float(corr)))
        else:
            # 3) se é texto/categórica, medir associação (Cramér's V)
            v = cramers_v(s, y)
            if v >= 0.95:
                suspicious.append((col, "assoc_alta", float(v)))

    print("\n=== COLUNAS SUSPEITAS (possível 'cola') ===")
    if not suspicious:
        print("Nenhuma coluna muito suspeita encontrada (>=0.95).")
    else:
        for col, reason, score in suspicious:
            if score is None:
                print(f"- {col} | motivo: {reason}")
            else:
                print(f"- {col} | motivo: {reason} | score: {score:.4f}")

    print("\nDica: se aparecer algo relacionado a 'defasagem' ou 'Target', vamos remover do treino.")

if __name__ == "__main__":
    main()

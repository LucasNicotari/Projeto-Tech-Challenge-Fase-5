import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from asyncio.windows_utils import pipe
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from src.config import settings

def main():
    df = pd.read_csv(settings.DATA_PATH)

    # y = alvo (o que queremos prever)
    y = df[settings.TARGET_COL]

    # X = dados de entrada
    X = df.drop(columns=[settings.TARGET_COL], errors="ignore")

    # remover colunas que não queremos usar
    for col in settings.DROP_COLS:
        if col in X.columns:
            X = X.drop(columns=[col])

    # remover colunas 100% vazias (evita warnings)
    X = X.dropna(axis=1, how="all")

    # separar em treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=settings.RANDOM_STATE,
        stratify=y
    )

    # identificar colunas numéricas e categóricas (texto)
    num_cols = X_train.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = [c for c in X_train.columns if c not in num_cols]

    # pré-processamento
    preprocessor = ColumnTransformer(
    transformers=[
        ("num", Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ]), num_cols),
        ("cat", Pipeline(steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("ohe", OneHotEncoder(handle_unknown="ignore"))
        ]), cat_cols),
    ]
)

    model = LogisticRegression(max_iter=5000)

    pipe = Pipeline(steps=[
        ("pre", preprocessor),
        ("model", model)
    ])

    print("Treinando modelo...")
    pipe.fit(X_train, y_train)

    # salvar o modelo treinado (pipeline completo)
    model_path = Path("app/artifacts/model.joblib")
    joblib.dump(pipe, model_path)
    print(f"\n✅ Modelo salvo em: {model_path}")


    print("Avaliando...")
    y_pred = pipe.predict(X_test)

    print("\nMatriz de confusão:")
    print(confusion_matrix(y_test, y_pred))

    print("\nRelatório de classificação:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    main()

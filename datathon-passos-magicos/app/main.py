from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import joblib
import pandas as pd
from pathlib import Path
from sklearn.pipeline import Pipeline

app = FastAPI(
    title="Datathon - Passos Mágicos",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Predict",
            "description": "Endpoints for making predictions"
        }
    ]
)

# Load the trained model
model_path = Path(__file__).resolve().parent / "artifacts" / "model.joblib"
try:
    model = joblib.load(model_path)
    print(f"Model loaded successfully from {model_path}")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

class StudentData(BaseModel):
    RA: str
    Fase: int
    Turma: str
    Nome: str
    Ano_nasc: float
    Idade_22: float
    Gênero: str
    Ano_ingresso: int
    Instituição_de_ensino: str
    Pedra_20: str
    Pedra_21: str
    Pedra_22: str
    INDE_22: float
    Cg: float
    Cf: float
    Ct: float
    Nº_Av: float
    Avaliador1: str
    Rec_Av1: str
    Avaliador2: str
    Rec_Av2: str
    Avaliador3: str
    Rec_Av3: str
    Avaliador4: str
    Rec_Av4: str
    IAA: float
    IEG: float
    IPS: float
    Rec_Psicologia: str
    IDA: float
    Matem: float
    Portug: float
    Inglês: float
    Indicado: str
    Atingiu_PV: str
    IPV: float
    IAN: float
    Fase_ideal: str
    Destaque_IEG: str
    Destaque_IDA: str
    Destaque_IPV: str
    Ano: int
    INDE_2023: Optional[float] = None
    Pedra_2023: Optional[str] = None
    Nome_Anonimizado: Optional[str] = None
    Data_de_Nasc: Optional[str] = None
    Idade: Optional[float] = None
    Pedra_23: Optional[str] = None
    INDE_23: Optional[float] = None
    IPP: Optional[float] = None
    Mat: Optional[float] = None
    Por: Optional[float] = None
    Ing: Optional[float] = None
    Fase_Ideal: Optional[str] = None
    Destaque_IPV_1: Optional[str] = None
    INDE_2024: Optional[float] = None
    Pedra_2024: Optional[str] = None
    Avaliador5: Optional[str] = None
    Avaliador6: Optional[str] = None
    Escola: Optional[str] = None
    Ativo_Inativo: Optional[str] = None
    Ativo_Inativo_1: Optional[str] = None

@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "API online. Use /docs para testar."}

@app.post("/predict")
def predict(data: dict):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    # Convert to DataFrame
    df = pd.DataFrame([data])

# Garantir as mesmas colunas usadas no treino
    if hasattr(model, "feature_names_in_"):
        expected = list(model.feature_names_in_)
    df = df.reindex(columns=expected)


    # Make prediction
    try:
        prediction = model.predict(df)
        prediction_proba = model.predict_proba(df)[0]
        prob_risco_1 = float(prediction_proba[1])

        return {
            "risco": int(prediction[0]),
            "probabilidade": prob_risco_1,
            "message": "Prediction successful"
    }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003, log_level="info")

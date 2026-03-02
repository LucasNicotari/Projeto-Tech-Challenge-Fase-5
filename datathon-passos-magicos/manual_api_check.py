import requests
import json
import sys

# Test data
data = {
    "RA": "RA-1",
    "Fase": 7,
    "Turma": "A",
    "Nome": "Aluno-1",
    "Ano_nasc": 2003.0,
    "Idade_22": 19.0,
    "Gênero": "Menina",
    "Ano_ingresso": 2016,
    "Instituição_de_ensino": "Escola Pública",
    "Pedra_20": "Ametista",
    "Pedra_21": "Ametista",
    "Pedra_22": "Quartzo",
    "INDE_22": 5.783,
    "Cg": 753.0,
    "Cf": 18.0,
    "Ct": 10.0,
    "No_Av": 4.0,
    "Avaliador1": "Avaliador-5",
    "Rec_Av1": "Mantido na Fase atual",
    "Avaliador2": "Avaliador-27",
    "Rec_Av2": "Promovido de Fase + Bolsa",
    "Avaliador3": "Avaliador-28",
    "Rec_Av3": "Promovido de Fase",
    "Avaliador4": "Avaliador-31",
    "Rec_Av4": "Mantido na Fase atual",
    "IAA": 8.3,
    "IEG": 4.1,
    "IPS": 5.6,
    "Rec_Psicologia": "Requer avaliação",
    "IDA": 4.0,
    "Matem": 2.7,
    "Portug": 3.5,
    "Inglês": 6.0,
    "Indicado": "Sim",
    "Atingiu_PV": "Não",
    "IPV": 7.278,
    "IAN": 5.0,
    "Fase_ideal": "Fase 8",
    "Destaque_IEG": "Melhorar",
    "Destaque_IDA": "Melhorar",
    "Destaque_IPV": "Melhorar",
    "Ano": 2022
}

try:
    # Make request
    response = requests.post("http://localhost:8002/predict", json=data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
except requests.exceptions.ConnectionError:
    print("Error: Could not connect to API. Make sure the server is running on port 8002.")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
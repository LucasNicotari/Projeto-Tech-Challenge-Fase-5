#  Datathon – Associação Passos Mágicos

## Predição de Risco de Defasagem Escolar

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-20.10+-blue.svg)](https://www.docker.com)

### 🎯 Visão Geral

Este projeto foi desenvolvido como parte do Datathon da Associação Passos Mágicos.

O objetivo principal é prever o risco de defasagem escolar de crianças e jovens com base nos dados históricos disponibilizados (2022, 2023 e 2024).

A solução utiliza técnicas de Machine Learning para classificar os alunos em:

- **0** → Sem risco
- **1** → Com risco de defasagem

Além do modelo preditivo, foi construída uma API utilizando FastAPI para disponibilizar as previsões de forma estruturada e pronta para integração com outros sistemas.

---

## 📁 Estrutura do Projeto

```
datathon-passos-magicos/
│
├── app/
│   ├── main.py              # API FastAPI
│   ├── __init__.py
│   └── artifacts/
│       └── model.joblib     # Modelo treinado salvo
│
├── src/
│   ├── data_io.py
│   ├── preprocessing.py
│   ├── train.py
│   └── build_dataset.py
│
├── data/
│   ├── dataset_unificado.csv
│   └── dataset_modelo.csv
│
├── tests/
│   ├── test_health.py
│   ├── test_predict.py
│   └── conftest.py
│
├── Dockerfile
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## 🎯 Entendimento do Problema

A tarefa consiste em identificar alunos com risco de defasagem escolar com base em variáveis como:

- **Indicadores pedagógicos** (INDE, IEG, IPS, IDA, IPV)
- **Avaliações**
- **Fase escolar**
- **Informações demográficas**
- **Dados históricos**

A modelagem foi estruturada como um problema de classificação binária supervisionada.

---

## 🔄 Pipeline de Machine Learning

O fluxo foi dividido em etapas bem definidas:

### 4.1 Unificação dos dados

Os dados de 2022, 2023 e 2024 foram consolidados em um único dataset.

### 4.2 Criação da variável alvo

A variável de risco foi derivada da defasagem escolar, convertendo para:

- **1** → aluno com risco
- **0** → aluno sem risco

### 4.3 Pré-processamento

Foi utilizado ColumnTransformer com:

- `SimpleImputer(strategy="median")` para variáveis numéricas
- `SimpleImputer(strategy="most_frequent")` para categóricas
- `OneHotEncoder(handle_unknown="ignore")` para variáveis categóricas

O pré-processamento está integrado ao pipeline do modelo.

### 4.4 Modelo

Foi utilizado **Logistic Regression** (após testes comparativos).

**Motivos da escolha:**

- Interpretabilidade
- Boa performance
- Estabilidade
- Treinamento rápido

---

## 🚀 Treinamento do Modelo

Para treinar novamente:

```bash
python -m src.train
```

O modelo treinado é salvo automaticamente em:

```
app/artifacts/model.joblib
```

---

## 🌐 API – FastAPI

A API expõe dois endpoints principais:

### Health Check

```http
GET /health
```

**Resposta:**

```json
{
  "status": "ok"
}
```

### Predição

```http
POST /predict
```

**Formato esperado:**

```json
{
  "data": {
    "RA": "...",
    "Fase": ...,
    ...
  }
}
```

**Resposta:**

```json
{
  "risco": 1,
  "probabilidade": 0.92,
  "message": "Prediction successful"
}
```

---

## 🏃‍♂️ Executando Localmente

### Criar ambiente virtual

```bash
python -m venv .venv
```

### Ativar

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux/MacOS:**

```bash
source .venv/bin/activate
```

### Instalar dependências

```bash
pip install -r requirements.txt
```

### Rodar API

```bash
uvicorn app.main:app --reload --port 8004
```

### Acessar

[http://127.0.0.1:8004/docs](http://127.0.0.1:8004/docs)

---

## 🧪 Testes Automatizados

Executar testes:

```bash
pytest -q
```

Cobertura de código:

```bash
pytest --cov=app --cov-report=term-missing
```

**Cobertura atual:** 83%

Os testes validam:

- Endpoint `/health`
- Endpoint `/predict`
- Estrutura da resposta da API

---

## 🐳 Docker

### Build da imagem

```bash
docker build -t datathon-passos-magicos .
```

### Executar container

```bash
docker run --rm -p 8004:8000 datathon-passos-magicos
```

A API ficará disponível em:

[http://127.0.0.1:8004](http://127.0.0.1:8004)

---

## 💡 Principais Decisões Técnicas

- Uso de Pipeline para evitar vazamento de dados
- Reindexação das features na API para garantir alinhamento com o treino
- Tratamento de valores ausentes via imputação
- Conversão de NaN para None na camada de testes
- Testes automatizados cobrindo os endpoints principais
- Containerização para facilitar deploy

---

## 📝 Considerações Finais

O projeto foi estruturado buscando:

- Clareza no fluxo de dados
- Reprodutibilidade
- Organização modular
- Facilidade de deploy
- Testabilidade

A solução está pronta para ser integrada em ambiente produtivo, podendo evoluir com monitoramento de drift e ajustes de modelo conforme novos dados sejam disponibilizados.

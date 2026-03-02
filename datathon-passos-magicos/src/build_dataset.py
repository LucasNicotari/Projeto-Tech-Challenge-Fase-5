import pandas as pd
from src.data_io import load_data

def main():
    sheets = load_data()

    # 1) pega cada aba
    df22 = sheets["PEDE2022"].copy()
    df23 = sheets["PEDE2023"].copy()
    df24 = sheets["PEDE2024"].copy()

    # 2) cria coluna Ano (para identificar)
    df22["Ano"] = 2022
    df23["Ano"] = 2023
    df24["Ano"] = 2024

    # 3) padroniza o nome do target (alvo)
    df22["Target"] = df22["Defas"]
    df23["Target"] = df23["Defasagem"]
    df24["Target"] = df24["Defasagem"]

    # 4) remove as colunas originais para não duplicar informação
    df22 = df22.drop(columns=["Defas"], errors="ignore")
    df23 = df23.drop(columns=["Defasagem"], errors="ignore")
    df24 = df24.drop(columns=["Defasagem"], errors="ignore")

    # 5) junta tudo
    df_all = pd.concat([df22, df23, df24], ignore_index=True)

    # 6) salva em CSV "limpo" para o modelo
    df_all.to_csv("data/dataset_unificado.csv", index=False)

    print("✅ Dataset unificado salvo em: data/dataset_unificado.csv")
    print("Linhas e colunas:", df_all.shape)
    print("Distribuição do Target:")
    print(df_all["Target"].value_counts(dropna=False))

if __name__ == "__main__":
    main()

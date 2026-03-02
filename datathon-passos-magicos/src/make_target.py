import pandas as pd

def main():
    df = pd.read_csv("data/dataset_unificado.csv")

    # cria coluna Risco (0/1)
    df["Risco"] = (df["Target"] < 0).astype(int)

    # salva dataset pronto para o modelo
    df.to_csv("data/dataset_modelo.csv", index=False)

    print("✅ Dataset do modelo salvo em: data/dataset_modelo.csv")
    print("Distribuição do Risco (0=ok, 1=defasado):")
    print(df["Risco"].value_counts())

if __name__ == "__main__":
    main()

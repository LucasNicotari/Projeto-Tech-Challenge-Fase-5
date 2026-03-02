from src.data_io import load_data

def main():
    sheets = load_data()
    print("Abas encontradas (sheets):", list(sheets.keys()))

    for name, df in sheets.items():
        cols_defas = [c for c in df.columns if "defas" in c.lower()]
        print("\n==============================")
        print("ABA:", name)
        print("Linhas e colunas:", df.shape)
        print("Colunas com 'defas':", cols_defas)

if __name__ == "__main__":
    main()

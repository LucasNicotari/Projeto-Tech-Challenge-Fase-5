import pandas as pd
from .config import settings

def load_data(path=None) -> dict[str, pd.DataFrame]:
    """
    Retorna um dicionário:
    - chave = nome da aba (sheet)
    - valor = dataframe (tabela) daquela aba
    """
    p = path if path is not None else settings.DATA_PATH
    xls = pd.ExcelFile(p)
    return {sheet: xls.parse(sheet) for sheet in xls.sheet_names}

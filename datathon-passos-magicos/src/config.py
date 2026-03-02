from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Settings:
    DATA_PATH: Path = Path("data/dataset_modelo.csv")
    TARGET_COL: str = "Risco"

    # Colunas para remover (não usar no modelo)
    DROP_COLS: tuple[str, ...] = (
        "Nome",
        "Nome Anonimizado",
        "Target",
        "IAN",
    )

    RANDOM_STATE: int = 42

settings = Settings()

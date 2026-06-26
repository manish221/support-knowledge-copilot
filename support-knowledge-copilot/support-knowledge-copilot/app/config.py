from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    project_root: Path = Path(__file__).resolve().parents[1]
    storage_dir: Path = Path("storage")
    chunk_store_path: Path = Path("storage/chunks.jsonl")
    dense_index_path: Path = Path("storage/dense_index.joblib")
    sparse_index_path: Path = Path("storage/sparse_index.joblib")
    top_k_dense: int = 20
    top_k_sparse: int = 20
    top_k_final: int = 5
    rrf_k: int = 60
    min_confidence: float = 0.35

settings = Settings()

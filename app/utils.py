from __future__ import annotations
from pathlib import Path
import shutil
import pandas as pd

def save_uploaded_file(uploaded_file, dest_dir: Path) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / uploaded_file.name
    with dest.open('wb') as f:
        f.write(uploaded_file.getbuffer())
    return dest

def ensure_project_dirs(project_root: Path):
    for sub in ["inputs", "config", "results", "logs"]:
        (project_root / sub).mkdir(parents=True, exist_ok=True)

def read_table_preview(path: Path, n: int = 5) -> pd.DataFrame:
    if path.suffix.lower() in [".csv"]:
        return pd.read_csv(path).head(n)
    else:
        # assume tsv
        return pd.read_csv(path, sep="\t").head(n)

def which(cmd: str) -> str | None:
    return shutil.which(cmd)

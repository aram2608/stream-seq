from __future__ import annotations
from pathlib import Path
import shutil
import pandas as pd
import streamlit as st

def save_uploaded_file(uploaded_file, dest_dir: Path) -> Path:
    """Saves input files to project folders."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / uploaded_file.name
    with dest.open("wb") as f:
        f.write(uploaded_file.getbuffer())
    return dest

def ensure_project_dirs(project_root: Path):
    """Helper function to ensure all project directories are created."""
    for sub in ["inputs", "config", "results", "logs"]:
        (project_root / sub).mkdir(parents=True, exist_ok=True)

def ensure_project_dirs(project_root: Path):
    """Helper function to ensure all project directories are created."""
    for sub in ["files", "renamed", "formatted"]:
        (project_root / sub).mkdir(parents=True, exist_ok=True)

def read_table_preview(path: Path, n: int = 5) -> pd.DataFrame:
    """Helper function to preview input tables."""
    if path.suffix.lower() in [".csv"]:
        return pd.read_csv(path).head(n)
    else:
        # assume tsv
        return pd.read_csv(path, sep="\t").head(n)

def read_table_wiz(path: Path, n: int = 20) -> pd.DataFrame:
    """Helper function to read in tables for file wiz."""
    if path.suffix.lower() in [".csv"]:
        return pd.read_csv(path).head(n)
    else:
        return pd.read_csv(path, sep="\t").head(n)

def which(cmd: str) -> str | None:
    """
    Helper function that wraps shutils.which() command.
    Finds the absolute path of a command from the PATH env variable and returns it as a string.
    """
    return shutil.which(cmd)

from __future__ import annotations
import subprocess, sys
from pathlib import Path


def run_r_engine(
    rscript_path: Path, config_json: Path, workdir: Path | None = None
) -> subprocess.CompletedProcess:
    """Helper function to run the R engine for analysis."""
    cmd = ["Rscript", str(rscript_path), str(config_json)]
    result = subprocess.run(
        cmd, cwd=workdir, text=True, capture_output=True, check=False
    )
    return result

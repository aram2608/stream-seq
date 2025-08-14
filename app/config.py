from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
import json


@dataclass
class AnalysisConfig:
    """A data class to represent the configuration file used in the R engine."""
    counts: str
    samples: str
    design: str
    outdir: str
    species: str | None = None
    use_tximport: bool = False
    tximport_dir: str | None = None

    def write_json(self, path: str | Path):
        """Helper function to write JSON config file."""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w") as f:
            json.dump(asdict(self), f, indent=2)
        return p

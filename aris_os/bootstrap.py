"""Reusable v0.2 project bootstrap.

``bootstrap_project_v02`` creates governance scaffolding for an existing
project without touching scientific data and without inferring or freezing
scientific definitions.  Those definitions remain placeholders until a human
reviews them.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Dict, List


def package_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _copy_if_missing(src: Path, dst: Path) -> bool:
    if dst.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.exists():
        shutil.copy2(src, dst)
    else:
        dst.touch()
    return True


def _template(name: str) -> Path:
    return package_root() / "templates" / name


def bootstrap_project_v02(root: str | Path) -> Dict[str, object]:
    """Generate governance scaffolding under an existing project root."""
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)

    created: List[str] = []
    skipped: List[str] = []

    # Directory scaffolding.
    for rel in (
        "governance",
        "design",
        "data_contract",
        "analysis",
        "freezes",
        "manuscript",
        "audits",
        "incidents",
        "archive",
    ):
        d = root / rel
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)
            created.append(str(d.relative_to(root)))

    # Root identity / navigational files.
    mappings = {
        root / "PROJECT_IDENTITY.yaml": _template("PROJECT_IDENTITY.yaml"),
        root / "PROJECT_STATUS.md": _template("PROJECT_STATUS.md"),
        root / "MASTER_INDEX.md": _template("MASTER_INDEX.md"),
    }
    for dst, src in mappings.items():
        if _copy_if_missing(src, dst):
            created.append(str(dst.relative_to(root)))
        else:
            skipped.append(str(dst.relative_to(root)))

    # Governance files.
    gov_mappings = {
        root / "governance" / "CONSTRAINTS.yaml": _template("CONSTRAINTS.yaml"),
        root / "governance" / "PROJECT_NAMESPACE.yaml": _template("PROJECT_NAMESPACE.yaml"),
        root / "governance" / "DECISION_REGISTER.md": _template("DECISION_REGISTER.md"),
        root / "governance" / "GATE_REGISTER.md": _template("GATE_REGISTER.md"),
        root / "governance" / "INCIDENT_REGISTER.md": _template("INCIDENT_REGISTER.md"),
    }
    for dst, src in gov_mappings.items():
        if _copy_if_missing(src, dst):
            created.append(str(dst.relative_to(root)))
        else:
            skipped.append(str(dst.relative_to(root)))

    # Non-template governance files that need an initial skeleton.
    for name in ("DESIGN_CHANGELOG.md", "MASTER_LOG.md"):
        dst = root / "governance" / name
        if not dst.exists():
            dst.write_text(f"# {name.replace('.md', '').replace('_', ' ')}\n\n", encoding="utf-8")
            created.append(str(dst.relative_to(root)))
        else:
            skipped.append(str(dst.relative_to(root)))

    return {
        "root": str(root),
        "created": created,
        "skipped": skipped,
        "note": (
            "Scientific definitions in PROJECT_IDENTITY.yaml and CONSTRAINTS.yaml "
            "are placeholders. A human must review them before substantive execution."
        ),
    }


def read_identity(root: str | Path) -> Dict[str, object]:
    """Read PROJECT_IDENTITY.yaml from a project root."""
    from .governance import parse_simple_yaml

    path = Path(root) / "PROJECT_IDENTITY.yaml"
    if not path.exists():
        return {}
    return parse_simple_yaml(path.read_text(encoding="utf-8"))

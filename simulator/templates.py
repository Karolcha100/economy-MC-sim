"""Templates: developer-defined schemas that every formula row must follow.

Each template is `simulator/common/templates/<kind>.csv`, one row per field.
Users never edit templates; they edit formulas (see `formulas.py`).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from simulator.io import SimulatorError, read_csv, slugify

TEMPLATES_DIR = Path(__file__).parent / "common" / "templates"

INTERNAL_GRADES = "internal-grades"
RELATIONS_DIRECTED = "relations-directed"
RELATIONS_DOUBLESIDED = "relations-doublesided"
KINDS = (INTERNAL_GRADES, RELATIONS_DIRECTED, RELATIONS_DOUBLESIDED)
RELATION_KINDS = (RELATIONS_DIRECTED, RELATIONS_DOUBLESIDED)

KIND_ALIASES = {
    "internal-grades": INTERNAL_GRADES,
    "internal-grade": INTERNAL_GRADES,
    "grades": INTERNAL_GRADES,
    "grade": INTERNAL_GRADES,
    "relations-directed": RELATIONS_DIRECTED,
    "relation-directed": RELATIONS_DIRECTED,
    "directed": RELATIONS_DIRECTED,
    "relations-doublesided": RELATIONS_DOUBLESIDED,
    "relation-doublesided": RELATIONS_DOUBLESIDED,
    "doublesided": RELATIONS_DOUBLESIDED,
    "double-sided": RELATIONS_DOUBLESIDED,
}

VALUE_TYPES = ("float", "int")
# Entity kinds allowed on the sides of a relation. TAG = a country from tags.csv.
ENTITY_KINDS = ("TAG",)
ENTITY_FIELDS = {
    INTERNAL_GRADES: (),
    RELATIONS_DIRECTED: ("from", "to"),
    RELATIONS_DOUBLESIDED: ("side-a", "side-b"),
}


def resolve_kind(kind: str) -> str:
    try:
        return KIND_ALIASES[kind.strip().lower()]
    except KeyError:
        raise SimulatorError(f"Unknown kind {kind!r}. Use one of: {', '.join(KINDS)}") from None


@dataclass(frozen=True)
class Template:
    kind: str
    fields: pd.DataFrame  # columns: field, dtype, required, description

    @property
    def field_names(self) -> list[str]:
        return self.fields["field"].tolist()

    @property
    def entity_fields(self) -> tuple[str, ...]:
        return ENTITY_FIELDS[self.kind]


def load_template(kind: str, templates_dir: Path = TEMPLATES_DIR) -> Template:
    kind = resolve_kind(kind)
    path = templates_dir / f"{kind}.csv"
    if not path.exists():
        raise SimulatorError(f"Template file missing: {path}")
    return Template(kind=kind, fields=read_csv(path, dtype=str, keep_default_na=False))


def validate_formulas(template: Template, formulas: pd.DataFrame) -> list[str]:
    """Return a list of problems (empty = valid) of a formulas table against its template."""
    errors: list[str] = []
    if list(formulas.columns) != template.field_names:
        return [
            f"[{template.kind}] formula columns {list(formulas.columns)} "
            f"do not match template fields {template.field_names}"
        ]

    seen_slugs: dict[str, str] = {}
    for _, row in formulas.iterrows():
        name = str(row["name"]).strip()
        where = f"[{template.kind}] formula {name!r}"
        slug = slugify(name)
        if not name or not slug:
            errors.append(f"{where}: empty or invalid name")
            continue
        if name != name.lower():
            errors.append(f"{where}: name must be lowercase")
        if slug in seen_slugs:
            errors.append(f"{where}: name collides with {seen_slugs[slug]!r} (same slug {slug!r})")
        seen_slugs[slug] = name

        if row["type"] not in VALUE_TYPES:
            errors.append(f"{where}: type {row['type']!r} not in {VALUE_TYPES}")
        try:
            vmin, vmax = float(row["valmin"]), float(row["valmax"])
        except (TypeError, ValueError):
            errors.append(f"{where}: valmin/valmax must be numbers")
        else:
            if not vmin < vmax:
                errors.append(f"{where}: valmin ({vmin}) must be < valmax ({vmax})")
            if row["type"] == "int" and not (vmin.is_integer() and vmax.is_integer()):
                errors.append(f"{where}: int formula needs integer valmin/valmax")

        for field in template.entity_fields:
            if row[field] not in ENTITY_KINDS:
                errors.append(f"{where}: {field} = {row[field]!r} not in {ENTITY_KINDS}")
    return errors

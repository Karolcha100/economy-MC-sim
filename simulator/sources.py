"""Readers for external data sources (country-year tables and dyadic country-pair data).

Country-year readers return a frame: rows = years, columns = ISO3 country codes.
Dyadic readers return a long frame: date, side_a, side_b, value.
Each raw file lives in `data/<source>/` with a README describing where it came from.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from simulator.io import ENCODING, SimulatorError, read_csv

DYAD_COLUMNS = ["date", "side_a", "side_b", "value"]

# Sheets of the official WGI file (https://www.worldbank.org/content/dam/sites/govindicators/doc/wgidataset.xlsx).
WGI_SHEETS = {
    "pv": "Political StabilityNoViolence",
    "cc": "ControlofCorruption",
    "va": "VoiceandAccountability",
    "ge": "GovernmentEffectiveness",
    "rq": "RegulatoryQuality",
    "rl": "RuleofLaw",
}

# Gleditsch-Ward codes that country_converter does not know or maps differently.
GW_OVERRIDES = {816: "VNM", 260: "DEU", 316: "CZE", 345: "SRB", 678: "YEM", 365: "RUS", 347: "XKX", 713: "TWN"}


# --- country-year -----------------------------------------------------------------------

def read_owid(path: Path, column: str | None = None) -> pd.DataFrame:
    """Our World in Data grapher CSV (entity, code, year, <value>, ...). Rows without ISO3 code are aggregates."""
    df = read_csv(path)
    missing = {"code", "year"} - set(df.columns)
    if missing:
        raise SimulatorError(f"{path}: not an OWID grapher CSV (missing {sorted(missing)})")
    if column is None:
        candidates = [c for c in df.columns if c not in ("entity", "code", "year", "owid_region")]
        if len(candidates) != 1:
            raise SimulatorError(f"{path}: pick a value column with --column, one of {candidates}")
        column = candidates[0]
    df = df[df["code"].astype(str).str.fullmatch(r"[A-Z]{3}")]
    return df.pivot_table(index="year", columns="code", values=column, aggfunc="first").sort_index()


def read_wgi_xlsx(path: Path, sheet: str) -> pd.DataFrame:
    """Official WGI workbook: per sheet a header row of years and a row of fields (Estimate, StdErr, ...)."""
    sheet_name = WGI_SHEETS.get(sheet, sheet)
    try:
        raw = pd.read_excel(path, sheet_name=sheet_name, header=None)
    except (ValueError, OSError) as e:
        raise SimulatorError(f"{path}: cannot read sheet {sheet_name!r} ({e}); sheets: {sorted(WGI_SHEETS)}") from None
    field_row = raw.index[raw.eq("Code").any(axis=1)][0]
    years, fields = raw.iloc[field_row - 1], raw.iloc[field_row]
    code_col = int(fields[fields == "Code"].index[0])
    data = raw.iloc[field_row + 1:]
    out = {
        int(years[c]): pd.to_numeric(data[c], errors="coerce").values
        for c in raw.columns if fields[c] == "Estimate"
    }
    return pd.DataFrame(out, index=data[code_col].astype(str).values).T.sort_index()


# --- dyadic -----------------------------------------------------------------------------

def read_geonames_neighbours(path: Path, years: list[int]) -> pd.DataFrame:
    """GeoNames countryInfo.txt: 'neighbours' = countries sharing a land border (today's borders)."""
    rows = [line.rstrip("\n").split("\t") for line in path.read_text(encoding=ENCODING).splitlines()
            if line and not line.startswith("#")]
    iso2_to_iso3 = {r[0]: r[1] for r in rows}
    pairs = set()
    for r in rows:
        if len(r) > 17 and r[17]:
            for n in r[17].split(","):
                if n in iso2_to_iso3:
                    pairs.add(tuple(sorted((r[1], iso2_to_iso3[n]))))
    return pd.DataFrame(
        [(y, a, b, 1.0) for y in years for a, b in sorted(pairs)], columns=DYAD_COLUMNS
    )


def read_pair_ranges(path: Path) -> pd.DataFrame:
    """Hand-made pairs valid for a range of years: side_a, side_b, from, to[, note] -> value 1."""
    df = read_csv(path, dtype={"side_a": str, "side_b": str})
    missing = {"side_a", "side_b", "from", "to"} - set(df.columns)
    if missing:
        raise SimulatorError(f"{path}: missing columns {sorted(missing)}")
    rows = []
    for _, r in df.iterrows():
        a, b = sorted((r["side_a"], r["side_b"]))
        rows += [(y, a, b, 1.0) for y in range(int(r["from"]), int(r["to"]) + 1)]
    return pd.DataFrame(rows, columns=DYAD_COLUMNS)


def _gw_to_iso3(codes: pd.Series) -> dict[int, str]:
    import logging

    import country_converter as coco

    logging.getLogger("country_converter").setLevel(logging.ERROR)  # unknown codes are handled below
    unique = sorted({int(c) for c in codes})
    converted = coco.CountryConverter().convert(unique, src="GWcode", to="ISO3", not_found=None)
    # country_converter returns the input unchanged when it does not know a code
    mapping = {c: iso for c, iso in zip(unique, converted) if isinstance(iso, str) and iso.isalpha()}
    mapping.update({c: iso for c, iso in GW_OVERRIDES.items() if c in unique})
    return mapping


def read_ucdp_dyadic(path: Path, min_year: int | None = None) -> pd.DataFrame:
    """UCDP Dyadic dataset -> pairs of governments fighting on opposite sides in a year.

    value 2 = both are primary parties of an interstate conflict (type 2),
    value 1 = at least one of them only as a secondary warring party (troops), e.g. Russia
    supporting DPR/LPR against Ukraine 2014-2021. The highest value of the year is kept.
    """
    df = read_csv(path, dtype=str)
    df["year"] = df["year"].astype(int)
    if min_year is not None:
        df = df[df["year"] >= min_year]

    def codes(cell) -> list[int]:
        return [int(c) for c in str(cell).replace(" ", "").split(",") if c and c != "nan"]

    sides = []
    for _, r in df.iterrows():
        a_primary, b_primary = codes(r["gwno_a"]), codes(r["gwno_b"])
        a_all, b_all = a_primary + codes(r["gwno_a_2nd"]), b_primary + codes(r["gwno_b_2nd"])
        for a in a_all:
            for b in b_all:
                if a == b:
                    continue
                level = 2 if (a in a_primary and b in b_primary and r["type_of_conflict"] == "2") else 1
                sides.append((r["year"], a, b, level))
    if not sides:
        return pd.DataFrame(columns=DYAD_COLUMNS)
    raw = pd.DataFrame(sides, columns=["date", "a", "b", "value"])
    mapping = _gw_to_iso3(pd.concat([raw["a"], raw["b"]]))
    unknown = sorted(set(raw["a"]).union(raw["b"]) - set(mapping))
    if unknown:
        raise SimulatorError(f"Unknown Gleditsch-Ward codes {unknown}; add them to GW_OVERRIDES")
    raw["a"], raw["b"] = raw["a"].map(mapping), raw["b"].map(mapping)
    raw = raw[raw["a"] != raw["b"]]
    ordered = raw[["a", "b"]].apply(sorted, axis=1, result_type="expand")
    raw["side_a"], raw["side_b"] = ordered[0], ordered[1]
    out = raw.groupby(["date", "side_a", "side_b"], as_index=False)["value"].max()
    return out[DYAD_COLUMNS].astype({"value": float})

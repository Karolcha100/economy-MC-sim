"""Command line interface: `python -m simulator --scenario NAME <command> ...`.

Run `python -m simulator --help` or `python -m simulator <command> --help` for details.
Exit code: 0 = ok, 1 = invalid input / validation errors.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import pandas as pd

from simulator import formulas as fm
from simulator import history, narrated
from simulator.interpolation import CURVES
from simulator.io import SimulatorError
from simulator.scenario import Scenario
from simulator.templates import KINDS, load_template
from simulator.validate import validate

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 50)
pd.set_option("display.max_rows", 500)


def _print_table(df: pd.DataFrame, as_json: bool) -> None:
    if as_json:
        print(df.reset_index().to_json(orient="records", force_ascii=False))
    else:
        print(df.to_string())


def _start_value(text: str) -> float | str:
    return text if text.strip().lower() == narrated.CURRENT else float(text)


def _param(text: str) -> tuple[str, float]:
    key, sep, value = text.partition("=")
    if not sep:
        raise argparse.ArgumentTypeError(f"param must be key=value, got {text!r}")
    return key.strip(), float(value)


def _floats(text: str) -> list[float]:
    return [float(v) for v in text.split(",") if v.strip()]


def _add_set_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--kind", required=True, help=f"one of {KINDS} (aliases: grade, directed, doublesided)")
    p.add_argument("--name", required=True, help="formula name or slug, e.g. 'war exhaustion'")
    p.add_argument("--targets", required=True,
                   help="comma separated; grades: POL,DEU; relations: POL:RUS,DEU:RUS")
    p.add_argument("--years", required=True, help="closed interval '1990-2000' or a single year '1995'")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m simulator", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--scenario", default=os.environ.get("SIMULATOR_SCENARIO"),
                        help="scenario name (in simulator/scenarios) or path; env SIMULATOR_SCENARIO")
    parser.add_argument("--json", action="store_true", help="print tables as JSON records")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("tags", help="list tags with existence windows")
    sub.add_parser("dates", help="list scenario dates")
    sub.add_parser("validate", help="check the whole scenario")

    # formulas
    pf = sub.add_parser("formulas", help="list/add/edit/remove formulas").add_subparsers(dest="action", required=True)
    p = pf.add_parser("list")
    p.add_argument("--kind", help="limit to one kind")
    p = pf.add_parser("template", help="show the template fields of a kind")
    p.add_argument("--kind", required=True)
    p = pf.add_parser("add")
    p.add_argument("--kind", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--type", required=True, choices=["float", "int"])
    p.add_argument("--valmin", required=True, type=float)
    p.add_argument("--valmax", required=True, type=float)
    p = pf.add_parser("edit", help="rename / change type or range; migrates narrated data")
    p.add_argument("--kind", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--rename")
    p.add_argument("--type", choices=["float", "int"])
    p.add_argument("--valmin", type=float)
    p.add_argument("--valmax", type=float)
    p.add_argument("--clip", action="store_true", help="round/clip existing values into the new definition")
    p = pf.add_parser("remove")
    p.add_argument("--kind", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--purge", action="store_true", help="also delete existing narrated data")
    for p in (pf.choices["add"], pf.choices["edit"], pf.choices["remove"]):
        p.add_argument("--author", default="user")
        p.add_argument("--rationale", default="")

    # set
    p = sub.add_parser("set", help="fill values of one formula with a change curve",
                       description=f"Curves: {', '.join(CURVES)}. Params: exponential k=3; "
                                   "logistic steepness=10 midpoint=0.5; step midpoint=0.5.")
    _add_set_args(p)
    p.add_argument("--curve", default="linear", choices=CURVES)
    p.add_argument("--start", type=_start_value, help="start value or 'current' (existing value in first year)")
    p.add_argument("--end", type=float, help="end value (not needed for constant)")
    p.add_argument("--values", type=_floats, help="manual curve: comma separated value per year")
    p.add_argument("--param", type=_param, action="append", default=[], help="curve parameter key=value")
    p.add_argument("--only-empty", action="store_true", help="do not overwrite filled cells")
    p.add_argument("--clip", action="store_true", help="clip values into [valmin, valmax] instead of failing")
    p.add_argument("--author", required=True, help="who sets the values (model name or 'user')")
    p.add_argument("--rationale", default="", help="why / based on what (recommended)")
    p.add_argument("--dry-run", action="store_true", help="show computed values, write nothing")

    # batch
    p = sub.add_parser("batch", help="apply a JSON list of operations (all-or-nothing)")
    p.add_argument("file", type=Path, help="JSON: list of operations or {'operations': [...], 'rationale': ...}")
    p.add_argument("--author", required=True)
    p.add_argument("--rationale", default="")
    p.add_argument("--dry-run", action="store_true")

    # show / missing
    p = sub.add_parser("show", help="print current values (years x targets)")
    _add_set_args(p)
    p = sub.add_parser("missing", help="how much of each formula is filled")
    p.add_argument("--kind")
    p.add_argument("--name")

    # history
    ph = sub.add_parser("history", help="real statistics").add_subparsers(dest="action", required=True)
    ph.add_parser("list")
    p = ph.add_parser("import")
    p.add_argument("--name", required=True, help="statistic name, e.g. gdp-current-usd")
    p.add_argument("--source-file", required=True, type=Path)
    p.add_argument("--format", default="worldbank", choices=history.FORMATS)
    p.add_argument("--unit", default="")
    p.add_argument("--source", default="")
    p.add_argument("--source-code", default="")
    p.add_argument("--downloaded", default="", help="download date, YYYY-MM-DD")
    p.add_argument("--description", default="")
    p.add_argument("--scale", type=float, default=1.0, help="multiply values (e.g. 1e-9 for billions)")
    return parser


def _print_results(results: list[narrated.Result], dry_run: bool, as_json: bool) -> None:
    for r in results:
        print(f"# {r.formula.kind} {r.formula.name!r}: "
              f"{'would write' if dry_run else 'written'} {r.written}, skipped (filled) {r.skipped}")
        _print_table(r.preview, as_json)
    if dry_run:
        print("# dry run: nothing written")


def run(args: argparse.Namespace) -> int:
    if not args.scenario:
        raise SimulatorError("--scenario is required (or set SIMULATOR_SCENARIO)")
    scenario = Scenario.open(args.scenario)

    match args.command:
        case "tags":
            _print_table(scenario.tags_table, args.json)
        case "dates":
            print(",".join(map(str, scenario.dates)))
        case "validate":
            issues = validate(scenario)
            for issue in issues:
                print(issue)
            errors = sum(i.level == "error" for i in issues)
            print(f"# {errors} error(s), {len(issues) - errors} warning(s)")
            return 1 if errors else 0
        case "formulas":
            if args.action == "list":
                kinds = KINDS if args.kind is None else (args.kind,)
                for kind in kinds:
                    print(f"# {kind}")
                    _print_table(fm.load_table(scenario, kind), args.json)
            elif args.action == "template":
                _print_table(load_template(args.kind).fields, args.json)
            elif args.action == "add":
                f = fm.add_formula(scenario, args.kind, args.name, args.type, args.valmin, args.valmax,
                                   author=args.author, rationale=args.rationale)
                print(f"added {f}")
            elif args.action == "edit":
                f = fm.edit_formula(scenario, args.kind, args.name, args.rename, args.type,
                                    args.valmin, args.valmax, args.clip, args.author, args.rationale)
                print(f"edited -> {f}")
            elif args.action == "remove":
                f = fm.remove_formula(scenario, args.kind, args.name, args.purge, args.author, args.rationale)
                print(f"removed {f}")
        case "set":
            op = narrated.Operation(
                kind=args.kind, name=args.name, targets=args.targets, years=args.years,
                curve=args.curve, start=args.start, end=args.end, values=args.values,
                params=dict(args.param), only_empty=args.only_empty, clip=args.clip,
            )
            results = narrated.apply_operations(scenario, [op], args.author, args.rationale, args.dry_run)
            _print_results(results, args.dry_run, args.json)
        case "batch":
            try:
                data = json.loads(args.file.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as e:
                raise SimulatorError(f"Cannot read {args.file}: {e}") from None
            rationale = args.rationale
            if isinstance(data, dict):
                rationale = rationale or data.get("rationale", "")
                data = data.get("operations", [])
            ops = [narrated.Operation.from_dict(d) for d in data]
            results = narrated.apply_operations(scenario, ops, args.author, rationale, args.dry_run)
            _print_results(results, args.dry_run, args.json)
        case "show":
            _print_table(narrated.show(scenario, args.kind, args.name, args.targets, args.years), args.json)
        case "missing":
            _print_table(narrated.missing_report(scenario, args.kind, args.name), args.json)
        case "history":
            if args.action == "list":
                _print_table(history.load_metadata(scenario), args.json)
            else:
                report = history.import_history(
                    scenario, args.name, args.source_file, args.format, args.unit, args.source,
                    args.source_code, args.downloaded, args.description, args.scale,
                )
                incomplete = report[report["filled"] < report["total"]]
                print(f"# imported {args.name}: {len(report)} tags, {int(report['filled'].sum())} values, "
                      f"{report.attrs['ignored_columns']} source columns ignored (not in tags.csv)")
                print(f"# {len(incomplete)} tag(s) with gaps")
                if not incomplete.empty:
                    _print_table(incomplete, args.json)
    return 0


def _hoist_global_options(argv: list[str]) -> list[str]:
    """Allow --scenario/--json anywhere on the command line, not only before the command."""
    front: list[str] = []
    rest: list[str] = []
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg == "--json" or arg.startswith("--scenario="):
            front.append(arg)
        elif arg == "--scenario" and i + 1 < len(argv):
            front += [arg, argv[i + 1]]
            i += 1
        else:
            rest.append(arg)
        i += 1
    return front + rest


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    args = build_parser().parse_args(_hoist_global_options(argv))
    try:
        return run(args)
    except SimulatorError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

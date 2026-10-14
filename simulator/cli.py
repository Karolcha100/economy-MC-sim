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
from simulator.context import context
from simulator.review import DEFAULT_JUMP, DEFAULT_SEED_DEVIATION, review
from simulator.seed import apply_seeds, load_rules, reset_seeded
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
                   help="comma separated; grades: POL,DEU; relations: POL:RUS,DEU:RUS; "
                        "groups/wildcard: @NATO, @EU:RUS, POL:*")
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
    sub.add_parser("groups", help="list groups (@NAME targets) and their members by year")

    p = sub.add_parser("context", help="compact context for an LLM: a country (POL) or a pair (POL:RUS)")
    p.add_argument("target")
    p = sub.add_parser("review", help="warnings: big year-to-year jumps, writes without rationale")
    p.add_argument("--kind")
    p.add_argument("--name")
    p.add_argument("--jump", type=float, default=DEFAULT_JUMP, help="share of the value range (default 0.25)")
    p.add_argument("--seed-deviation", type=float, default=DEFAULT_SEED_DEVIATION,
                   help="warn when a value is this many points away from its seed (default 15)")
    p = sub.add_parser("seed", help="write seed values from real indicators into empty cells (rules: seeds.csv)")
    p.add_argument("--name", help="only the rule(s) of this formula")
    p.add_argument("--reset", action="store_true",
                   help="with --name: first delete the formula's values (only if nothing but seeds wrote them)")
    p.add_argument("--dry-run", action="store_true")
    p = sub.add_parser("reference-map", help="world map of a statistic for reference countries (HTML)")
    p.add_argument("--kind", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--focus", help="relations: show FOCUS -> country")
    p.add_argument("--years", help="e.g. 1990-2025 (default: all dates)")
    p.add_argument("--all", action="store_true", help="all countries, not only reference ones")
    p.add_argument("--out", type=Path, help="HTML file (default: <scenario>/views/<name>.html)")
    p.add_argument("--no-open", action="store_true", help="do not open a browser")

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
    p.add_argument("--description", required=True, help="one-sentence meaning and scale, read by LLMs")
    p.add_argument("--default", type=float, help="value assumed for unfilled cells (omit = must be filled)")
    p = pf.add_parser("edit", help="rename / change type, range, default, description; migrates narrated data")
    p.add_argument("--kind", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--rename")
    p.add_argument("--type", choices=["float", "int"])
    p.add_argument("--valmin", type=float)
    p.add_argument("--valmax", type=float)
    p.add_argument("--default", help="new default; '' removes it")
    p.add_argument("--description")
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
    p.add_argument("--sources", action="append", default=[],
                   help="URL or 'title, outlet, date' the values are based on (repeatable)")
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
    p = sub.add_parser("missing", help="how much of each formula is filled (values or confirmed defaults)")
    p.add_argument("--kind")
    p.add_argument("--name")
    p.add_argument("--by-country", action="store_true", help="percent filled per country and kind (worst first)")
    p = sub.add_parser("confirm-default", help="mark unfilled cells as deliberately default (P1, thread T011)")
    p.add_argument("--kind", required=True)
    p.add_argument("--name", required=True, help="formula name(s), comma separated, or 'all' (all with a default)")
    p.add_argument("--targets", required=True, help="tags: grades = those countries; relations = pairs FROM/with them")
    p.add_argument("--years", required=True)
    p.add_argument("--author", required=True)
    p.add_argument("--note", default="")
    p = sub.add_parser("drop-tags", help="remove countries from the whole scenario (decision A39 / K7)")
    p.add_argument("--tags", required=True, help="comma separated tags")
    p.add_argument("--author", required=True)
    p.add_argument("--note", default="")
    p = sub.add_parser("audit", help="compare narrated data of all countries with real indicators (rules: audit.csv)")
    p.add_argument("--out", type=Path, help="folder for the markdown report (default: <scenario>/views/)")
    p = sub.add_parser("queue", help="write the Phase 1.2b task queue (markdown) for filling agents")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--first", default="", help="tags to put right after the reference countries (e.g. Tier 1)")

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
    p.add_argument("--column", help="owid: value column when the file has several")
    p.add_argument("--sheet", help="wgi-xlsx: pv (political stability), cc (control of corruption), va, ge, rq, rl")
    p = ph.add_parser("import-dyadic", help="pairs of countries (history/dyadic/), e.g. borders, wars")
    p.add_argument("--name", required=True)
    p.add_argument("--source-file", required=True, type=Path)
    p.add_argument("--format", required=True, choices=history.DYADIC_FORMATS)
    for opt in ("--unit", "--source", "--source-code", "--downloaded", "--description"):
        p.add_argument(opt, default="")
    p = ph.add_parser("gaps", help="missing values in years a country exists")
    p.add_argument("--name", required=True)
    p = ph.add_parser("fill", help="fill gaps (never overwrites); every value is logged in history/fill-log.csv",
                      description="Typical order: --method source (other data), then interpolate, then extrapolate.")
    p.add_argument("--name", required=True)
    p.add_argument("--method", required=True, choices=history.FILL_METHODS)
    p.add_argument("--source-file", type=Path, help="method source: file with the same statistic")
    p.add_argument("--source-format", default="wide", choices=history.FORMATS)
    p.add_argument("--source-scale", type=float, default=1.0, help="e.g. 1e9 when the source is in billions")
    p.add_argument("--source-label", default="", help="written to the log, e.g. 'IMF WEO Apr 2026, NGDPD'")
    p.add_argument("--window", type=int, default=3, help="extrapolate: years used to estimate the growth")
    p.add_argument("--tags", help="limit to these tags (comma separated)")
    p.add_argument("--author", required=True)
    p.add_argument("--dry-run", action="store_true")
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
        case "groups":
            table = scenario.groups_table.copy()
            for c in ("from", "to"):
                table[c] = table[c].astype("Int64")
            _print_table(table.set_index(["group", "tag"]), args.json)
        case "context":
            print(context(scenario, args.target))
        case "review":
            warnings = review(scenario, args.kind, args.name, args.jump, args.seed_deviation)
            print(f"# {len(warnings)} warning(s)")
            if not warnings.empty:
                _print_table(warnings, args.json)
        case "seed":
            if args.reset:
                if not args.name or args.dry_run:
                    raise SimulatorError("--reset needs --name and cannot be combined with --dry-run")
                rule = load_rules(scenario, args.name)[0]
                print(f"# reset {args.name}: {reset_seeded(scenario, rule.kind, args.name)} cell(s) cleared")
            report = apply_seeds(scenario, args.name, args.dry_run)
            _print_table(report.set_index(["kind", "name", "source"]), args.json)
            if args.dry_run:
                print("# dry run: nothing written")
        case "reference-map":
            from simulator.reference_map import build_map, write_map

            fig = build_map(scenario, args.kind, args.name, args.years, args.focus, args.all)
            out = args.out or scenario.root / "views" / f"{fm.get_formula(scenario, args.kind, args.name).slug}"\
                f"{'-' + args.focus.lower() if args.focus else ''}.html"
            write_map(fig, out)
            print(f"# map written to {out}")
            if not args.no_open:
                import webbrowser

                webbrowser.open(out.resolve().as_uri())
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
                                   args.description, args.default,
                                   author=args.author, rationale=args.rationale)
                print(f"added {f}")
            elif args.action == "edit":
                f = fm.edit_formula(scenario, args.kind, args.name, args.rename, args.type,
                                    args.valmin, args.valmax, args.clip, args.author, args.rationale,
                                    args.default, args.description)
                print(f"edited -> {f}")
            elif args.action == "remove":
                f = fm.remove_formula(scenario, args.kind, args.name, args.purge, args.author, args.rationale)
                print(f"removed {f}")
        case "set":
            op = narrated.Operation(
                kind=args.kind, name=args.name, targets=args.targets, years=args.years,
                curve=args.curve, start=args.start, end=args.end, values=args.values,
                params=dict(args.param), only_empty=args.only_empty, clip=args.clip, sources=args.sources,
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
            _print_table(narrated.missing_report(scenario, args.kind, args.name, args.by_country), args.json)
        case "confirm-default":
            n = narrated.confirm_default(scenario, args.kind, args.name, args.targets, args.years, args.author, args.note)
            print(f"# confirmed defaults: {n} row(s)")
        case "drop-tags":
            from simulator.drop import drop_tags

            changed = drop_tags(scenario, args.tags, args.author, args.note)
            print("# dropped; files changed: " + ", ".join(f"{k} {v}" for k, v in changed.items()))
        case "audit":
            from simulator.audit import run_audit, write_report

            result = run_audit(scenario)
            _print_table(result["summary"].set_index("statistic"), args.json)
            print(f"# outliers: {len(result['outliers'])}, flat lines: {len(result['flat'])}, "
                  f"crowded years: {len(result['crowding'])}")
            print(f"# report: {write_report(scenario, result, args.out or scenario.root / 'views')}")
        case "queue":
            from simulator.queue import write_queue

            print(f"# queue written to {write_queue(scenario, args.out, args.first)}")
        case "history":
            if args.action == "list":
                _print_table(history.load_metadata(scenario), args.json)
            elif args.action == "import-dyadic":
                rows = history.import_dyadic(
                    scenario, args.name, args.source_file, args.format, args.unit, args.source,
                    args.source_code, args.downloaded, args.description,
                )
                pairs = rows[["side_a", "side_b"]].drop_duplicates()
                print(f"# imported {args.name}: {len(rows)} rows, {len(pairs)} pairs, "
                      f"years {rows['date'].min()}-{rows['date'].max()}" if len(rows) else f"# {args.name}: no rows")
            elif args.action == "gaps":
                gaps = history.find_gaps(scenario, args.name)
                print(f"# {args.name}: {int(gaps['missing'].sum())} missing value(s) in {len(gaps)} tag(s)")
                if not gaps.empty:
                    _print_table(gaps.set_index("tag"), args.json)
            elif args.action == "fill":
                tags = None if args.tags is None else [t.strip().upper() for t in args.tags.split(",") if t.strip()]
                rows = history.fill_gaps(
                    scenario, args.name, args.method, args.source_file, args.source_format,
                    args.source_scale, args.source_label, args.window, args.author, tags, args.dry_run,
                )
                verb = "would fill" if args.dry_run else "filled"
                print(f"# {verb} {len(rows)} value(s) with {args.method}")
                if not rows.empty:
                    summary = rows.groupby("tag")["year"].apply(lambda y: history.compress_years(sorted(y)))
                    _print_table(summary.to_frame("years"), args.json)
            else:
                report = history.import_history(
                    scenario, args.name, args.source_file, args.format, args.unit, args.source,
                    args.source_code, args.downloaded, args.description, args.scale, args.column, args.sheet,
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

"""Week 1 readiness check for the Python for Data track (Py1).

Run from the root of your template repo:
    uv run python check_env.py
Optional: point it at your Sakila DuckDB file / CSV export folder:
    uv run python check_env.py --duckdb data/sakila.duckdb --csv-dir data/sakila_csv
Uses only the standard library (plus duckdb if installed).
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

results = []  # (status, item, detail)


def run(cmd):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        return out.returncode, (out.stdout or out.stderr).strip()
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return 1, str(e)


def check(ok, item, detail="", optional=False):
    status = "PASS" if ok else ("WARN" if optional else "FAIL")
    results.append((status, item, detail))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--duckdb", help="path to Sakila .duckdb file")
    p.add_argument("--csv-dir", help="folder with Sakila CSV exports (needed in week 2)")
    args = p.parse_args()
    root = Path.cwd()

    # --- Tooling ---
    v = sys.version_info
    check(v >= (3, 11), "Python >= 3.11", f"{v.major}.{v.minor}.{v.micro} at {sys.executable}")
    in_venv = sys.prefix != sys.base_prefix
    check(in_venv and ".venv" in sys.prefix, "Running inside the project's .venv", sys.prefix)

    rc, out = run(["uv", "--version"])
    check(rc == 0, "uv installed", out)

    rc, out = run(["git", "--version"])
    check(rc == 0, "git installed", out)
    for key in ("user.name", "user.email"):
        rc, out = run(["git", "config", "--get", key])
        check(rc == 0 and bool(out), f"git {key} set", out or "not set")

    check(shutil.which("docker") is not None, "docker on PATH (needed from week 6)",
          shutil.which("docker") or "not found", optional=True)

    # --- Template repo structure ---
    for name, optional in [
        ("pyproject.toml", False),
        ("uv.lock", False),
        (".python-version", False),
        (".venv", False),
        (".gitignore", False),
        ("README.md", False),
        ("tests", True),
        ("src", True),  # src/ layout is formally week 5-6, fine to have now
    ]:
        check((root / name).exists(), f"repo has {name}", str(root / name), optional)

    gi = root / ".gitignore"
    if gi.exists():
        text = gi.read_text()
        check(".venv" in text, ".gitignore excludes .venv")
        check(".env" in text, ".gitignore excludes .env (secrets, week 3)", optional=True)

    rc, out = run(["git", "rev-parse", "--is-inside-work-tree"])
    check(rc == 0, "repo is a git repository")
    if rc == 0:
        rc, out = run(["git", "log", "--oneline", "-1"])
        check(rc == 0 and bool(out), "at least one commit", out or "no commits")
        rc, out = run(["git", "remote", "-v"])
        check(bool(out), "remote configured (GitHub)", out.splitlines()[0] if out else "none",
              optional=True)
        rc, out = run(["git", "branch", "--format=%(refname:short)"])
        check(rc == 0, "branches", ", ".join(out.split()))

    rc, out = run(["uv", "lock", "--check"])
    check(rc == 0, "uv.lock is in sync with pyproject.toml", out.splitlines()[-1] if out else "")

    # --- Data: Sakila ---
    try:
        import duckdb  # noqa: F401
        check(True, "duckdb importable", duckdb.__version__)
    except ImportError:
        duckdb = None
        check(False, "duckdb importable", "run: uv add duckdb")

    if args.duckdb and duckdb:
        try:
            con = duckdb.connect(args.duckdb, read_only=True)
            tables = {r[0] for r in con.execute("select table_name from information_schema.tables").fetchall()}
            expected = {"actor", "film", "customer", "rental", "payment", "inventory", "store", "staff"}
            missing = expected - tables
            check(not missing, "Sakila tables in DuckDB", f"{len(tables)} tables; missing: {sorted(missing) or 'none'}")
            if "rental" in tables:
                n = con.execute("select count(*) from rental").fetchone()[0]
                check(n > 15000, "rental row count ~16,044", str(n))
        except Exception as e:
            check(False, "Sakila DuckDB readable", str(e))
    else:
        check(False, "Sakila DuckDB checked", "pass --duckdb <path>", optional=True)

    if args.csv_dir:
        csvs = sorted(Path(args.csv_dir).glob("*.csv"))
        check(len(csvs) >= 8, "Sakila CSV exports present (week 2)",
              f"{len(csvs)} files: {', '.join(c.stem for c in csvs[:10])}")
    else:
        check(False, "Sakila CSV exports checked", "pass --csv-dir <path>", optional=True)

    # --- Report ---
    width = max(len(i) for _, i, _ in results)
    for status, item, detail in results:
        print(f"[{status}] {item.ljust(width)}  {detail}")
    fails = sum(s == "FAIL" for s, _, _ in results)
    warns = sum(s == "WARN" for s, _, _ in results)
    print(f"\n{fails} fail, {warns} warn -> {'READY for week 2' if fails == 0 else 'fix FAILs first'}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()

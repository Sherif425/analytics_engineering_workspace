"""SOLO 1 - pathlib (uses: g1).

Goal: find the "big" CSV files without hard-coding any absolute path.

Tasks
  1. Build DATA_DIR from Path(__file__), exactly like g1 (no "/home/sherif/..." strings!).
  2. Implement big_csv_files(): return the NAMES (e.g. "rental.csv") of CSV files in
     data_dir larger than min_kb kilobytes, sorted alphabetically.
  3. Implement make_folder(): create PROJECT_ROOT / name if missing, return the Path.

Hints: .glob("*.csv"), .stat().st_size (bytes; 1 KB = 1024 bytes), .name,
       sorted(), .mkdir(parents=True, exist_ok=True)

Run:  uv run python lessons/week1/s1_paths.py
Also run it from inside lessons/week1/ - it must still PASS.
"""

from pathlib import Path

PROJECT_ROOT = None  # TODO
DATA_DIR = None  # TODO


def big_csv_files(data_dir: Path, min_kb: float) -> list[str]:
    # TODO
    return []


def make_folder(name: str) -> Path:
    # TODO
    return Path()


# ---------------- self-check (don't edit below) ----------------
def check(name, got, expected):
    ok = got == expected
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + ("" if ok else f"  got {got!r}, expected {expected!r}"))


check("DATA_DIR exists", bool(DATA_DIR) and Path(DATA_DIR).is_dir(), True)
if DATA_DIR:
    check(
        "big_csv_files > 100 KB",
        big_csv_files(DATA_DIR, 100),
        ["film.csv", "film_actor.csv", "inventory.csv", "payment.csv", "rental.csv"],
    )
folder = make_folder("reports")
check("make_folder('reports')", folder.is_dir() and folder.name == "reports", True)

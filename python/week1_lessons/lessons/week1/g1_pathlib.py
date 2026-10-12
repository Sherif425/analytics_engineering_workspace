"""GUIDED 1 - pathlib: finding your files reliably.

CONCEPT
-------
A path is the address of a file. There are two kinds:
  * absolute:  /home/sherif/analytics_engineering_workspace/python/data/sakila_csv/rental.csv
  * relative:  data/sakila_csv/rental.csv   <- relative to WHAT?

A relative path is relative to the *current working directory* (cwd): the folder
your terminal is in when you type the command. Change folders, and the same
relative path points somewhere else -> "FileNotFoundError". That is the #1
reason scripts "work on my machine" and break elsewhere.

THE ONE RULE WE USE
-------------------
Anchor every path to the script file itself, never to the cwd:
    SCRIPT_DIR = Path(__file__).resolve().parent
Then walk up with .parent and down with the / operator.

pathlib.Path is an object, not a string. You join with "/" and ask it questions
(.exists(), .name, .suffix ...). No string gluing, works on Linux and Windows.

Run:   uv run python lessons/week1/g1_pathlib.py
"""

from pathlib import Path

# --- 1. Two different starting points ---------------------------------------
print("1) Where am I?")
print("   current working directory:", Path.cwd())
print("   this script file:         ", Path(__file__).resolve())

# --- 2. Anchor to the script, walk up, then down ----------------------------
SCRIPT_DIR = Path(__file__).resolve().parent  # .../python/lessons/week1
PROJECT_ROOT = SCRIPT_DIR.parent.parent  # .../python   (up two folders)
DATA_DIR = PROJECT_ROOT / "data" / "sakila_csv"  # "/" joins path parts

print("\n2) Paths built from the script location")
print("   SCRIPT_DIR  :", SCRIPT_DIR)
print("   PROJECT_ROOT:", PROJECT_ROOT)
print("   DATA_DIR    :", DATA_DIR)

# --- 3. Ask a path questions -------------------------------------------------
rental_path = DATA_DIR / "rental.csv"
print("\n3) Questions you can ask a path")
print("   .name        ", rental_path.name)  # rental.csv
print("   .stem        ", rental_path.stem)  # rental
print("   .suffix      ", rental_path.suffix)  # .csv
print("   .parent.name ", rental_path.parent.name)  # sakila_csv
print("   .exists()    ", rental_path.exists())  # True
print("   .is_file()   ", rental_path.is_file())  # True
print("   .is_dir()    ", DATA_DIR.is_dir())  # True

# --- 4. Find files with a pattern: .glob() ----------------------------------
print("\n4) All CSV files in DATA_DIR, with their size")
for csv_path in sorted(DATA_DIR.glob("*.csv")):
    size_kb = csv_path.stat().st_size / 1024
    print(f"   {csv_path.name:<20} {size_kb:8.1f} KB")

# --- 5. Create an output folder safely --------------------------------------
REPORTS_DIR = PROJECT_ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)  # no error if it already exists
print("\n5) Output folder ready:", REPORTS_DIR)

# --- 6. Check before you use ------------------------------------------------
typo_path = DATA_DIR / "rentals.csv"  # note the extra "s"
print("\n6) Check a path before opening it")
if typo_path.exists():
    print("   found", typo_path.name)
else:
    print(f"   {typo_path.name} does not exist in {typo_path.parent}")

# TRY THIS
# a) cd lessons/week1 && uv run python g1_pathlib.py
#    -> section 1 cwd changes, but DATA_DIR stays the same. That's the point.
# b) Change the glob pattern to "f*.csv". Which files match?
# c) Print PROJECT_ROOT using Path(__file__).resolve().parents[2] instead.
#    parents[0] is the folder of the file, parents[1] one above, parents[2] two above.

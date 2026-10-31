#!/usr/bin/env python3
"""Add a new example: a folder with an input script, a notebook and a
placeholder image, plus its entry in examples.json.

    python3 scripts/new_example.py my-example "My example title"

Then edit <id>/<id>.in, replace <id>/<id>.png with a screenshot, and run
python3 scripts/validate.py.
"""

import json
import os
import re
import struct
import sys
import zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT = """# {title}
# Lines starting with #/ are Atomify visualizer commands, for example:
#/atom 1 1.0 #ffffff

units lj
dimension 2
atom_style atomic

lattice sq2 0.6
region box block 0 20 0 20 -0.1 0.1
create_box 1 box
create_atoms 1 box
mass * 1.0

pair_style lj/cut 2.5
pair_coeff * * 1 1
velocity all create 1.0 87287

fix nve all nve
fix enforce2d all enforce2d

thermo_style custom step temp pe ke etotal press
thermo 100
run 10000
"""

NOTEBOOK_CELLS = [
    ("markdown", "# {title}\n\nAnalysis of the latest run of this example."),
    ("code", "%pip install -q lammps-logfile pandas"),
    (
        "code",
        """import glob
import lammps_logfile
import matplotlib.pyplot as plt

# Atomify stores every run under runs/<run>/. Analyse the latest one.
logs = sorted(glob.glob("runs/*/log.lammps")) or glob.glob("log.lammps")
assert logs, "No runs yet. Press Run simulation in Atomify first."
print(f"Analysing {{logs[-1]}}")
log = lammps_logfile.File(logs[-1])
step = log.get("Step")

plt.figure()
plt.plot(step, log.get("Temp"))
plt.xlabel("Timestep")
plt.ylabel("Temperature")
plt.show()""",
    ),
]


def placeholder_png(width=320, height=200, gray=40):
    row = b"\x00" + bytes([gray, gray, gray]) * width
    raw = row * height

    def chunk(kind, data):
        body = kind + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    example_id, title = sys.argv[1], sys.argv[2]
    if not re.match(r"^[a-z0-9][a-z0-9_-]*$", example_id):
        print("error: id must be lowercase letters, digits, '-' or '_'")
        return 1

    config_path = os.path.join(ROOT, "examples.json")
    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)
    if any(e.get("id") == example_id for e in config["examples"]):
        print(f"error: an example with id '{example_id}' already exists")
        return 1
    folder = os.path.join(ROOT, example_id)
    if os.path.exists(folder):
        print(f"error: {example_id}/ already exists")
        return 1
    os.makedirs(folder)

    with open(os.path.join(folder, f"{example_id}.in"), "w") as f:
        f.write(INPUT.format(title=title))
    notebook = {
        "cells": [
            {"cell_type": kind, "metadata": {}, "source": text.format(title=title).splitlines(True)}
            | ({"outputs": [], "execution_count": None} if kind == "code" else {})
            for kind, text in NOTEBOOK_CELLS
        ],
        "metadata": {
            "kernelspec": {"name": "python", "display_name": "Python (Pyodide)", "language": "python"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 4,
    }
    with open(os.path.join(folder, f"{example_id}.ipynb"), "w") as f:
        json.dump(notebook, f, indent=1)
        f.write("\n")
    with open(os.path.join(folder, f"{example_id}.png"), "wb") as f:
        f.write(placeholder_png())

    config["examples"].append(
        {
            "id": example_id,
            "title": title,
            "description": "Describe what this example shows.",
            "imageUrl": f"{example_id}/{example_id}.png",
            "inputScript": f"{example_id}.in",
            "analysisScript": f"{example_id}.ipynb",
            "keywords": [],
            "files": [
                {"fileName": f"{example_id}.in", "url": f"{example_id}/{example_id}.in"},
                {"fileName": f"{example_id}.ipynb", "url": f"{example_id}/{example_id}.ipynb"},
            ],
        }
    )
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Created {example_id}/ and added it to examples.json.")
    print(f"Next: edit {example_id}/{example_id}.in, replace the placeholder image,")
    print("and run python3 scripts/validate.py.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

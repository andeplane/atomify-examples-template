# Agent guide

This repository is an example library for Atomify (https://andeplane.github.io/atomify), a browser app that runs LAMMPS molecular dynamics simulations and analyses them in JupyterLite notebooks. Atomify loads `examples.json` from a URL given as `?examplesUrl=`.

## Layout

- `examples.json`: the library. Format in `examples.schema.json` and `README.md`.
- `<id>/`: one folder per example, with `<id>.in` (LAMMPS input), `<id>.ipynb` (analysis notebook) and `<id>.png` (card image, about 16:9).
- `description.md`: Markdown about the whole library.
- `scripts/new_example.py <id> "<title>"`: scaffolds a new example and its entry.
- `scripts/validate.py`: checks `examples.json` and every file it references. CI runs it on every push.
- `scripts/serve.py`: local server with CORS for testing in Atomify.

## Rules

- Paths in `examples.json` are relative to `examples.json`. Do not add `baseUrl` or absolute links to this repository; they break forks.
- `inputScript` and `analysisScript` are `fileName`s that must appear in the example's `files`.
- `fileName`s are flat names with no `/`; they are where the file lands in the Atomify project.
- Notebooks run in Pyodide. Read simulation output from the latest run: `sorted(glob.glob("runs/*/log.lammps"))[-1]` (runs live in `runs/<run>/`). Install packages with `%pip install -q ...`. Commit notebooks with outputs cleared.
- LAMMPS input lines starting with `#/` are Atomify visualizer commands (`#/atom <type> <radius> <color>`, `#/camera position x y z`, `#/camera target x y z`).
- Atomify's LAMMPS is a WebAssembly build. Keep examples small enough to run in a browser (roughly up to tens of thousands of atoms) and use the packages it ships: MOLECULE, MANYBODY, KSPACE, RIGID, GRANULAR, CLASS2, MC, SHOCK, MISC, QEQ, REAXFF, EXTRA-MOLECULE, VORONOI and COLVARS.
- Only the Python standard library is used by the scripts; keep it that way.

## Checking your work

Run `python3 scripts/validate.py` after every change. To try it in Atomify, run `python3 scripts/serve.py` and open the link it prints.

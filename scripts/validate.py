#!/usr/bin/env python3
"""Check examples.json and the files it points to.

    python3 scripts/validate.py

Exits non-zero on errors, so CI can block a broken example library. Only the
Python standard library is needed.
"""

import json
import os
import re
import sys
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
EXAMPLE_KEYS = {
    "id", "title", "description", "analysisDescription", "imageUrl",
    "inputScript", "analysisScript", "author", "authorUrl", "keywords", "files",
}
REQUIRED = ["id", "title", "description", "imageUrl", "inputScript", "files"]

errors = []
warnings = []


def is_url(path):
    return bool(urlparse(path).scheme)


def check_path(where, path):
    """A relative path must exist in the repository."""
    if not isinstance(path, str) or not path:
        errors.append(f"{where}: missing path")
        return None
    if is_url(path):
        return None
    full = os.path.normpath(os.path.join(ROOT, path))
    if not full.startswith(ROOT + os.sep):
        errors.append(f"{where}: '{path}' points outside the repository")
    elif not os.path.isfile(full):
        errors.append(f"{where}: '{path}' does not exist")
    else:
        return full
    return None


def check_notebook(where, full):
    try:
        with open(full, encoding="utf-8") as f:
            nb = json.load(f)
    except ValueError as e:
        errors.append(f"{where}: not valid notebook JSON ({e})")
        return
    if "cells" not in nb:
        errors.append(f"{where}: notebook has no cells")
        return
    for cell in nb["cells"]:
        if cell.get("cell_type") == "code" and cell.get("outputs"):
            warnings.append(
                f"{where}: has saved outputs; clear them to keep the repo small"
            )
            return


def main():
    path = os.path.join(ROOT, "examples.json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as e:
        print(f"error: examples.json: {e}")
        return 1

    if "baseUrl" in data:
        warnings.append(
            "examples.json: 'baseUrl' is set. Remove it so paths resolve "
            "relative to examples.json; then forks and local servers work "
            "without edits."
        )
    if not data.get("title"):
        errors.append("examples.json: missing 'title'")
    if "descriptionFile" in data:
        check_path("descriptionFile", data["descriptionFile"])

    examples = data.get("examples")
    if not isinstance(examples, list) or not examples:
        errors.append("examples.json: 'examples' must be a non-empty list")
        examples = []

    seen = set()
    for index, example in enumerate(examples):
        name = f"examples[{index}]"
        if not isinstance(example, dict):
            errors.append(f"{name}: must be an object")
            continue
        if example.get("id"):
            name = example["id"]
        for key in REQUIRED:
            if key not in example:
                errors.append(f"{name}: missing '{key}'")
        for key in example:
            if key not in EXAMPLE_KEYS:
                errors.append(f"{name}: unknown key '{key}'")

        example_id = example.get("id", "")
        if not ID_PATTERN.match(example_id):
            errors.append(
                f"{name}: id must be lowercase letters, digits, '-' or '_'"
            )
        if example_id in seen:
            errors.append(f"{name}: duplicate id")
        seen.add(example_id)

        if "imageUrl" in example:
            check_path(f"{name}.imageUrl", example["imageUrl"])

        names = []
        for f_index, file in enumerate(example.get("files") or []):
            where = f"{name}.files[{f_index}]"
            file_name = file.get("fileName")
            if not file_name:
                errors.append(f"{where}: missing 'fileName'")
                continue
            if "/" in file_name:
                errors.append(f"{where}: fileName must not contain '/'")
            if file_name in names:
                errors.append(f"{where}: duplicate fileName '{file_name}'")
            names.append(file_name)
            if "content" in file:
                continue
            full = check_path(where, file.get("url"))
            if full and file_name.endswith(".ipynb"):
                check_notebook(where, full)

        script = example.get("inputScript")
        if script and script not in names:
            errors.append(f"{name}: inputScript '{script}' is not in files")
        notebook = example.get("analysisScript")
        if notebook and notebook not in names:
            errors.append(
                f"{name}: analysisScript '{notebook}' is not in files; "
                "add the notebook to files and use its fileName here"
            )

    for message in warnings:
        print(f"warning: {message}")
    for message in errors:
        print(f"error: {message}")
    if errors:
        print(f"\n{len(errors)} error(s).")
        return 1
    print(f"OK: {len(examples)} example(s) in examples.json.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

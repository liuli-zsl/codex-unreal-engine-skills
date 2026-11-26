"""Look up versioned desktop workflows and read definitions in a local Unreal installation."""

import argparse
import ast
import csv
import json
import re
import sys
from pathlib import Path


REFERENCES = Path(__file__).resolve().parents[1] / "references"


def series(version):
    match = re.fullmatch(r"(5\.[89])(?:\.\d+)?", version)
    if not match:
        raise ValueError(f"Unsupported Unreal version {version!r}. Supported series: 5.8 and 5.9.")
    return match.group(1)


def target(engine, version):
    requested = series(version) if version else None
    if engine is None:
        if requested is None:
            raise ValueError("Specify --engine or --version for the target project.")
        return requested, None

    root = engine.expanduser().resolve()
    if not (root / "Build" / "Build.version").is_file():
        root = root / "Engine"
    build_file = root / "Build" / "Build.version"
    with build_file.open(encoding="utf-8-sig") as stream:
        build = json.load(stream)
    if not isinstance(build, dict) or not all(type(build.get(k)) is int for k in ("MajorVersion", "MinorVersion")):
        raise ValueError(f"Missing or invalid engine version in {build_file}")
    detected = series(f"{build['MajorVersion']}.{build['MinorVersion']}")
    if requested and requested != detected:
        raise ValueError(f"Requested UE {requested}, but {build_file} identifies UE {detected}.")
    return detected, root


def catalogue(version):
    files = ["shared.csv"]
    if version == "5.9":
        files.append("ue5.9.csv")
    entries = {}
    for filename in files:
        with (REFERENCES / filename).open(encoding="utf-8", newline="") as stream:
            for row in csv.DictReader(stream):
                entries[row["id"]] = row
    return entries


def python_instructions(text, skill_id):
    # Inspect simple literal assignments without importing Unreal or executing engine code.
    module = ast.parse(text)
    constants = {}
    for node in module.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
            for name in node.targets:
                if isinstance(name, ast.Name):
                    constants[name.id] = node.value.value
        if isinstance(node, ast.ClassDef) and node.name == skill_id:
            for field in node.body:
                if isinstance(field, ast.Assign) and any(
                    isinstance(name, ast.Name) and name.id == "instructions" for name in field.targets
                ):
                    value = field.value
                    if isinstance(value, ast.Name):
                        return constants.get(value.id)
                    if isinstance(value, ast.Constant):
                        return value.value
    return None


def read_source(root, entry):
    path = root / entry["source"]
    if not path.is_file():
        raise ValueError(f"Missing from the selected installation: {path}")
    if path.suffix == ".uasset":
        raise ValueError(f"{path} is a Blueprint asset. Use the matching editor's ListSkills and GetSkills for the resolved instructions.")
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix == ".py":
        instructions = python_instructions(text, entry["id"])
        if isinstance(instructions, str) and instructions.strip():
            return f"Local Python instructions: {path}\n\n{instructions.strip()}"
    return f"Local source: {path}\n\n{text.rstrip()}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", help="Target UE series or patch version, e.g. 5.8.4")
    parser.add_argument("--engine", type=Path, help="Target installation root or Engine directory")
    parser.add_argument("--show", metavar="ID", help="Show a workflow by its exact catalog ID")
    parser.add_argument("--source", action="store_true", help="Also read its local text definition")
    args = parser.parse_args()
    if args.source and not (args.engine and args.show):
        parser.error("--source requires --engine and --show ID")
    try:
        version, root = target(args.engine, args.version)
        entries = catalogue(version)
        if args.show:
            entry = entries.get(args.show)
            if entry is None:
                raise ValueError(f"{args.show!r} is not in the UE {version} built-in catalog.")
            print(f"UE {version} | {entry['provider']} | {entry['id']}\n{entry['workflow']}\nEngine/{entry['source']}")
            if args.source:
                print(read_source(root, entry))
        else:
            print(f"UE {version} | {len(entries)} built-in workflows")
            for entry in entries.values():
                print(f"{entry['id']}\t{entry['provider']}\t{entry['workflow']}")
    except (OSError, ValueError, SyntaxError) as exc:
        parser.exit(2, f"{parser.prog}: {exc}\n")


if __name__ == "__main__":
    if not sys.stdout.isatty():
        sys.stdout.reconfigure(encoding="utf-8")
    main()

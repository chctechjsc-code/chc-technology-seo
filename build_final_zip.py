#!/usr/bin/env python3
"""Build one Claude-uploadable CHC skill ZIP without nested archives."""
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent
skill = root / "skills" / "chc-seo"
entry = skill / "SKILL.md"
if not entry.is_file():
    raise SystemExit(f"Missing CHC skill entrypoint: {entry}")

source = entry.read_text(encoding="utf-8")
frontmatter = source.split("---", 2)
if len(frontmatter) < 3:
    raise SystemExit("SKILL.md requires YAML frontmatter")
name = re.search(r"(?m)^name:\s*(.+?)\s*$", frontmatter[1])
description = re.search(r'(?m)^description:\s*"([^"]+)"\s*$', frontmatter[1])
if not name or name.group(1) != "chc-seo":
    raise SystemExit("Skill name must be chc-seo")
if not description or len(description.group(1)) > 200 or "CHC Technology" not in description.group(1):
    raise SystemExit("Description must identify CHC Technology and be at most 200 characters")

files = [p for p in sorted(skill.rglob("*")) if p.is_file()
         and "__pycache__" not in p.parts and p.suffix.lower() != ".pyc"]
bad = [p for p in files if p.suffix.lower() in {".zip", ".rar", ".7z"}]
if bad:
    raise SystemExit(f"Nested archives are not allowed: {bad}")
if [p for p in files if p.name.lower() == "skill.md"] != [entry]:
    raise SystemExit("The upload must contain exactly one SKILL.md")
if len(files) > 200:
    raise SystemExit(f"Claude Upload a skill permits at most 200 files; CHC full plugin has {len(files)}. Install as a Claude Code plugin instead (see README.md).")

output = root.parent / "claude-seo-vn-final.zip"
with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
    for path in files:
        archive.write(path, Path("chc-seo") / path.relative_to(skill))

with zipfile.ZipFile(output) as archive:
    if archive.testzip() is not None:
        raise SystemExit("ZIP integrity check failed")
    names = archive.namelist()
    if any(not name.startswith("chc-seo/") or name.lower().endswith((".zip", ".rar", ".7z")) for name in names):
        raise SystemExit("Unexpected ZIP layout or nested archive")
    if [name for name in names if name.endswith("/SKILL.md")] != ["chc-seo/SKILL.md"]:
        raise SystemExit("Unexpected skill entrypoint in ZIP")
print(f"{output} ({len(names)} files; Claude skill layout; no nested ZIP)")

#!/usr/bin/env python3
"""
Self-contained skill validator for tinted-ui-tokens.

Replicates the core frontmatter checks used by WorkBuddy's skill-creator
``quick_validate`` so that "passes CI" stays equivalent to "passes
``package_skill.py``" locally:

- SKILL.md exists
- starts with YAML frontmatter (``---``) and is well-formed
- frontmatter contains ``name`` and ``description``
- ``name`` is hyphen-case (lowercase letters, digits, hyphens; no leading /
  trailing hyphen, no consecutive hyphens)
- ``description`` contains no angle brackets (``<`` or ``>``)

This script is dependency-free (standard library only) and can be run both in
CI and locally:

    python scripts/validate_skill.py [path/to/skill-dir]   # default: current dir
"""

import re
import sys
from pathlib import Path


def validate_skill(skill_path: Path):
    """Return (ok, message) for the skill at ``skill_path``."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter = match.group(1)

    if "name:" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if "description:" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    # Extract name (anchored to line start so ``display_name`` is not matched).
    name_match = re.search(r"(?m)^name:\s*(.+)", frontmatter)
    if name_match:
        name = name_match.group(1).strip()
        if not re.match(r"^[a-z0-9-]+$", name):
            return False, (
                f"Name '{name}' should be hyphen-case "
                "(lowercase letters, digits, and hyphens only)"
            )
        if name.startswith("-") or name.endswith("-") or "--" in name:
            return False, (
                f"Name '{name}' cannot start/end with hyphen "
                "or contain consecutive hyphens"
            )

    # Extract description and reject angle brackets.
    desc_match = re.search(r"(?m)^description:\s*(.+)", frontmatter)
    if desc_match:
        description = desc_match.group(1).strip()
        if "<" in description or ">" in description:
            return False, "Description cannot contain angle brackets (< or >)"

    return True, "Skill is valid!"


def main():
    skill_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(".").resolve()
    ok, message = validate_skill(skill_path)
    print(("PASS: " if ok else "FAIL: ") + message)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

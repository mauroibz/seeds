#!/usr/bin/env python3
"""Validate the small, self-contained Seeds documentation bundle."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
SEEDS = ROOT / "seeds"
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def local_target(source: Path, raw: str) -> Path | None:
    target = raw.strip().strip("<>").split("#", 1)[0]
    if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
        return None
    target = unquote(target)
    if target.startswith("/"):
        return ROOT / target.lstrip("/")
    return (source.parent / target).resolve()


def markdown_files() -> list[Path]:
    return sorted(path for path in ROOT.rglob("*.md") if ".git" not in path.parts)


def main() -> int:
    errors: list[str] = []

    for source in markdown_files():
        text = source.read_text(encoding="utf-8")
        for match in LINK.finditer(text):
            target = local_target(source, match.group(1))
            if target is None:
                continue
            if not target.exists():
                errors.append(
                    f"broken link: {source.relative_to(ROOT)} -> {match.group(1)}"
                )
            if source.is_relative_to(SEEDS) and not target.is_relative_to(SEEDS):
                errors.append(
                    f"skill link escapes seeds/: {source.relative_to(ROOT)} -> {match.group(1)}"
                )

    skill = SEEDS / "SKILL.md"
    skill_text = skill.read_text(encoding="utf-8") if skill.exists() else ""
    if not skill_text.startswith("---\n") or "\nname: seeds\n" not in skill_text:
        errors.append("seeds/SKILL.md has invalid or missing Seeds frontmatter")

    required_templates = {
        "AGENTS.md",
        "PROJECT.md",
        "PLAN.md",
        "MILESTONE.md",
        "DECISIONS.md",
        "HANDOFF.md",
        "WORKLOG.md",
    }
    template_dir = SEEDS / "assets" / "templates"
    missing = sorted(name for name in required_templates if not (template_dir / name).is_file())
    if missing:
        errors.append(f"missing templates: {', '.join(missing)}")

    reusable_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in markdown_files()
        if path.is_relative_to(SEEDS)
    ).lower()
    for project_name in ("quepaso", "akasha"):
        if project_name in reusable_text:
            errors.append(f"project-specific name in reusable bundle: {project_name}")

    for retired in (
        "00-initial-brief",
        "01-spec-templates",
        "02-agent-manual",
        "03-case-study-quepaso",
        "04-case-study-akasha",
        "skill",
    ):
        if (ROOT / retired).exists():
            errors.append(f"retired path still exists: {retired}")

    if errors:
        print("Seeds checks failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Seeds checks passed ({len(markdown_files())} Markdown files).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

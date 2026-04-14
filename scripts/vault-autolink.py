#!/usr/bin/env python3
"""Auto-insert backlinks into a vault note.

Scans a newly-written `docs/vault/**.md` file for token candidates that map
to existing vault notes and rewrites the `<!-- linked-notes:start -->` …
`<!-- linked-notes:end -->` block. Idempotent.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VAULT = REPO_ROOT / "docs" / "vault"

START = "<!-- linked-notes:start -->"
END = "<!-- linked-notes:end -->"


def index_vault() -> dict[str, Path]:
    """Map note basename (without .md) → relative path inside vault."""
    notes: dict[str, Path] = {}
    for md in VAULT.rglob("*.md"):
        if md.name == "_index.md":
            continue
        notes[md.stem] = md.relative_to(VAULT)
    return notes


def find_candidates(text: str, notes: dict[str, Path]) -> list[str]:
    found: set[str] = set()
    for stem in notes:
        if re.search(r"\b" + re.escape(stem) + r"\b", text):
            found.add(stem)
    return sorted(found)


def rel_link(target_rel: Path, source: Path) -> str:
    rel = Path(*[".."] * (len(source.parts) - 1)) / target_rel
    return rel.as_posix().removesuffix(".md")


def update_block(text: str, links: list[str]) -> str:
    block = "\n".join(f"- [[{link}]]" for link in links) or "- _no matches_"
    new_section = f"{START}\n{block}\n{END}"
    if START in text and END in text:
        return re.sub(
            re.escape(START) + r".*?" + re.escape(END),
            new_section,
            text,
            count=1,
            flags=re.DOTALL,
        )
    # No markers — append a Linked Notes section.
    return text.rstrip() + f"\n\n## Linked Notes\n\n{new_section}\n"


def main(target: str) -> None:
    path = Path(target).resolve()
    if not path.exists() or VAULT not in path.parents:
        return
    notes = index_vault()
    text = path.read_text(encoding="utf-8")

    self_stem = path.stem
    candidates = [c for c in find_candidates(text, notes) if c != self_stem]

    rel_source = path.relative_to(VAULT)
    links = [rel_link(notes[c], rel_source) for c in candidates[:25]]

    new_text = update_block(text, links)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(0)
    main(sys.argv[1])

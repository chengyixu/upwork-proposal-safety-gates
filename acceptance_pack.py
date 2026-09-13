#!/usr/bin/env python3
"""Generate an offline acceptance checklist from explicit scope lines only."""
from __future__ import annotations
import sys
from pathlib import Path


def make_pack(items: list[str]) -> str:
    if not items:
        return "BLOCK: at least one explicit scope item is required\n"
    lines = ["# Delivery acceptance checklist", "", "Use only after the contract scope is verified.", ""]
    for item in items:
        lines.extend([f"## {item}", "- [ ] Implementation demonstrated against the agreed scope.", "- [ ] Acceptance evidence attached or linked by the authorized operator.", "- [ ] Client feedback or exception recorded before sign-off.", ""])
    lines.extend(["## Handoff record", "- [ ] Delivered items, evidence, and unresolved exceptions recorded.", "- [ ] No revenue is recognized unless a platform receipt confirms settlement.", ""])
    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: acceptance_pack.py SCOPE_FILE")
        return 2
    try:
        items = [line.strip() for line in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines() if line.strip() and not line.lstrip().startswith("#")]
    except OSError as exc:
        print(f"BLOCK: {exc}")
        return 1
    output = make_pack(items)
    print(output)
    return 0 if items else 1

if __name__ == "__main__":
    raise SystemExit(main())

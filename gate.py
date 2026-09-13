#!/usr/bin/env python3
"""Offline proposal safety gate. It makes no network or platform requests."""
from __future__ import annotations
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

PLACEHOLDER = re.compile(r"\[[^\]\n]{1,100}\]")
SECRET = ("api_key=", "token=", "password=", "secret=", "bearer ")
REQUIRED = {"job_id", "title", "posted_at", "client_verified", "scope_confirmed", "allowance_confirmed", "estimated_hours", "skills"}


def check(job: dict, draft: str, claims: list, seen: list) -> list[str]:
    issues = []
    missing = REQUIRED - job.keys()
    if missing:
        issues.append("missing job fields")
    elif job["job_id"] in seen:
        issues.append("duplicate job")
    else:
        try:
            if date.fromisoformat(job["posted_at"]) < date.today(): issues.append("stale job")
        except ValueError: issues.append("invalid posting date")
        if not all(job[x] is True for x in ("client_verified", "scope_confirmed", "allowance_confirmed")): issues.append("unverified job gate")
        if not isinstance(job["skills"], list) or not job["skills"]: issues.append("missing skills")
    if PLACEHOLDER.search(draft): issues.append("unresolved placeholder")
    if len(re.findall(r"^\s*[123][.)]\s+\S", draft, re.M)) < 3: issues.append("missing delivery steps")
    claim_names = set()
    for claim in claims:
        name, evidence = claim.get("claim", ""), claim.get("evidence", "")
        if not isinstance(name, str) or not isinstance(evidence, str) or urlparse(evidence).scheme != "https": issues.append("unsupported proof")
        if name in claim_names: issues.append("duplicate proof claim")
        claim_names.add(name)
        if any(marker in evidence.lower() for marker in SECRET): issues.append("unsafe proof")
    return list(dict.fromkeys(issues))


def main() -> int:
    if len(sys.argv) != 5:
        print("usage: gate.py JOB_JSON DRAFT_MD CLAIMS_JSON SEEN_JSON")
        return 2
    try:
        job = json.loads(Path(sys.argv[1]).read_text())
        draft = Path(sys.argv[2]).read_text()
        claims = json.loads(Path(sys.argv[3]).read_text())
        seen = json.loads(Path(sys.argv[4]).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"BLOCK: {exc}")
        return 1
    issues = check(job, draft, claims, seen)
    print("READY" if not issues else "BLOCK: " + "; ".join(issues))
    return 0 if not issues else 1

if __name__ == "__main__":
    raise SystemExit(main())

"""평가 구조 검증 채점: 회사별·심은 쪽별 검출률, 놓친 항목, 심지 않은 항목 지적(오탐 후보).

사용: uv run python -m tools.review.score <workflow 출력.json> <정답표.json> [<채점 결과.json>]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def _frac(hit: int, total: int) -> str:
    return f"{hit}/{total}"


def _summary(flagged: set[str], key: dict[str, dict[str, str]]) -> dict[str, Any]:
    seeds = list(key)
    origins = sorted({v.get("origin", "?") for v in key.values()})
    return {
        "recall": _frac(sum(s in flagged for s in seeds), len(seeds)),
        "by_origin": {
            o: _frac(
                sum(s in flagged for s in seeds if key[s].get("origin", "?") == o),
                sum(1 for s in seeds if key[s].get("origin", "?") == o),
            )
            for o in origins
        },
        "missed": [s for s in seeds if s not in flagged],
        "non_seed_flagged": sorted(flagged - set(seeds)),
    }


def score(runs: list[dict[str, Any]], key: dict[str, dict[str, str]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    every: set[str] = set()
    for prov in sorted({r["provider"] for r in runs}):
        flagged = {f["id"] for r in runs if r["provider"] == prov for f in r["findings"]}
        every |= flagged
        out[prov] = _summary(flagged, key)
        out[prov]["by_lens"] = {
            r["lens"]: sorted(f["id"] for f in r["findings"] if f["id"] in key)
            for r in runs
            if r["provider"] == prov
        }
    out["combined"] = _summary(every, key)
    return out


def main() -> None:
    runs = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))["result"]
    if isinstance(runs, dict):  # calibrate.js: {"failedReviewers": n, "result": [...]}
        if runs.get("failedReviewers", 1) != 0:
            raise SystemExit(f"평가자 실패 {runs.get('failedReviewers')}명: 이 검증은 무효라 채점하지 않는다")
        runs = runs["result"]
    key = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    result = score(runs, key)
    text = json.dumps(result, ensure_ascii=False, indent=1)
    if len(sys.argv) > 3:
        Path(sys.argv[3]).write_text(text, encoding="utf-8")
    for prov, s in result.items():
        print(
            f"{prov}: {s['recall']} {s['by_origin']} 놓침 {len(s['missed'])} 심지 않은 항목 지적 {len(s['non_seed_flagged'])}"
        )


if __name__ == "__main__":
    main()

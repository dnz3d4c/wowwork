"""다듬기 뒤에 남은 지적을 파일별로 모은다: 회귀 확인의 중대 이상 지적과 본 평가의 사용자 판단 건.

사용: uv run python -m tools.review.polish_leftover <본평가 main-result.json> <회귀 result.json> <출력.json>
인용(quote)이 지금 설명서에 글자 그대로 없는 지적은 이미 바뀐 곳이라 빼고 수를 보고한다.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from tools.manual import KO_ROOT


def collect(
    main: dict[str, Any], regression: dict[str, Any], texts: dict[str, str]
) -> tuple[dict[str, list[dict[str, Any]]], int]:
    by_file: dict[str, list[dict[str, Any]]] = {}
    gone = 0

    def add(file: str, item: dict[str, Any]) -> None:
        nonlocal gone
        if item["quote"] and item["quote"] in texts.get(file, ""):
            by_file.setdefault(file, []).append(item)
        else:
            gone += 1

    for f in regression["failed"]:
        for i, b in enumerate(f["blocking"]):
            add(
                f["file"],
                {
                    "ref": f"{f['file']}#reg-{b['by']}-{i}",
                    "kind": "regression",
                    **{
                        k: b[k]
                        for k in ("by", "category", "severity", "quote", "suggestion", "problem", "evidence")
                    },
                },
            )
    for x in main["reviewed"]:
        for e in x["escalations"]:
            if "quote" not in e:
                continue
            add(
                x["file"],
                {
                    "ref": e["ref"],
                    "kind": "split" if "gpt" in e else "unanswered",
                    "quote": e["quote"],
                    "suggestion": e.get("suggestion", ""),
                    "why": e["why"],
                    "gpt_reason": e.get("gpt", ""),
                    "claude_reason": e.get("claude", ""),
                },
            )
    return by_file, gone


def main() -> int:
    main_r = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    reg = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    texts = {p.relative_to(KO_ROOT).as_posix(): p.read_text(encoding="utf-8") for p in KO_ROOT.rglob("*.md")}
    by_file, gone = collect(main_r, reg, texts)
    Path(sys.argv[3]).write_text(json.dumps(by_file, ensure_ascii=False, indent=1), encoding="utf-8")
    n = sum(len(v) for v in by_file.values())
    print(f"남은 지적 {n}건, 파일 {len(by_file)}개, 이미 바뀌어 뺀 것 {gone}건")
    return 0


if __name__ == "__main__":
    sys.exit(main())

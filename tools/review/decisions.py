"""Workflow 결과(확정 번역)를 기록 파일과 동기화 도구용 TSV 로 바꾼다.

사용: uv run python -m tools.review.decisions <workflow 출력.json> <평가 폴더>
<평가 폴더>/decisions.json 에 판정 전체를, <평가 폴더>/apply.tsv 에 번역이 바뀌는 항목만 쓴다.
apply.tsv 는 `uv run python -m tools.sync_locale <apply.tsv>` 로 반영한다.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

from tools.locale_lib import KOKR_DIR, parse_locale_file


def changes(decisions: list[dict[str, str]], current: dict[tuple[str, str], str]) -> list[list[str]]:
    rows = []
    for d in decisions:
        file, key = d["id"].split("::", 1)
        before = current.get((file, key), "")
        if d["final_ko"] != before:
            rows.append([file, key, before, d["final_ko"]])
    return rows


def main() -> None:
    out_json, review_dir = Path(sys.argv[1]), Path(sys.argv[2])
    result = json.loads(out_json.read_text(encoding="utf-8"))["result"]
    decisions = [d for b in result for d in b["decisions"]]
    current = {(p.name, k): v for p in KOKR_DIR.glob("*.lua") for k, v in parse_locale_file(p).items()}
    rows = changes(decisions, current)
    (review_dir / "decisions.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    with (review_dir / "apply.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["file", "key", "en", "ko"])  # en 열에는 바뀌기 전 번역을 기록한다
        w.writerows(rows)
    print(f"판정 {len(decisions)}건, 번역 변경 {len(rows)}건 -> {review_dir / 'apply.tsv'}")


if __name__ == "__main__":
    main()

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
from typing import Any

from tools.locale_lib import KOKR_DIR, parse_locale_file
from tools.review.guard import valid_evidence


def changes(decisions: list[dict[str, str]], current: dict[tuple[str, str], str]) -> list[list[str]]:
    rows = []
    for d in decisions:
        file, key = d["id"].split("::", 1)
        before = current.get((file, key), "")
        if d["final_ko"] != before:
            rows.append([file, key, before, d["final_ko"]])
    return rows


JUDGED = ("upheld", "dispute-won")


def incomplete_batches(result: list[dict[str, Any]]) -> list[str]:
    """평가자가 하나라도 실패했거나 실패 수 기록이 없는 묶음. 이런 묶음의 판정은 반영하지 않는다."""
    return [b["batch"] for b in result if b.get("failedReviewers", 1) != 0]


def split_invalid(decisions: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """판정자가 결정한 항목은 허용된 1차 자료를 근거로 댔을 때만 유효하다(guard.valid_evidence)."""
    valid: list[dict[str, Any]] = []
    invalid: list[dict[str, Any]] = []
    for d in decisions:
        judged = str(d.get("how", "")).startswith(JUDGED)
        (invalid if judged and not valid_evidence(d.get("evidence") or []) else valid).append(d)
    return valid, invalid


RETRY = ("번역자 응답 없음", "판정 누락")


def collect_escalations(result: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """확정하지 못한 항목 전체와, 그중 실패라서 다시 돌려야 하는 것(응답 없음·판정 누락)."""
    esc = [{"batch": b["batch"], **e} for b in result for e in b.get("escalations", [])]
    return esc, [e for e in esc if str(e.get("why", "")).startswith(RETRY)]


def main() -> int:
    out_json, review_dir = Path(sys.argv[1]), Path(sys.argv[2])
    result = json.loads(out_json.read_text(encoding="utf-8"))["result"]
    broken = incomplete_batches(result)
    if broken:
        raise SystemExit(f"평가자가 실패한 묶음이 있어 반영하지 않는다(다시 돌릴 것): {broken}")
    decisions, invalid = split_invalid([d for b in result for d in b["decisions"]])
    current = {(p.name, k): v for p in KOKR_DIR.glob("*.lua") for k, v in parse_locale_file(p).items()}
    rows = changes(decisions, current)
    if invalid:
        (review_dir / "invalid-judgments.json").write_text(
            json.dumps(invalid, ensure_ascii=False, indent=1), encoding="utf-8"
        )
        print(
            f"근거가 무효인 판정 {len(invalid)}건은 반영하지 않음 -> 사용자 판단 목록 (invalid-judgments.json)"
        )
    (review_dir / "decisions.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    with (review_dir / "apply.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["file", "key", "en", "ko"])  # en 열에는 바뀌기 전 번역을 기록한다
        w.writerows(rows)
    print(f"판정 {len(decisions)}건, 번역 변경 {len(rows)}건 -> {review_dir / 'apply.tsv'}")
    esc, failed = collect_escalations(result)
    if esc:
        (review_dir / "escalations.json").write_text(
            json.dumps(esc, ensure_ascii=False, indent=1), encoding="utf-8"
        )
        print(f"확정하지 못한 항목 {len(esc)}건 -> 사용자 판단 목록 (escalations.json)")
    if failed:
        print(f"그중 {len(failed)}건은 에이전트 실패(응답 없음·판정 누락)라 다시 돌려야 함")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

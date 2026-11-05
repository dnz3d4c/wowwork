"""평가 구조 검증용: 묶음 사본에 알려진 오류를 심는다. 정답표는 평가자에게 주지 않는다.

사용: uv run python -m tools.review.seed <원본 묶음.json> <출력 묶음.json> <정답표.json> <심을목록.json>

심을 목록과 정답표는 평가자가 읽을 수 없는 곳(저장소 밖)에 둔다. 평가가 끝난 뒤에 기록으로 옮긴다.
심을 목록 형식: {"<id>": ["심은 번역", "오류 종류", "잡아야 할 관점"], ...}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> None:
    src, out, key, seeds_path = map(Path, sys.argv[1:5])
    seeds = json.loads(seeds_path.read_text(encoding="utf-8"))
    data = json.loads(src.read_text(encoding="utf-8"))
    answers = {}
    for item in data["items"]:
        if item["id"] in seeds:
            seeded, kind, lens = seeds[item["id"]]
            answers[item["id"]] = {"original": item["ko"], "seeded": seeded, "kind": kind, "lens": lens}
            item["ko"] = seeded
    missing = set(seeds) - set(answers)
    if missing:
        raise SystemExit(f"묶음에 없는 id: {missing}")
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    key.write_text(json.dumps(answers, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(answers)}개 심음 -> {out}")


if __name__ == "__main__":
    main()

"""평가 구조 검증용: 묶음 사본에 알려진 오류를 심는다. 정답표는 평가자에게 주지 않는다.

심을 목록 형식: {"<id>": ["심은 번역", "오류 종류", "잡아야 할 관점"], ...}
심을 목록과 정답표는 평가자가 읽을 수 없는 곳(저장소 밖)에 둔다. 평가가 끝난 뒤에 기록으로 옮긴다.
격리 폴더와 함께 만들 때는 tools.review.sandbox 를 쓴다.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

Seeds = dict[str, list[str]]


def merge_seeds(sources: dict[str, Path]) -> Seeds:
    """출처 이름 → 심을 목록 파일. 같은 id 는 먼저 온 출처가 이긴다. 값 끝에 출처를 붙인다."""
    merged: Seeds = {}
    for origin, path in sources.items():
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data.get("seeds"), list):  # 오류 제작자(seeds.schema.json) 출력 형식
            data = {s["id"]: [s["seeded"], s["kind"], s["lens"]] for s in data["seeds"]}
        for item_id, (seeded, kind, lens, *_) in data.items():
            merged.setdefault(item_id, [seeded, kind, lens, origin])
    return merged


def apply_seeds(data: dict[str, Any], seeds: Seeds) -> dict[str, dict[str, str]]:
    """묶음의 번역과 related 목록에 심는다. 정답표를 돌려준다."""
    answers = {}
    for item in data["items"]:
        if item["id"] in seeds:
            seeded, kind, lens, *rest = seeds[item["id"]]
            answers[item["id"]] = {"original": item["ko"], "seeded": seeded, "kind": kind, "lens": lens}
            if rest:
                answers[item["id"]]["origin"] = rest[0]
            item["ko"] = seeded
        for rel in item.get("related", []):
            if rel["id"] in seeds:
                rel["ko"] = seeds[rel["id"]][0]
    missing = set(seeds) - set(answers)
    if missing:
        raise ValueError(f"묶음에 없는 id: {sorted(missing)}")
    return answers

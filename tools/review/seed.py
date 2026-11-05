"""평가 구조 검증용: 묶음 사본에 알려진 오류를 심는다. 정답표는 평가자에게 주지 않는다.

사용: uv run python -m tools.review.seed <원본 묶음.json> <출력 묶음.json> <정답표.json>
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# id → (심은 번역, 오류 종류, 이 오류를 잡아야 할 관점)
SEEDS: dict[str, tuple[str, str, str]] = {
    "navigation.lua::You are targeting yourself": ("대상이 당신을 지정함", "뜻 반전", "accuracy"),
    "targeting.lua::Cannot set virtual focus while in combat.": (
        "가상 주시 대상을 설정할 수 없습니다.", "조건 누락", "accuracy"),
    "targeting.lua::Focus %d set to %s.": ("주시 대상 %s 설정: %d.", "서식 지정자 순서", "context"),
    "windows.lua::Guild Control": ("길드 관리", "공식 용어", "terminology"),
    "navigation.lua::Visited waypoints forgotten": ("방문한 경유지 기록 지움!", "원문에 없는 기호", "listening"),
    "windows.lua::Stable": ("우리", "동음이의어", "listening"),
    "navigation.lua::Your floor is not clear here. Choose your start.": (
        "여기서는 현재 층이 불분명합니다.", "문장 누락", "accuracy"),
    "targeting.lua::Open Target Menu": ("대상 메뉴를 엽니다", "문체(메뉴 항목은 명사형)", "style"),
    "targeting.lua::Free": ("자유", "파일 간 불일치(Free Sound=해제됨 소리)", "terminology"),
    "windows.lua::Leader": ("지도자", "코드 맥락(파티 찾기 역할 버튼)", "context"),
}  # fmt: skip


def main() -> None:
    src, out, key = map(Path, sys.argv[1:4])
    data = json.loads(src.read_text(encoding="utf-8"))
    answers = {}
    for item in data["items"]:
        if item["id"] in SEEDS:
            seeded, kind, lens = SEEDS[item["id"]]
            answers[item["id"]] = {"original": item["ko"], "seeded": seeded, "kind": kind, "lens": lens}
            item["ko"] = seeded
    missing = set(SEEDS) - set(answers)
    if missing:
        raise SystemExit(f"묶음에 없는 id: {missing}")
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    key.write_text(json.dumps(answers, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(answers)}개 심음 -> {out}")


if __name__ == "__main__":
    main()

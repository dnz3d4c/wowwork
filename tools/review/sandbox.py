"""평가 구조 검증용 격리 폴더를 만든다. 평가자는 이 폴더만 본다.

들어가는 것: 오류를 심은 묶음(batch.json), 평가 프롬프트·스키마, 번역 지침·결정 목록·용어집,
게임 공식 문자열, 앱 코드 사본(.git·문서 제외), 오류를 심은 koKR 사본과 enUS.
들어가지 않는 것: 원래 번역, 정답표, 평가 기록(reviews), 계획 문서.

사용: uv run python -m tools.review.sandbox <격리폴더> <원본 묶음.json> <정답표 출력.json> <출처=심을목록.json>...
예: ... claude=C:/tmp/seeds-claude.json gpt=C:/tmp/seeds-gpt.json
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from typing import Any

from tools.locale_lib import REPO_ROOT, WOWVISION_DIR, parse_locale_file, upstream_locale_dir
from tools.review.guard import ALLOWED_EVIDENCE
from tools.review.seed import apply_seeds, merge_seeds
from tools.sync_locale import rebuild

# 평가자에게 주는 wowwork 자료는 판정 근거로 인정하는 자료와 같다(guard.ALLOWED_EVIDENCE 가 원천).
WORK_FILES = tuple(a.removeprefix("wowwork/") for a in ALLOWED_EVIDENCE if a.startswith("wowwork/"))
APP_IGNORE = shutil.ignore_patterns(".git", "docs", "audio", "mapdata", "*.ogg", "*.mp3", "*.blp", "*.tga")


def build_sandbox(
    root: Path,
    batch: dict[str, Any],
    seeded: dict[str, str],
    *,
    locale_dir: Path,
    app_dir: Path,
    work_dir: Path,
) -> None:
    """seeded: 항목 id → 심은 번역. batch 는 이미 심어진 상태여야 한다."""
    if root.exists():
        shutil.rmtree(root)
    work = root / "wowwork"
    for rel in WORK_FILES:
        src = work_dir / rel
        if src.exists():
            (work / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, work / rel)
    shutil.copytree(work_dir / "tools" / "review" / "prompts", work / "tools" / "review" / "prompts")
    for schema in (work_dir / "tools" / "review").glob("*.schema.json"):
        shutil.copy2(schema, work / "tools" / "review" / schema.name)
    shutil.copytree(app_dir, root / "wowvision-ko" / "WowVision", ignore=APP_IGNORE)
    loc = root / "wowvision-ko" / "vision-locale"
    shutil.copytree(locale_dir / "enUS", loc / "enUS")
    (loc / "koKR").mkdir(parents=True)
    by_file: dict[str, dict[str, str]] = {}
    for item_id, value in seeded.items():
        file, key = item_id.split("::", 1)
        by_file.setdefault(file, {})[key] = value
    for en_path in sorted((locale_dir / "enUS").glob("*.lua")):
        ko_path = locale_dir / "koKR" / en_path.name
        ko_text = ko_path.read_text(encoding="utf-8") if ko_path.exists() else None
        changed = set(by_file.get(en_path.name, {}))
        text, _ = rebuild(
            en_path.read_text(encoding="utf-8"), ko_text, by_file.get(en_path.name, {}), changed
        )
        (loc / "koKR" / en_path.name).write_text(text, encoding="utf-8", newline="\n")
    (root / "batch.json").write_text(json.dumps(batch, ensure_ascii=False, indent=1), encoding="utf-8")


def main() -> None:
    root, src, key_out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    sources = dict(arg.split("=", 1) for arg in sys.argv[4:])
    seeds = merge_seeds({name: Path(p) for name, p in sources.items()})
    batch = json.loads(src.read_text(encoding="utf-8"))
    answers = apply_seeds(batch, seeds)
    build_sandbox(
        root, batch, {i: s[0] for i, s in seeds.items()},
        locale_dir=upstream_locale_dir(), app_dir=WOWVISION_DIR, work_dir=REPO_ROOT,
    )  # fmt: skip
    key_out.write_text(json.dumps(answers, ensure_ascii=False, indent=1), encoding="utf-8")
    ko_check = {
        (p.name, k): v for p in (root / "wowvision-ko/vision-locale/koKR").glob("*.lua")
        for k, v in parse_locale_file(p).items()
    }  # fmt: skip
    leaked = [i for i, a in answers.items() if ko_check.get(tuple(i.split("::", 1))) == a["original"]]  # type: ignore[arg-type]
    print(f"{len(answers)}개 심음 -> {root} (원래 번역이 남은 항목: {leaked or '없음'})")


if __name__ == "__main__":
    main()

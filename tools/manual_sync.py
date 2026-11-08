"""koKR 값이 바뀌었을 때 한국어 설명서의 화면 문구 인용을 새 값에 맞춘다.

사용: uv run python -m tools.manual_sync <apply.tsv> [--dry-run]
apply.tsv 는 tools.review.decisions 가 만든 것(file, key, 바뀌기 전 값, 바뀐 값). 세 번째 열의
이름은 en 이지만 내용은 바뀌기 전 한국어 값이다.

설명서는 koKR 값을 화면 문구로 인용하므로(docs/translation-guide.md `## 설명서` `### 용어` 1번) 값이 바뀌면 따라야 한다.
판단 기준:
- 바꾸는 곳: 같은 경로의 영어 설명서가 그 키의 영어를 인용할 때만. 짧은 값(8자 미만)은 따옴표로
  감싼 인용 전체가 옛 값과 같을 때만, 긴 값은 어디에 나오든.
- 같은 옛 값을 쓰는 다른 키가 있으면 영어 설명서가 어느 키를 인용하는지 본다. 둘 다 인용하면
  바꾸지 않고 "판단 필요"로 보고한다.
2026-11-06 사례: targeting.lua "Controlled"를 바꾸면서 ui.lua "controlled"(같은 값 "제어됨")를
인용한 world/combat.md 3곳까지 바꿨다가 되돌렸다.
"""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from pathlib import Path

LONG = 8


@dataclass(frozen=True)
class Change:
    en: str
    old: str
    new: str


def _mentions(en_text: str, en: str, short: bool) -> bool:
    # 짧은 값은 대소문자를 가린다("Controlled"와 "controlled"가 다른 키). 긴 값은 원문이 문장 속에서
    # 소문자로 쓰기도 해서("free bag slots") 가리지 않는다.
    return f'"{en}"' in en_text if short else en.lower() in en_text.lower()


def _unmask(text: str, masks: list[str]) -> str:
    for i, v in enumerate(masks):
        text = text.replace(f"\x00{i}\x00", v)
    return text


def sync_text(
    changes: list[Change],
    en_text: str,
    ko_text: str,
    others: dict[str, list[str]],
    values: set[str] | frozenset[str] = frozenset(),
) -> tuple[str, list[str]]:
    """others: 옛 값 → 그 값을 지금도 쓰는 **다른** 키들의 영어. values: 지금 koKR 값 전체."""
    log: list[str] = []
    for ch in sorted(changes, key=lambda c: -len(c.old)):
        if ch.old == ch.new:
            continue
        short = len(ch.old) < LONG
        needle = f'"{ch.old}"' if short else ch.old
        target = f'"{ch.new}"' if short else ch.new
        # 긴 값은 따옴표 없이 찾으므로 더 긴 다른 값 안쪽("주시 대상 강화 효과" 속 "대상 강화 효과")도
        # 걸린다. 그런 값은 자리표시자로 가려 두고 바꾼 뒤 되돌린다(2026-11-08).
        masks = [] if short else sorted(
            {v for v in values if ch.old in v and v not in (ch.old, ch.new)}, key=len, reverse=True
        )
        for i, v in enumerate(masks):
            ko_text = ko_text.replace(v, f"\x00{i}\x00")
        # 새 값 안에 옛 값이 들어 있으면("…경로" → "…경로 안내") 이미 바뀐 곳을 다시 바꾸지 않도록
        # 새 값으로 쪼갠 조각에서만 찾는다. 그래야 여러 번 돌려도 결과가 같다.
        parts = ko_text.split(target) if needle in target else [ko_text]
        count = sum(p.count(needle) for p in parts)
        if not count or not _mentions(en_text, ch.en, short):
            ko_text = _unmask(ko_text, masks)
            continue
        # 이번에 함께 바뀐 키 가운데 옛 값은 같고 새 값이 다른 키도 경쟁자다. 이 검사가 없으면
        # 먼저 처리한 키가 다른 키의 인용까지 바꾸고, 뒤의 키는 옛 값이 사라져 아무 일도 안 한다
        # (codex 2026-11-06). 새 값까지 같으면 어느 키로 바꿔도 결과가 같으므로 경쟁자가 아니다.
        peers = [c.en for c in changes if c is not ch and c.old == ch.old and c.new != ch.new]
        rivals = [e for e in [*others.get(ch.old, []), *peers] if _mentions(en_text, e, short)]
        if rivals:
            log.append(f"판단 필요: {ch.old!r} {count}곳, 원문이 {ch.en!r}와 {rivals}를 모두 인용")
            ko_text = _unmask(ko_text, masks)
            continue
        joiner = target if needle in target else ""
        ko_text = _unmask(joiner.join(p.replace(needle, target) for p in parts), masks)
        log.append(f"{count}x {ch.old} -> {ch.new}")
    return ko_text, log


def load(apply_tsv: Path) -> tuple[list[Change], dict[str, list[str]], set[str]]:
    from tools.locale_lib import KOKR_DIR, parse_locale_file, upstream_locale_dir

    en_dir = upstream_locale_dir() / "enUS"
    rows = list(csv.DictReader(apply_tsv.open(encoding="utf-8"), delimiter="\t"))
    changed = {(r["file"], r["key"]) for r in rows}
    changes = []
    for r in rows:
        en = parse_locale_file(en_dir / r["file"]).get(r["key"]) or r["key"]
        changes.append(Change(en=en, old=r["en"], new=r["ko"]))
    olds = {c.old for c in changes}
    others: dict[str, list[str]] = {}
    values: set[str] = olds.copy()
    for ko_path in KOKR_DIR.glob("*.lua"):
        en_map = parse_locale_file(en_dir / ko_path.name) if (en_dir / ko_path.name).exists() else {}
        for key, value in parse_locale_file(ko_path).items():
            values.add(value)
            if value in olds and (ko_path.name, key) not in changed:
                others.setdefault(value, []).append(en_map.get(key) or key)
    return changes, others, values


def main() -> int:
    from tools.manual import EN_ROOT, KO_ROOT

    changes, others, values = load(Path(sys.argv[1]))
    dry = "--dry-run" in sys.argv
    for ko_path in sorted(KO_ROOT.rglob("*.md")):
        rel = ko_path.relative_to(KO_ROOT)
        en_path = EN_ROOT / rel
        if not en_path.exists():
            continue
        text = ko_path.read_text(encoding="utf-8")
        out, log = sync_text(changes, en_path.read_text(encoding="utf-8"), text, others, values)
        for line in log:
            print(f"{rel.as_posix()}: {line}")
        if out != text and not dry:
            ko_path.write_text(out, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())

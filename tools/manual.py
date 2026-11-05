"""설명서 번역 도구: 원문과 번역문의 구조 대조, 앵커 검사, 파일별 용어표.

사용:
  uv run python -m tools.manual list                 # 원문 파일 목록과 단어 수
  uv run python -m tools.manual terms <상대경로>       # 그 파일의 UI 문자열 용어표(JSON)
  uv run python -m tools.manual check [<상대경로>...]  # 번역문 기계 검사(없으면 번역된 전체)
  uv run python -m tools.manual batch <상대경로> <출력.json>  # 평가 입력(원문, 번역문, 용어표)
상대경로는 docs/src/user/en 기준(예: basics/interface.md). 번역문은 같은 상대경로의 ko 폴더.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from tools.locale_lib import KOKR_DIR, WOWVISION_DIR, parse_locale_file, upstream_locale_dir

EN_ROOT = WOWVISION_DIR / "docs" / "src" / "user" / "en"
KO_ROOT = WOWVISION_DIR / "docs" / "src" / "user" / "ko"
SOURCE_LINE = re.compile(r"^<!-- source: docs/src/user/en/(\S+) @ ([0-9a-f]{7,40}) -->\n")
_HEADING = re.compile(r"^(#{1,6}) +(.*?)\s*$", re.MULTILINE)
_FENCE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]*)\)")
_CODE = re.compile(r"`[^`\n]+`")
# 설명서는 합니다체. 문장 끝의 해요체 어미는 기계 검사로 잡는다.
_HAEYO = re.compile(r"[가-힣]*(?:세요|해요|에요|예요|어요|아요|지요|죠)(?=[.!?)\s]|$)", re.MULTILINE)


def slug(heading: str) -> str:
    """mdBook normalize_id: 문자·숫자·_·- 만 남기고(영문은 소문자), 공백은 -."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", heading)
    out = []
    for ch in text:
        if ch.isalnum() or ch in "_-":
            out.append(ch.lower() if ch.isascii() else ch)
        elif ch.isspace():
            out.append("-")
    return "".join(out)


def _strip_fences(md: str) -> str:
    return _FENCE.sub("", md)


def structure(md: str) -> dict[str, list]:  # type: ignore[type-arg]
    body = _strip_fences(SOURCE_LINE.sub("", md))
    tables, rows = [], 0
    for line in body.splitlines() + [""]:
        if line.lstrip().startswith("|"):
            rows += 1
        elif rows:
            tables.append(rows)
            rows = 0
    return {
        "headings": [len(m.group(1)) for m in _HEADING.finditer(body)],
        "tables": tables,
        "links": [t.split("#", 1)[0] for t in _LINK.findall(body)],
        "code": _CODE.findall(body),
        "blocks": _FENCE.findall(md),
    }


def _anchors(path: Path) -> set[str]:
    if not path.exists():
        return set()
    seen: dict[str, int] = {}
    out = set()
    for m in _HEADING.finditer(_strip_fences(path.read_text(encoding="utf-8"))):
        s = slug(m.group(2))
        n = seen.get(s, 0)
        out.add(s if n == 0 else f"{s}-{n}")
        seen[s] = n + 1
    return out


def check(en: str, ko: str, ko_path: Path) -> list[str]:
    problems = []
    if not SOURCE_LINE.match(ko):
        problems.append("첫 줄에 원문 기록(<!-- source: docs/src/user/en/... @ 커밋 -->)이 없다")
    a, b = structure(en), structure(ko)
    labels = {
        "headings": "제목 수준",
        "tables": "표 행 수",
        "links": "링크 대상",
        "code": "인라인 코드",
        "blocks": "코드 블록",
    }
    for key, label in labels.items():
        if key == "code":
            if sorted(a[key]) != sorted(b[key]):
                problems.append(
                    f"{label} 다름: 원문만 {sorted(set(a[key]) - set(b[key]))}, 번역만 {sorted(set(b[key]) - set(a[key]))}"
                )
        elif a[key] != b[key]:
            problems.append(f"{label} 다름: 원문 {a[key]} / 번역 {b[key]}")
    haeyo = [
        m.group(0) + "." for m in _HAEYO.finditer(_CODE.sub("", _strip_fences(ko))) if len(m.group(0)) > 1
    ]
    if haeyo:
        problems.append(f"해요체 어미 {len(haeyo)}곳(설명서는 합니다체): {', '.join(sorted(set(haeyo))[:8])}")
    for target in _LINK.findall(_strip_fences(ko)):
        if "#" not in target or target.startswith(("http://", "https://")):
            continue
        file_part, frag = target.split("#", 1)
        dest = ko_path if not file_part else (ko_path.parent / file_part).resolve()
        if frag not in _anchors(dest):
            problems.append(f"앵커 없음: {target} (대상 {dest.name}의 제목에서 만든 앵커와 맞지 않는다)")
    return problems


def term_sheet(en: str, en_to_ko: dict[str, str]) -> list[dict[str, str]]:
    """원문에 나오는 UI 문자열(두 단어 이상, 또는 한 단어라도 대문자로 시작하는 6자 이상)과 koKR 값."""
    text = _strip_fences(en)
    sheet = []
    for value, ko in sorted(en_to_ko.items(), key=lambda kv: -len(kv[0])):
        words = value.split()
        if "%" in value or not ko or (len(words) < 2 and not (value[:1].isupper() and len(value) >= 6)):
            continue
        if re.search(r"(?<![\w])" + re.escape(value) + r"(?![\w])", text):
            sheet.append({"en": value, "ko": ko})
    return sheet


def locale_pairs() -> dict[str, str]:
    pairs: dict[str, str] = {}
    for p in (upstream_locale_dir() / "enUS").glob("*.lua"):
        ko = parse_locale_file(KOKR_DIR / p.name)
        for key, value in parse_locale_file(p).items():
            if key in ko:
                pairs.setdefault(value, ko[key])
    return pairs


def main() -> int:
    cmd, rest = sys.argv[1], sys.argv[2:]
    if cmd == "list":
        for p in sorted(EN_ROOT.rglob("*.md")):
            print(f"{len(p.read_text(encoding='utf-8').split()):6d}  {p.relative_to(EN_ROOT).as_posix()}")
        return 0
    if cmd == "terms":
        en = (EN_ROOT / rest[0]).read_text(encoding="utf-8")
        print(json.dumps(term_sheet(en, locale_pairs()), ensure_ascii=False, indent=1))
        return 0
    if cmd == "batch":
        rel, out = rest[0], Path(rest[1])
        en = (EN_ROOT / rel).read_text(encoding="utf-8")
        data = {"file": rel, "en_path": f"wowvision-ko/WowVision/docs/src/user/en/{rel}",
                "ko_path": f"wowvision-ko/WowVision/docs/src/user/ko/{rel}", "en": en,
                "ko": (KO_ROOT / rel).read_text(encoding="utf-8"), "terms": term_sheet(en, locale_pairs())}  # fmt: skip
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        print(out)
        return 0
    rels = rest or sorted(p.relative_to(KO_ROOT).as_posix() for p in KO_ROOT.rglob("*.md"))
    bad = 0
    for rel in rels:
        ko_path = KO_ROOT / rel
        problems = (
            ["번역 파일 없음"] if not ko_path.exists()
            else check((EN_ROOT / rel).read_text(encoding="utf-8"), ko_path.read_text(encoding="utf-8"), ko_path)
        )  # fmt: skip
        if problems:
            bad += 1
            print(f"{rel}:")
            for pr in problems:
                print(f"  - {pr}")
    print(f"검사 {len(rels)}개, 문제 있는 파일 {bad}개")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

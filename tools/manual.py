"""설명서 번역 도구: 원문과 번역문의 구조 대조, 앵커 검사, 파일별 용어표, koKR 값 변경 따라가기.

koKR 값이 바뀌면 설명서의 화면 문구 인용도 따라 바뀌어야 한다(`follow_all`). tools.sync_locale 이
koKR 을 쓸 때 부르므로 따로 실행하지 않는다.

사용:
  uv run python -m tools.manual list                 # 원문 파일 목록과 단어 수
  uv run python -m tools.manual terms <상대경로>       # 그 파일의 UI 문자열 용어표(JSON)
  uv run python -m tools.manual check [<상대경로>...]  # 번역문 기계 검사(없으면 번역된 전체)
  uv run python -m tools.manual batch <상대경로> <출력.json>  # 평가 입력(원문, 번역문, 용어표, 원문이 바뀌었으면 en_diff)
  uv run python -m tools.manual diff <상대경로>          # 커밋된 번역의 원문 커밋 이후 영어 원문의 변경
상대경로는 docs/src/user/en 기준(예: basics/interface.md). 번역문은 같은 상대경로의 ko 폴더.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
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

# ── koKR 값 변경 따라가기 ──────────────────────────────────────────────
# 바꾸는 곳: 같은 경로의 영어 설명서가 그 키의 영어를 인용할 때만. 짧은 값(LONG 미만)은 따옴표로 감싼
# 인용 전체가 옛 값과 같을 때만, 긴 값은 어디에 나오든.
# 같은 옛 값을 쓰는 다른 키가 있으면 영어 설명서가 어느 키를 인용하는지 본다. 둘 다 인용하면 바꾸지 않고
# "판단 필요"로 보고한다(2026-11-06: targeting.lua "Controlled"를 바꾸면서 ui.lua "controlled"를 인용한
# world/combat.md 3곳까지 바꿨다가 되돌렸다).
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


def _alternation(words: set[str]) -> re.Pattern[str]:
    return re.compile("|".join(re.escape(w) for w in sorted(words, key=len, reverse=True)))


def follow_values(
    changes: list[Change],
    en_text: str,
    ko_text: str,
    others: dict[str, list[str]],
    values: set[str] | frozenset[str] = frozenset(),
) -> tuple[str, list[str]]:
    """설명서 한 파일의 인용을 새 값으로 바꾼다. others: 옛 값 → 그 값을 지금도 쓰는 다른 키들의 영어.
    values: 지금 koKR 값 전체.

    옛 값, 그리고 옛 값을 품은 더 긴 값(다른 키의 값, 이번에 바뀐 새 값)을 길이 순 정규식 하나로 찾아
    한 번에 바꾼다. 품은 값은 그대로 두므로 "주시 대상 강화 효과" 속 "대상 강화 효과"는 바뀌지 않고,
    앞 치환의 결과를 뒤 치환이 다시 보지 않으며, 여러 번 돌려도 결과가 같다.
    """
    log: list[str] = []
    keep = set(values) | {c.new for c in changes} | {c.old for c in changes}
    replace: dict[str, tuple[str, Change]] = {}
    guards: set[str] = set()
    for ch in changes:
        if ch.old == ch.new:
            continue
        short = len(ch.old) < LONG
        needle, target = (f'"{ch.old}"', f'"{ch.new}"') if short else (ch.old, ch.new)
        mine = set() if short else {v for v in keep if ch.old in v and v != ch.old}
        count = sum(m.group(0) == needle for m in _alternation({needle, *mine}).finditer(ko_text))
        if not count or not _mentions(en_text, ch.en, short):
            continue
        # 이번에 함께 바뀐 키 가운데 옛 값은 같고 새 값이 다른 키도 경쟁자다. 새 값까지 같으면 어느 키로
        # 바꿔도 결과가 같으므로 경쟁자가 아니다.
        peers = [c.en for c in changes if c is not ch and c.old == ch.old and c.new != ch.new]
        rivals = [e for e in [*others.get(ch.old, []), *peers] if _mentions(en_text, e, short)]
        if rivals:
            log.append(f"판단 필요: {ch.old!r} {count}곳, 원문이 {ch.en!r}와 {rivals}를 모두 인용")
            continue
        replace[needle] = (target, ch)
        guards |= mine
    if not replace:
        return ko_text, log
    counts: Counter[str] = Counter()

    def sub(m: re.Match[str]) -> str:
        hit = replace.get(m.group(0))
        if not hit:
            return m.group(0)
        counts[m.group(0)] += 1
        return hit[0]

    out = _alternation({*replace, *guards}).sub(sub, ko_text)
    log += [f"{counts[n]}x {ch.old} -> {ch.new}" for n, (_, ch) in replace.items() if counts[n]]
    return out, log


def follow_all(
    changes: list[Change],
    others: dict[str, list[str]],
    values: set[str],
    *,
    en_root: Path = EN_ROOT,
    ko_root: Path = KO_ROOT,
) -> tuple[dict[Path, str], list[str]]:
    """한국어 설명서 전체에 follow_values 를 적용해 (바뀌는 파일 → 새 내용, 로그)를 돌려준다.

    쓰지는 않는다. sync_locale 이 koKR 과 함께 한 번에 써야, 중간에 실패해도 koKR 만 바뀐 채 남지 않는다.
    """
    if not ko_root.exists():
        return {}, [f"설명서 폴더 없음, 건너뜀: {ko_root}"]
    outputs: dict[Path, str] = {}
    log: list[str] = []
    for ko_path in sorted(ko_root.rglob("*.md")):
        rel = ko_path.relative_to(ko_root)
        en_path = en_root / rel
        if not en_path.exists():
            continue
        text = ko_path.read_text(encoding="utf-8")
        out, lines = follow_values(changes, en_path.read_text(encoding="utf-8"), text, others, values)
        log += [f"{rel.as_posix()}: {line}" for line in lines]
        if out != text:
            outputs[ko_path] = out
    return outputs, log


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


def source_diff(ko_text: str, rel: str, repo: Path = WOWVISION_DIR) -> str:
    """번역 파일 첫 줄의 원문 커밋 이후 영어 원문의 변경(git diff). 바뀌지 않았거나 기록이 없으면 "".

    원문이 바뀐 파일은 이 diff 에 해당하는 곳만 다시 번역하고 평가한다. 파일 전체를 다시 번역하면
    이미 거친 다듬기와 사용자 결정이 사라진다(2026-11-08 사용자 결정).
    """
    m = SOURCE_LINE.match(ko_text)
    if not m:
        return ""
    r = subprocess.run(
        ["git", "-C", str(repo), "diff", m.group(2), "--", f"docs/src/user/en/{rel}"],
        capture_output=True,
        check=True,
    )
    return r.stdout.decode("utf-8")


def _committed_ko(rel: str) -> str:
    """마지막으로 커밋된 번역 파일. 번역자가 첫 줄의 원문 커밋을 고친 뒤에도 평가 단계가 같은 diff 를 보게 한다."""
    r = subprocess.run(
        ["git", "-C", str(WOWVISION_DIR), "show", f"HEAD:docs/src/user/ko/{rel}"],
        capture_output=True,
        check=False,
    )
    return r.stdout.decode("utf-8") if r.returncode == 0 else ""


def main() -> int:
    cmd, rest = sys.argv[1], sys.argv[2:]
    if cmd == "diff":
        print(source_diff(_committed_ko(rest[0]), rest[0]) or "원문 변경 없음")
        return 0
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
        ko = (KO_ROOT / rel).read_text(encoding="utf-8")
        data = {"file": rel, "en_path": f"wowvision-ko/WowVision/docs/src/user/en/{rel}",
                "ko_path": f"wowvision-ko/WowVision/docs/src/user/ko/{rel}", "en": en,
                "ko": ko, "terms": term_sheet(en, locale_pairs())}  # fmt: skip
        if d := source_diff(_committed_ko(rel), rel):
            data["en_diff"] = d
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

"""설명서 번역 도구: 원문과 번역문의 구조 대조, 앵커 검사, koKR 값 변경 따라가기.

koKR 값이 바뀌면 설명서의 화면 문구 인용도 따라 바뀌어야 한다(`follow_all`). tools.sync_locale 이
koKR 을 쓸 때 부르므로 따로 실행하지 않는다.

사용:
  uv run python -m tools.manual check [<상대경로>...]  # 번역문 기계 검사(없으면 번역된 전체)
  uv run python -m tools.manual diff <상대경로>          # 커밋된 번역의 원문 커밋 이후 영어 원문의 변경
상대경로는 docs/src/user/en 기준(예: basics/interface.md). 번역문은 같은 상대경로의 ko 폴더.
"""

from __future__ import annotations

import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from tools.glossary import Term, _excepted, load_glossary, violations
from tools.locale_lib import JOSA_WORDS, WOWVISION_DIR

EN_ROOT = WOWVISION_DIR / "docs" / "src" / "user" / "en"
KO_ROOT = WOWVISION_DIR / "docs" / "src" / "user" / "ko"
SOURCE_LINE = re.compile(r"^<!-- source: docs/src/user/en/(\S+) @ ([0-9a-f]{7,40}) -->\n")
_HEADING = re.compile(r"^(#{1,6}) +(.*?)\s*$", re.MULTILINE)
_FENCE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]*)\)")
_CODE = re.compile(r"`[^`\n]+`")
# 설명서는 합니다체. 문장 끝의 해요체 어미는 기계 검사로 잡는다.
_HAEYO = re.compile(r"[가-힣]*(?:세요|해요|에요|예요|어요|아요|지요|죠)(?=[.!?)\s]|$)", re.MULTILINE)
# 본문은 바꾸다·바뀌다 대신 변경하다·변경되다(docs/decisions.tsv 2026-11-09, docs/translation-guide.md 낱말 표).
# 따옴표 인용은 화면 문구라 실물 그대로 둔다("바꾸기"는 koKR Replace 값). 맞바꾸다(교환)는 다른 낱말이다.
_BAKKUDA = re.compile(r"(?<!맞)(?:바꾸|바꿉|바꿔|바꿨|바꾼|바꿀|바꿈|바뀌|바뀝|바뀐|바뀔|바뀜)[가-힣]*")
_QUOTED = re.compile(r'"[^"\n]*"')
_LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+\.) +", re.MULTILINE)

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


# 바꾼 값 바로 뒤의 받침 조사. 뒤에 한글이 이어지면("이다") 조사로 보지 않는다.
_JOSA = f"(?:({JOSA_WORDS})(?![가-힣]))?"
_JOSA_PAIRS = {"을": "를", "이": "가", "은": "는", "과": "와", "이라고": "라고", "이라는": "라는"}


def fit_josa(word: str, josa: str) -> str:
    """word 의 마지막 글자 받침에 맞는 조사. 마지막이 한글이 아니면(숫자, 영어) 그대로 둔다."""
    code = ord(word[-1]) - 0xAC00 if word else -1
    if not 0 <= code < 11172:
        return josa
    final = code % 28  # 0 받침 없음, 8 ㄹ
    if josa in ("으로", "로"):
        return "로" if final in (0, 8) else "으로"
    pair = next((p for p in _JOSA_PAIRS.items() if josa in p), None)
    if pair is None:
        return josa
    return pair[0] if final else pair[1]


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
        hit = replace.get(m.group(1))
        if not hit:
            return m.group(0)
        counts[m.group(1)] += 1
        josa = m.group(2) or ""
        # 받침이 다른 값으로 바뀌면 뒤 조사도 따라 바꾼다(2026-11-07 "경보를" → "알림를" 사례).
        return hit[0] + (fit_josa(hit[0].strip('"'), josa) if josa else "")

    out = re.compile(f"({_alternation({*replace, *guards}).pattern}){_JOSA}").sub(sub, ko_text)
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
    tables, columns, rows = [], [], 0
    for line in body.splitlines() + [""]:
        if line.lstrip().startswith("|"):
            # 머리 행만 세면 데이터 행에서 빠진 칸을 놓친다. 행마다 칸 수를 남긴다.
            columns.append(len(re.split(r"(?<!\\)\|", line.strip().strip("|"))))
            rows += 1
        elif rows:
            tables.append(rows)
            rows = 0
    return {
        "headings": [len(m.group(1)) for m in _HEADING.finditer(body)],
        "tables": tables,
        "columns": columns,
        "lists": [len(_LIST_ITEM.findall(body))],
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


# 저장소 문서(README, 지침, 스킬, docs)용. 영어 that·it 을 옮긴 "그 X"와 "~것입니다" 결말은
# 사람이 쓰는 문서에 남기 쉬운 번역투다. 번역 설명서는 바로 앞 명사를 가리키는 "그 X"를 허용하므로
# check() 에는 넣지 않는다(docs/translation-guide.md `### 문체`).
# 그 뒤·그 전·그 밖에 같은 시간·범위 관용 표현은 지시어 번역투가 아니라서 뺀다.
# "해당 X"도 같은 지시어다("해당하다" 동사는 띄어 쓰지 않으므로 걸리지 않고, "해당 없음"은 지시어가 아니다).
_DEMONSTRATIVE = re.compile(
    r"(?<![가-힣])(?:그(?: (?!(?:뒤|전|후|밖|외|다음|사이|대신|때|결과|동안)[에로는은의만도서]*(?![가-힣]))[가-힣]+|것[가-힣]*)"
    r"|해당 (?!없)[가-힣]+)"
)
_FILLER_ENDING = re.compile(r"[가-힣]*것(?:입니다|이다)")


def doc_style_problems(md: str) -> list[str]:
    """코드, 코드 블록, 따옴표 인용을 뺀 본문에서 지시어 "그 X", "~것입니다" 결말, 해요체를 찾는다."""
    body = _QUOTED.sub("", _CODE.sub("", _strip_fences(md)))
    problems = []
    for label, pattern in (
        ("지시어(가리키는 명사로)", _DEMONSTRATIVE),
        ('"~것입니다" 결말', _FILLER_ENDING),
        ("해요체(합니다체로)", _HAEYO),
    ):
        if found := [m.group(0) for m in pattern.finditer(body)]:
            problems.append(f"{label} {len(found)}곳: {', '.join(sorted(set(found)))}")
    return problems


def check(en: str, ko: str, ko_path: Path, terms: list[Term] | None = None) -> list[str]:
    """terms: 확정 용어집(없으면 docs/glossary.tsv). 원문의 코드는 빼고 대조한다."""
    problems = []
    try:
        rel = ko_path.resolve().relative_to(KO_ROOT.resolve()).as_posix()
    except ValueError:
        rel = ko_path.name
    entries = {("manual", rel): (_CODE.sub("", _strip_fences(en)), ko)}
    terms = load_glossary() if terms is None else terms
    problems += [f"용어집: {v}" for v in violations(terms, entries)]
    if not SOURCE_LINE.match(ko):
        problems.append("첫 줄에 원문 기록(<!-- source: docs/src/user/en/... @ 커밋 -->)이 없다")
    a, b = structure(en), structure(ko)
    labels = {
        "headings": "제목 수준",
        "tables": "표 행 수",
        "columns": "표 열 수",
        "lists": "목록 항목 수",
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
    # 용어집에 오른 이름(게임 탭 "무엇이 바뀌었나요?" 등)은 따옴표가 없어도 실물 그대로다.
    body = _QUOTED.sub("", _CODE.sub("", _strip_fences(ko)))
    names = {k for term in terms for k in term.ko if _BAKKUDA.search(k)}
    bakkuda = _BAKKUDA.findall(_alternation(names).sub("", body) if names else body)
    if bakkuda:
        problems.append(
            f"바꾸다·바뀌다 {len(bakkuda)}곳(변경하다·변경되다로): {', '.join(sorted(set(bakkuda))[:8])}"
        )
    # 용어집 avoid 열: 쓰지 않기로 한 직역(2026-11-13 사용자 결정 대응표). 따옴표 인용은 화면 문구라 뺀다.
    en_plain = _CODE.sub("", _strip_fences(en))
    for term in terms:
        if not term.avoid or _excepted(f"manual::{rel}", term.except_ids):
            continue
        if term.en and not re.search(r"\b" + re.escape(term.en) + r"s?\b", en_plain, re.IGNORECASE):
            continue
        if found := [a for a in term.avoid if a in body]:
            problems.append(
                f"피할 표현: {', '.join(found)} -> {'|'.join(term.ko)} ({term.en or '설명서 전체'})"
            )
    for target in _LINK.findall(_strip_fences(ko)):
        if "#" not in target or target.startswith(("http://", "https://")):
            continue
        file_part, frag = target.split("#", 1)
        dest = ko_path if not file_part else (ko_path.parent / file_part).resolve()
        if frag not in _anchors(dest):
            problems.append(f"앵커 없음: {target} (대상 {dest.name}의 제목에서 만든 앵커와 맞지 않는다)")
    return problems


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

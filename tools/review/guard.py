"""평가 절차의 기계 검사: 판정 근거가 허용된 1차 자료인지, 평가자가 격리 폴더 밖에 접근했는지."""

from __future__ import annotations

import re

# 판정 근거로 인정하는 자료. 번역 쪽이 쓴 문서(계획, 반박문, 평가 기록)는 근거가 아니다.
# "/"로 끝나는 것은 그 폴더 안 파일, 나머지는 정확히 그 파일만.
ALLOWED_EVIDENCE = (
    "wowvision-ko/WowVision/",
    "wowvision-ko/wowvision-installer/",
    "wowvision-ko/vision-locale/enUS/",
    "wowvision-ko/vision-locale/koKR/",
    "wowwork/cache/gs_enUS.csv",
    "wowwork/cache/gs_koKR.csv",
    "wowwork/cache/game_terms.tsv",
    "wowwork/docs/translation-guide.md",
    "wowwork/docs/decisions.tsv",
    "wowwork/docs/glossary.tsv",
)
_LINE_SUFFIX = re.compile(r":\d+(?:-\d+)?$")
_ABS_PATH = re.compile(r"[A-Za-z]:[\\/][^\s\"'`;|<>,)]*")


def _norm(path: str) -> str:
    # 셸 인용 때문에 구분자가 두 겹(C:\\Program)으로 들어오는 경우가 있다.
    return re.sub(r"/{2,}", "/", path.replace("\\", "/")).strip()


def valid_evidence(sources: list[str]) -> bool:
    """비어 있지 않고 전부 허용 자료여야 한다. "input"은 평가 입력(원문·번역·코드 사용처)이다."""
    if not sources:
        return False
    return all(_norm(src) == "input" or _allowed_path(src) for src in sources)


def _allowed_path(src: str) -> bool:
    """줄 표시(:12, :12-15)를 뗀 경로가 허용 파일과 정확히 같거나 허용 폴더 안에 있어야 한다.

    허용 항목은 경로 구분자 경계에서 시작해야 한다(notwowwork/... 불가). 절대 경로도 된다.
    """
    path = _LINE_SUFFIX.sub("", _norm(src)).lower()
    if "#" in path or "?" in path or "/../" in f"/{path}/":
        return False
    for allowed in (a.lower() for a in ALLOWED_EVIDENCE):
        idx = path.find(allowed)
        if idx < 0 or (idx > 0 and path[idx - 1] != "/"):
            continue
        rest = path[idx + len(allowed) :]
        if allowed.endswith("/") and rest:
            return True
        if not allowed.endswith("/") and rest == "":
            return True
    return False


def foreign_paths(text: str, root: str) -> list[str]:
    """text 안의 절대 경로 중 root 밖을 가리키는 것(정규화, 중복 제거, 등장 순)."""
    base = _norm(root).rstrip("/").lower()
    seen: list[str] = []
    for m in _ABS_PATH.finditer(text):
        p = _norm(m.group(0))
        if not (p.lower() == base or p.lower().startswith(base + "/")) and p not in seen:
            seen.append(p)
    return seen

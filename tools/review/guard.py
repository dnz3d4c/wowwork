"""평가 절차의 기계 검사: 판정 근거가 허용된 1차 자료인지, 평가자가 격리 폴더 밖에 접근했는지."""

from __future__ import annotations

import re

# 판정 근거로 인정하는 자료. 번역 쪽이 쓴 문서(계획, 반박문, 평가 기록)는 근거가 아니다.
ALLOWED_EVIDENCE = (
    "wowvision-ko/WowVision/",
    "wowvision-ko/vision-locale/enUS/",
    "wowvision-ko/vision-locale/koKR/",
    "wowwork/cache/gs_",
    "wowwork/cache/game_terms.tsv",
    "wowwork/docs/translation-guide.md",
    "wowwork/docs/decisions.tsv",
    "wowwork/docs/glossary.tsv",
)
_ABS_PATH = re.compile(r"[A-Za-z]:[\\/][^\s\"'`;|<>,)]*")


def _norm(path: str) -> str:
    # 셸 인용 때문에 구분자가 두 겹(C:\\Program)으로 들어오는 경우가 있다.
    return re.sub(r"/{2,}", "/", path.replace("\\", "/")).strip()


def valid_evidence(sources: list[str]) -> bool:
    """비어 있지 않고 전부 허용 자료여야 한다. "input"은 평가 입력(원문·번역·코드 사용처)이다."""
    if not sources:
        return False
    for src in sources:
        s = _norm(src)
        if s == "input":
            continue
        if not any(allowed.lower() in s.lower() for allowed in ALLOWED_EVIDENCE):
            return False
    return True


def foreign_paths(text: str, root: str) -> list[str]:
    """text 안의 절대 경로 중 root 밖을 가리키는 것(정규화, 중복 제거, 등장 순)."""
    base = _norm(root).rstrip("/").lower()
    seen: list[str] = []
    for m in _ABS_PATH.finditer(text):
        p = _norm(m.group(0))
        if not (p.lower() == base or p.lower().startswith(base + "/")) and p not in seen:
            seen.append(p)
    return seen

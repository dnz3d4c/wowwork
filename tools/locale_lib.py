"""WowVision 로케일 Lua 파일을 읽는 공용 함수."""

from __future__ import annotations

import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
# 비공개 복제 저장소들(dnz3d4c/vision-locale, WowVision, wowvision-installer)이 모인 폴더
KO_WORK_ROOT = REPO_ROOT.parent / "wowvision-ko"
# 원본 앱 코드. 키가 어떻게 쓰이는지 확인할 때 검색한다.
WOWVISION_DIR = KO_WORK_ROOT / "WowVision"

# L["key"] = true  /  L["key"] = "value"  (뒤에 -- 주석 허용)
_ENTRY = re.compile(r'^L\["((?:[^"\\]|\\.)*)"\] = (true|"((?:[^"\\]|\\.)*)")\s*(?:--.*)?$')
# Lua string.format 지정자. %% 는 리터럴이라 제외한다.
_FORMAT = re.compile(r"%(?:\d+\$)?[-+ #0]*\d*(?:\.\d+)?[sdifgxXcqeE]")


def upstream_locale_dir() -> Path:
    """vision-locale 복제 저장소 경로(enUS 원문과 koKR 번역이 함께 있다). WOWVISION_LOCALE 로 덮어쓸 수 있다."""
    env = os.environ.get("WOWVISION_LOCALE")
    if env:
        return Path(env)
    return KO_WORK_ROOT / "vision-locale"


KOKR_DIR = upstream_locale_dir() / "koKR"


def unescape(s: str) -> str:
    return re.sub(r"\\(.)", lambda m: {"n": "\n", "t": "\t"}.get(m.group(1), m.group(1)), s)


def parse_locale_file(path: Path) -> dict[str, str]:
    """키 → 실제 문자열. `true` 는 키 자체를 값으로 쓴다(AceLocale 기본 로케일 규칙)."""
    entries: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = _ENTRY.match(line.strip())
        if not m:
            continue
        key = unescape(m.group(1))
        entries[key] = key if m.group(2) == "true" else unescape(m.group(3))
    return entries


def format_specs(s: str) -> list[str]:
    """서식 지정자 목록. 위치 지정(%1$s)은 종류만 남겨 비교한다."""
    stripped = s.replace("%%", "")
    return sorted(re.sub(r"\d+\$", "", spec) for spec in _FORMAT.findall(stripped))

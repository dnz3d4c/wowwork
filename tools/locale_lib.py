"""WowVision 로케일 Lua 파일을 읽는 공용 함수."""

from __future__ import annotations

import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KOKR_DIR = REPO_ROOT / "koKR"

# L["key"] = true  /  L["key"] = "value"  (뒤에 -- 주석 허용)
_ENTRY = re.compile(r'^L\["((?:[^"\\]|\\.)*)"\] = (true|"((?:[^"\\]|\\.)*)")\s*(?:--.*)?$')
# Lua string.format 지정자. %% 는 리터럴이라 제외한다.
_FORMAT = re.compile(r"%(?:\d+\$)?[-+ #0]*\d*(?:\.\d+)?[sdifgxXcqeE]")


def upstream_locale_dir() -> Path:
    """원문(enUS)이 있는 locale 서브모듈 경로. WOWVISION_LOCALE 로 덮어쓸 수 있다."""
    env = os.environ.get("WOWVISION_LOCALE")
    if env:
        return Path(env)
    return REPO_ROOT.parent / "wowvision" / "upstream" / "WowVision" / "locale"


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

"""koKR 파일에서 지정한 키의 번역을 일괄 교체한다. 용어 통일용 단발 도구.

사용: uv run python -m tools.apply_fixes  (FIXES 를 고친 뒤 실행)
"""

from __future__ import annotations

import re

from tools.locale_lib import KOKR_DIR

# 키 → 새 번역 (모든 koKR 파일에 적용)
FIXES: dict[str, str] = {}


def lua_quote(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def apply(fixes: dict[str, str]) -> int:
    changed = 0
    for path in sorted(KOKR_DIR.glob("*.lua")):
        text = path.read_text(encoding="utf-8")
        new = text
        for key, val in fixes.items():
            pattern = re.compile(r'^(L\[' + re.escape(lua_quote(key)) + r'\] = )"(?:[^"\\]|\\.)*"', re.MULTILINE)
            quoted = lua_quote(val)
            new, n = pattern.subn(lambda m, q=quoted: m.group(1) + q, new)
            changed += n
        if new != text:
            path.write_text(new, encoding="utf-8")
    return changed


if __name__ == "__main__":
    print(f"{apply(FIXES)} lines changed")

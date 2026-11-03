"""koKR 번역을 게임에 설치된 WowVision 에 넣는다.

사용: uv run python -m tools.install [AddOns 경로]
경로를 생략하면 판다리아의 안개 클래식(_classic_) AddOns 폴더를 쓴다.
기존 koKR 폴더는 지우고 새로 복사하며, locale/modules.xml 에 koKR 포함 줄을 한 번만 추가한다.
WowVision 을 다시 설치하면 이 변경이 사라지므로 이 스크립트를 다시 실행한다.
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

from tools.locale_lib import KOKR_DIR

INCLUDE_LINE = '<Include file="koKR/modules.xml" />'
DEFAULT_ADDONS = Path(r"C:\Program Files (x86)\World of Warcraft\_classic_\Interface\AddOns")
_LAST_INCLUDE = re.compile(r'^([ \t]*)<Include file="[^"]+" />[ \t]*$', re.MULTILINE)


def add_include(xml: str) -> str:
    """마지막 <Include> 뒤에 koKR 줄을 넣는다. 이미 있으면 그대로 돌려준다."""
    if INCLUDE_LINE in xml:
        return xml
    matches = list(_LAST_INCLUDE.finditer(xml))
    if not matches:
        raise ValueError("locale/modules.xml 에서 <Include> 줄을 찾지 못했다")
    last = matches[-1]
    return xml[: last.end()] + "\n" + last.group(1) + INCLUDE_LINE + xml[last.end() :]


def install(addons: Path, src: Path = KOKR_DIR) -> Path:
    locale = addons / "WowVision" / "locale"
    xml_path = locale / "modules.xml"
    if not xml_path.exists():
        raise FileNotFoundError(f"WowVision 이 설치되어 있지 않다: {xml_path}")
    dest = locale / "koKR"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    xml_path.write_text(add_include(xml_path.read_text(encoding="utf-8")), encoding="utf-8")
    return dest


def main() -> None:
    addons = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ADDONS
    dest = install(addons)
    print(f"설치 완료: {dest} ({len(list(dest.glob('*.lua')))}개 파일)")


if __name__ == "__main__":
    main()

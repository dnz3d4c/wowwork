"""로그인 툴 한국어 판정 규칙을 실제 OCR 결과로 검사한다.

규칙은 ../wowvision-ko/Sku-WoW-Addon-TBC 의 ko 브랜치 flows.ahk 에 있다(AutoHotkey에는 테스트 틀이 없다).
여기서는 그 파일에서 정규식을 뽑아 2026-11-07 측정(게임 글꼴로 그린 카드 6,000여 장)에서 나온
OCR 문자열에 적용한다.

- 레벨 줄은 "%d 레벨 %s"(CHARACTER_SELECT_INFO). 작은 창에서 OCR이 "레벨"을 "해일"로 읽어
  (배율 0.8에서 레벨 단어 인식 26.5%) 카드가 사라졌다. 그래서 모양으로 판정한다.
- 이름에 "레벨"이 들어간 캐릭터("레벨이어야")를 카드로 오인하면 안 된다.
"""

import re
from pathlib import Path

import pytest

FLOWS = Path(__file__).resolve().parents[2] / "wowvision-ko" / "Sku-WoW-Addon-TBC" / "logintool" / "v2" / "includes" / "flows.ahk"
pytestmark = pytest.mark.skipif(not FLOWS.exists(), reason="Sku-WoW-Addon-TBC 복제본 없음")


def _patterns() -> list[str]:
    src = FLOWS.read_text(encoding="utf-8-sig")
    body = src[src.index("IsKoreanLevelLine(text) {"):]
    body = body[: body.index("\n}")]
    return [p.replace('""', '"') for p in re.findall(r'RegExMatch\(text, "((?:[^"]|"")*)"\)', body)]


def is_level_line(text: str) -> bool:
    return any(re.search(p, text) for p in _patterns())


@pytest.mark.parametrize("text", [
    "1 레벨 성기사", "60 레벨 흑마법사", "15 해일 사남꾼", "52 해일 도적", "36 레벨 옥마법사",
    "9 레벨 사제 (유령)", "56 레벨 옥0t법사",
])
def test_level_lines_found(text: str) -> None:
    assert is_level_line(text)


@pytest.mark.parametrize("text", [
    "까다로운 일렁", "레벨이어야", "레벨이01약", "던 모로", "0 0 人", "0 과|人y 자", "접속하기", "",
])
def test_other_lines_not_level_lines(text: str) -> None:
    assert not is_level_line(text)

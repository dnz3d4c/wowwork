"""로그인 툴 번역 평가용 어댑터(tools/logintool_loc.py)를 검사한다.

평가 대상은 data/localization/koKR.txt 와, forever.ahk 안에서 툴이 직접 말하는 낱말(Map 의 "ko" 값)이다.
화면 판별 문구("login_button", Map(...) 꼴)와 경험 사전 설정 카드는 게임 화면 글자와 같아야 하므로 뺀다.
"""

from pathlib import Path

from tools.logintool_loc import apply_forever, apply_txt, forever_items, parse_txt

FOREVER = '''global gFvStrings := Map(
    "login_button", Map("de", "Einloggen", "en", "Log In", "fr", "Connexion", "ko", "로그인"),
)
FvDropdownWord() {
    return Map("de", "Drop-down", "en", "Dropdown", "fr", "Menu déroulant", "ko", "드롭다운")[FvLangKey()]
}
    pink := Map("de", "rosa", "en", "pink", "fr", "rose", "ko", "분홍색")[L]
        hue := Map("de", "rosa", "en", "pink", "fr", "rose", "ko", "분홍색")[L]
    "ko_button", "버튼",
'''


def test_parse_txt_strips_bom_and_keeps_first() -> None:
    text = "﻿English==영어\nselected==선택됨\nselected==다른 값\nbad line\n"
    assert parse_txt(text) == {"English": "영어", "selected": "선택됨"}


def test_forever_items_skip_anchors_and_dedupe() -> None:
    items = forever_items(FOREVER)
    assert [(i["en"], i["ko"]) for i in items] == [("Dropdown", "드롭다운"), ("pink", "분홍색"), ("Button", "버튼")]
    assert items[0]["de"] == "Drop-down" and items[0]["fr"] == "Menu déroulant"
    assert items[0]["id"] == "forever.ahk::Dropdown"


def test_apply_forever_changes_every_occurrence_and_nothing_else() -> None:
    out = apply_forever(FOREVER, {"forever.ahk::pink": "연분홍색", "forever.ahk::Button": "단추"})
    assert out.count('"ko", "연분홍색"') == 2
    assert '"ko_button", "단추"' in out
    assert '"ko", "로그인"' in out and '"ko", "드롭다운"' in out


def test_apply_forever_rejects_unknown_id() -> None:
    try:
        apply_forever(FOREVER, {"forever.ahk::nope": "x"})
    except KeyError:
        return
    raise AssertionError("unknown id must fail")


def test_apply_txt_rewrites_only_named_keys(tmp_path: Path) -> None:
    raw = "﻿English==영어\r\nwait==기다려 주세요.\r\n".encode()
    out = apply_txt(raw, {"koKR.txt::wait": "잠시 기다리세요."})
    assert out == "﻿English==영어\r\nwait==잠시 기다리세요.\r\n".encode()



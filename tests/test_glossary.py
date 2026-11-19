"""용어집 검사: 확정 용어 누락과 되돌린 번역을 잡는다."""

from __future__ import annotations

from tools.glossary import Term, violations


def test_glossary_flags_missing_term_and_honours_alternatives_and_exceptions() -> None:
    terms = [
        Term("beacon", ("비컨",), frozenset(), ""),
        Term("the route goes on after it", ("이후 경로 계속", "그 후 경로가 이어집니다"), frozenset(), ""),
        Term("healer", ("치유 전담",), frozenset({"a.lua::spirit healer"}), ""),
    ]
    entries = {
        ("a.lua", "Beacon Sound"): ("Beacon Sound", "신호 소리"),
        ("a.lua", "Dive"): ("Dive; the route goes on after it", "잠수; 이후 경로 계속"),
        ("a.lua", "Wait"): ("Wait; the route goes on after it", "기다리십시오; 그 후 경로가 이어집니다"),
        ("a.lua", "spirit healer"): ("spirit healer", "영혼의 치유사"),
        ("a.lua", "Beacons"): ("Beacons", "비컨 목록"),
    }
    assert violations(terms, entries) == ["a.lua::Beacon Sound: 'beacon' -> '비컨' 없음 ('신호 소리')"]


def test_glossary_blocks_reverted_translations() -> None:
    """2026-11-06 최종 검수에서 다시 들어올 뻔한 번역 두 개를 확정 용어집이 막는다.

    - "카메라 따라가기 방식": 게임 공식 CAMERA_FOLLOWING_STYLE은 "시점 전환 방식". 2026-11-05에 한 번 되돌렸는데 다시 제안됐다.
    - "추가 전리품 주사위": "추가 전리품"은 Bonus Loot의 공식 번역이다. bonus roll의 공식 번역은 "보너스 주사위".
    """
    from tools.glossary import load_glossary

    camera_en = "You can change the camera following style in the game options under Controls."
    entries = {
        ("navigation.lua", "camera"): (
            camera_en,
            "카메라 따라가기 방식은 게임 설정의 조작 설정에서 바꿀 수 있습니다.",
        ),
        ("bindings.lua", "Roll Bonus"): ("Roll Bonus", "추가 전리품 주사위"),
    }
    assert len(violations(load_glossary(), entries)) == 2
    ok = {
        ("navigation.lua", "camera"): (
            camera_en,
            "시점 전환 방식은 게임 설정의 조작 설정에서 바꿀 수 있습니다.",
        ),
        ("bindings.lua", "Roll Bonus"): ("Roll Bonus", "보너스 주사위"),
    }
    assert violations(load_glossary(), ok) == []

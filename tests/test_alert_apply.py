"""alert=알림 결정을 koKR 반영 목록으로 만드는 규칙."""

from __future__ import annotations

from tools.review.alert_apply import plan


def test_alert_keys_become_allim_and_buffered_is_fixed() -> None:
    en = {
        ("a.lua", "TTS Alert"): "TTS Alert",
        ("speech.lua", "Buffered"): "Buffered",
        ("a.lua", "x"): "Announce",
    }
    ko = {
        ("a.lua", "TTS Alert"): "TTS 경보",
        ("speech.lua", "Buffered"): "대기열",
        ("a.lua", "x"): "오류 알림",
    }
    rows, odd = plan(en, ko)
    assert rows == [
        ["a.lua", "TTS Alert", "TTS 경보", "TTS 알림"],
        ["speech.lua", "Buffered", "대기열", "모아 말하기"],
    ]
    assert odd == []


def test_gyeongbo_without_alert_in_english_is_reported() -> None:
    rows, odd = plan({("a.lua", "w"): "Warning"}, {("a.lua", "w"): "위험 경보"})
    assert rows == []
    assert odd == ["a.lua::w = 위험 경보"]

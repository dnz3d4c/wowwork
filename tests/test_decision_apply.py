"""2026-11-07 사용자 결정의 설명서 일괄 반영: 경보→알림(조사 맞춤), 버전 이름 영어."""

from __future__ import annotations

from tools.review.decision_apply import apply_text


def test_gyeongbo_becomes_allim_with_particles() -> None:
    src = "경보는 묻지 않아도 알려 줍니다. 경보를 끄고, 경보가 울리면 경보와 소리, 경보로 바꾸거나 경보나 출력. 경보입니다. 경보의 경보에는"
    out = apply_text(src)
    assert out == (
        "알림은 묻지 않아도 알려 줍니다. 알림을 끄고, 알림이 울리면 알림과 소리, 알림으로 바꾸거나 알림이나 출력. 알림입니다. 알림의 알림에는"
    )


def test_version_names_become_english() -> None:
    assert apply_text("리테일과 클래식 시대에서") == "Retail과 Classic Era에서"


def test_announce_errors_follows_kokr() -> None:
    assert (
        apply_text("오류 알리기와 오류 알리기를 켜면 오류 알리기") == "오류 알림과 오류 알림을 켜면 오류 알림"
    )


def test_code_spans_are_untouched() -> None:
    assert apply_text("`경보는` 경보는") == "`경보는` 알림은"


def test_particle_after_parenthesis_follows_the_noun() -> None:
    """조사는 괄호가 아니라 그 앞 낱말의 받침을 따른다(2026-11-07 회귀 확인 2회차에서 발견: "알림(켬)와")."""
    assert apply_text("TTS 경보(켬)와 소리 경보(끔)가 있고, 경보(대화 등)는") == (
        "TTS 알림(켬)과 소리 알림(끔)이 있고, 알림(대화 등)은"
    )

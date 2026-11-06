"""다듬기 회귀 확인 입력: 다듬기 전후로 바뀐 줄 쌍."""

from __future__ import annotations

from tools.review.polish_regression_input import changed_lines


def test_changed_lines_pairs_old_and_new() -> None:
    old = "# 제목\n\n첫 문장입니다.\n그 화면을 쓰는 방법입니다.\n끝.\n"
    new = "# 제목\n\n첫 문장입니다.\n단축키 화면 사용법입니다.\n끝.\n"
    assert changed_lines(old, new) == [
        {"before": "그 화면을 쓰는 방법입니다.", "after": "단축키 화면 사용법입니다."}
    ]


def test_changed_lines_empty_when_same() -> None:
    assert changed_lines("a\nb\n", "a\nb\n") == []


def test_changed_lines_keeps_uneven_blocks() -> None:
    out = changed_lines("a\nx\ny\nb\n", "a\nz\nb\n")
    assert out == [{"before": "x\ny", "after": "z"}]

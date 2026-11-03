from __future__ import annotations

from pathlib import Path

from tools.apply_fixes import apply
from tools.locale_lib import parse_locale_file


def test_replaces_value_with_special_chars(tmp_path: Path) -> None:
    f = tmp_path / "x.lua"
    f.write_text('L["A"] = "old"\nL["B"] = "keep"\n', encoding="utf-8")
    value = 'a\\b"c'  # 백슬래시와 큰따옴표
    assert apply({"A": value}, tmp_path) == 1
    assert parse_locale_file(f) == {"A": value, "B": "keep"}

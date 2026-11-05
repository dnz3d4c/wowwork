from __future__ import annotations

from tools.locale_lib import parse_locale_file
from tools.sync_locale import HEADER, read_tsv, rebuild

EN = 'local L = WowVision:translate("enUS")\n\n-- 묶음\nL["A"] = true\nL["Gone"] = true\n\nL["B"] = "Bee"\nL["New"] = true\n'
KO = HEADER + '\nL["A"] = "가"\nL["Old"] = "옛것"\nL["B"] = "비"\nL["Gone2"] = "x"\n'


def test_keeps_existing_and_follows_enus_layout() -> None:
    text, missing = rebuild(EN.replace('L["Gone"] = true\n', ""), KO, {"New": "새것"})
    assert missing == []
    assert text == HEADER + '\n-- 묶음\nL["A"] = "가"\n\nL["B"] = "비"\nL["New"] = "새것"\n'


def test_reports_missing_keys_in_enus_order() -> None:
    _, missing = rebuild(EN, KO, {})
    assert missing == ["Gone", "New"]


def test_new_file_without_korean() -> None:
    text, missing = rebuild('local L = WowVision:translate("enUS")\n\nL["A"] = true\n', None, {"A": "가"})
    assert missing == []
    assert text == HEADER + '\nL["A"] = "가"\n'


def test_new_value_escaping_round_trips(tmp_path) -> None:  # type: ignore[no-untyped-def]
    value = 'a\\b"c\nd'
    text, _ = rebuild('local L = WowVision:translate("enUS")\n\nL["A"] = true\n', None, {"A": value})
    f = tmp_path / "x.lua"
    f.write_text(text, encoding="utf-8")
    assert parse_locale_file(f) == {"A": value}


def test_existing_escaped_line_is_kept_verbatim() -> None:
    ko = HEADER + '\nL["Q \\"x\\""] = "따옴표 \\"x\\"\\n줄"\n'
    text, missing = rebuild('local L = WowVision:translate("enUS")\n\nL["Q \\"x\\""] = true\n', ko, {})
    assert missing == []
    assert text == ko


def test_read_tsv(tmp_path) -> None:  # type: ignore[no-untyped-def]
    f = tmp_path / "t.tsv"
    f.write_text("file\tkey\ten\tko\na.lua\tK\tK\t번역\nb.lua\tE\tE\t\n", encoding="utf-8")
    assert read_tsv(f) == {"a.lua": {"K": "번역"}}

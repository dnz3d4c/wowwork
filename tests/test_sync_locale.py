from __future__ import annotations

from pathlib import Path

import pytest

from tools.locale_lib import parse_locale_file
from tools.sync_locale import (
    HEADER,
    changed_keys,
    load_snapshot,
    read_tsv,
    rebuild,
    save_snapshot,
    write_all,
)

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


def test_changed_english_value_forces_retranslation() -> None:
    en = 'local L = WowVision:translate("enUS")\n\nL["EditBox"] = "Edit box"\n'
    ko = HEADER + '\nL["EditBox"] = "편집"\n'
    _, missing = rebuild(en, ko, {}, changed={"EditBox"})
    assert missing == ["EditBox"]
    text, missing = rebuild(en, ko, {"EditBox": "편집 상자"}, changed={"EditBox"})
    assert missing == []
    assert 'L["EditBox"] = "편집 상자"' in text


def test_changed_keys_compares_snapshot() -> None:
    snap = {("a.lua", "K"): "Edit", ("a.lua", "S"): "Same"}
    assert changed_keys(snap, "a.lua", {"K": "Edit box", "S": "Same", "New": "New"}) == {"K"}


def test_snapshot_round_trip(tmp_path: Path) -> None:
    f = tmp_path / "snap.tsv"
    data = {("a.lua", 'Q "x"'): "tab\there\nline"}
    save_snapshot(f, data)
    assert load_snapshot(f) == data
    assert load_snapshot(tmp_path / "none.tsv") == {}


def test_write_all_leaves_targets_untouched_when_one_fails(tmp_path: Path) -> None:
    ok = tmp_path / "ok.lua"
    ok.write_text("old", encoding="utf-8")
    bad = tmp_path / "no_such_dir" / "bad.lua"
    with pytest.raises(OSError):
        write_all({ok: "new", bad: "x"})
    assert ok.read_text(encoding="utf-8") == "old"
    assert list(tmp_path.glob("*.tmp")) == []


def test_read_tsv(tmp_path) -> None:  # type: ignore[no-untyped-def]
    f = tmp_path / "t.tsv"
    f.write_text("file\tkey\ten\tko\na.lua\tK\tK\t번역\nb.lua\tE\tE\t\n", encoding="utf-8")
    assert read_tsv(f) == {"a.lua": {"K": "번역"}}


def test_unknown_rows_reports_keys_missing_from_enus() -> None:
    """apply.tsv 의 파일·키가 enUS 에 없으면 조용히 버려졌다(2026-11-08 조사)."""
    from tools.sync_locale import unknown_rows

    new = {"ui.lua": {"Ok": "확인", "Typo": "오타"}, "nofile.lua": {"X": "x"}}
    en = {"ui.lua": {"Ok": "Ok"}}
    assert unknown_rows(new, en) == [("nofile.lua", "X"), ("ui.lua", "Typo")]

from __future__ import annotations

import json
from pathlib import Path

from tools.review.build_batch import chunk, code_usages, collect_items, index_sources
from tools.review.gpt_review import build_command, build_prompt

HDR = 'local L = LibStub("AceLocale-3.0"):NewLocale("WowVision", "koKR")\nif not L then return end\n'


def _locale(tmp: Path) -> Path:
    (tmp / "enUS").mkdir()
    (tmp / "koKR").mkdir()
    (tmp / "enUS" / "a.lua").write_text('local L = x\n\nL["Dead"] = true\nL["Q \\"x\\""] = true\n', "utf-8")
    (tmp / "koKR" / "a.lua").write_text(HDR + '\nL["Dead"] = "사망"\nL["Q \\"x\\""] = "인용"\n', "utf-8")
    return tmp


def test_collect_items_pairs_en_and_ko(tmp_path: Path) -> None:
    items = collect_items(_locale(tmp_path))
    assert items == [
        {"id": "a.lua::Dead", "file": "a.lua", "key": "Dead", "en": "Dead", "ko": "사망"},
        {"id": 'a.lua::Q "x"', "file": "a.lua", "key": 'Q "x"', "en": 'Q "x"', "ko": "인용"},
    ]


def test_collect_items_key_filter(tmp_path: Path) -> None:
    items = collect_items(_locale(tmp_path), only={("a.lua", "Dead")})
    assert [i["key"] for i in items] == ["Dead"]


def test_code_usages_finds_escaped_key_and_skips_locale(tmp_path: Path) -> None:
    src = tmp_path / "src"
    (src / "core").mkdir(parents=True)
    (src / "locale").mkdir()
    (src / "core" / "m.lua").write_text('x = 1\nspeak(n .. " " .. L["Dead"])\nL["Q \\"x\\""]\n', "utf-8")
    (src / "locale" / "en.lua").write_text('L["Dead"] = true\n', "utf-8")
    idx = index_sources(src)
    assert code_usages(idx, "Dead") == ['core/m.lua:2: speak(n .. " " .. L["Dead"])']
    assert code_usages(idx, 'Q "x"') == ['core/m.lua:3: L["Q \\"x\\""]']


def test_chunk() -> None:
    assert chunk(list(range(5)), 2) == [[0, 1], [2, 3], [4]]


def test_build_prompt_contains_lens_guide_and_batch(tmp_path: Path) -> None:
    lens = tmp_path / "lens.md"
    lens.write_text("관점: 정확성", "utf-8")
    batch = tmp_path / "b.json"
    batch.write_text(json.dumps({"items": [{"id": "a.lua::Dead"}]}), "utf-8")
    prompt = build_prompt([lens], batch)
    assert "관점: 정확성" in prompt
    assert "a.lua::Dead" in prompt


def test_build_command_is_read_only_with_schema(tmp_path: Path) -> None:
    cmd = build_command(tmp_path / "out.json", tmp_path / "s.json", tmp_path)
    assert cmd[:2] == ["codex", "exec"]
    assert "--output-schema" in cmd
    assert cmd[cmd.index("--sandbox") + 1] == "read-only"
    assert cmd[-1] == "-"

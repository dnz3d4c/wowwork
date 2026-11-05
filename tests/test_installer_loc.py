from __future__ import annotations

from tools.installer_loc import apply_ko, cs_quote, parse_table, unquote

LOC = """    public static class Loc
    {
        private static readonly Dictionary<string, string> En = new Dictionary<string, string>
        {
            ["app.title"]            = "WowVision Installer & Updater",

            // ── wizard navigation ──
            ["nav.next"]             = "&Next >",
            ["q"]                    = "Say \\"hi\\" {0}",
        };

        // ── French ──
        private static readonly Dictionary<string, string> Fr = new Dictionary<string, string>
        {
            ["app.title"]            = "WowVision Installer & Updater",
            ["nav.next"]             = "&Suivant >",
            ["q"]                    = "Dis \\"salut\\" {0}",
        };
    }
}
"""


def test_parse_table_reads_entries_in_order() -> None:
    assert parse_table(LOC, "En") == {
        "app.title": "WowVision Installer & Updater",
        "nav.next": "&Next >",
        "q": 'Say "hi" {0}',
    }


def test_apply_ko_inserts_block_after_last_table_mirroring_english_layout() -> None:
    ko = {"app.title": "WowVision 설치 및 업데이트", "nav.next": "다음(&N) >", "q": '"안녕" {0} 말하기'}
    out, missing = apply_ko(LOC, ko)
    assert missing == []
    assert parse_table(out, "Ko") == ko
    assert out.index("Fr = new") < out.index("Ko = new")
    assert "            // ── wizard navigation ──\n" in out.split("Ko = new")[1]
    assert '            ["nav.next"]             = "다음(&N) >",\n' in out


def test_apply_ko_replaces_existing_block_and_reports_missing() -> None:
    out, _ = apply_ko(LOC, {"app.title": "가", "nav.next": "나", "q": "다 {0}"})
    out2, missing = apply_ko(out, {"app.title": "가2", "nav.next": "나"})
    assert missing == ["q"]
    assert out2 == out  # 빠진 키가 있으면 바꾸지 않는다
    out3, _ = apply_ko(out, {"app.title": "가2", "nav.next": "나", "q": "다 {0}"})
    assert out3.count("Ko = new") == 1
    assert parse_table(out3, "Ko")["app.title"] == "가2"


def test_quote_round_trip() -> None:
    for s in ['a "b" c', "back\\slash", "줄\n바꿈", "{0}…"]:
        assert unquote(cs_quote(s)[1:-1]) == s


def test_installer_items_include_code_usage_and_other_languages(tmp_path) -> None:  # type: ignore[no-untyped-def]
    from tools.installer_loc import installer_items

    src = tmp_path / "src"
    src.mkdir()
    (src / "Loc.cs").write_text(LOC.replace("    }\n}\n", "") + "        };\n    }\n}\n", "utf-8")
    loc_text, _ = apply_ko(LOC, {"app.title": "가", "nav.next": "다음(&N) >", "q": "말 {0}"})
    (src / "Loc.cs").write_text(loc_text, "utf-8")
    (src / "Form.cs").write_text('btn.Text = Loc.Get("nav.next");\nx = Loc.Format("q", n);\n', "utf-8")
    items = installer_items(src)
    nxt = next(i for i in items if i["key"] == "nav.next")
    assert nxt["id"] == "Loc.cs::nav.next"
    assert nxt["en"] == "&Next >" and nxt["ko"] == "다음(&N) >" and nxt["fr"] == "&Suivant >"
    assert nxt["code"] == ['Form.cs:1: btn.Text = Loc.Get("nav.next");']

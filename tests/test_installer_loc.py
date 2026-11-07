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


def test_build_payload_zips_kokr_folder_deterministically(tmp_path) -> None:  # type: ignore[no-untyped-def]
    import zipfile

    from tools.installer_loc import build_payload

    ko = tmp_path / "koKR"
    ko.mkdir()
    (ko / "modules.xml").write_text("<Ui/>", "utf-8")
    (ko / "ui.lua").write_text("L = 1", "utf-8")
    a, b = tmp_path / "a.zip", tmp_path / "b.zip"
    build_payload(ko, a)
    build_payload(ko, b)
    assert a.read_bytes() == b.read_bytes()
    with zipfile.ZipFile(a) as z:
        assert sorted(z.namelist()) == ["koKR/modules.xml", "koKR/ui.lua"]
        assert z.read("koKR/ui.lua") == b"L = 1"


def test_installer_payload_matches_current_kokr() -> None:
    """설치 프로그램에 넣은 payload 가 vision-locale 의 koKR 과 같아야 한다(낡은 번역 배포 방지).

    다르면: uv run python -m tools.installer_loc payload 후 설치 프로그램을 다시 빌드한다.
    """
    import zipfile

    from tools.installer_loc import PAYLOAD
    from tools.locale_lib import KOKR_DIR

    with zipfile.ZipFile(PAYLOAD) as z:
        packed = {n.removeprefix("koKR/"): z.read(n) for n in z.namelist()}
    current = {p.name: p.read_bytes() for p in KOKR_DIR.iterdir() if p.is_file()}
    assert sorted(packed) == sorted(current), "payload 의 파일 목록이 koKR 과 다르다"
    stale = [name for name in current if packed[name] != current[name]]
    assert stale == [], f"payload 가 낡았다: {stale}"


def test_build_voice_payload_keeps_subfolders(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """한국어 음성 팩(Yuna)은 `Yuna/directions/...`, `Yuna/numbers/...` 항목으로 묶는다(2026-11-07)."""
    import zipfile

    from tools.installer_loc import build_voice_payload

    pack = tmp_path / "Yuna"
    (pack / "directions").mkdir(parents=True)
    (pack / "numbers").mkdir()
    (pack / "directions" / "east.mp3").write_bytes(b"e")
    (pack / "numbers" / "1.mp3").write_bytes(b"1")
    a, b = tmp_path / "a.zip", tmp_path / "b.zip"
    build_voice_payload(pack, a)
    build_voice_payload(pack, b)
    assert a.read_bytes() == b.read_bytes()
    with zipfile.ZipFile(a) as z:
        assert sorted(z.namelist()) == ["Yuna/directions/east.mp3", "Yuna/numbers/1.mp3"]


def test_installer_voice_payload_matches_current_pack() -> None:
    """설치 프로그램에 넣은 음성 payload 가 assets/voice/Yuna 와 같아야 한다.

    다르면: uv run python -m tools.installer_loc payload 후 설치 프로그램을 다시 빌드한다.
    """
    import zipfile

    from tools.installer_loc import VOICE_PACK, VOICE_PAYLOAD

    with zipfile.ZipFile(VOICE_PAYLOAD) as z:
        packed = {n: z.read(n) for n in z.namelist()}
    current = {
        f"Yuna/{p.relative_to(VOICE_PACK).as_posix()}": p.read_bytes() for p in VOICE_PACK.rglob("*.mp3")
    }
    assert len(current) == 108
    assert packed == current, "음성 payload 가 낡았다"

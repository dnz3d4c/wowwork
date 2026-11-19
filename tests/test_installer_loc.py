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


def test_logintool_entries_take_runtime_files_but_not_user_settings(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """로그인 툴 한국어판(2026-11-08): 설치 프로그램이 원본 4.1 뒤에 덮어쓸 파일.
    범위는 CLAUDE.md 테스트 폴더 복사 범위와 같다. data/settings.ini 는 사용자 설정이라 넣지 않는다."""
    from tools.installer_loc import logintool_entries

    tool, helper = tmp_path / "logintool", tmp_path / "bin"
    for rel in [
        "v2/START.ahk",
        "v2/includes/forever.ahk",
        "data/data.ini",
        "data/settings.ini",
        "data/localization/koKR.txt",
        "CHANGELOG.md",
        "helper/SkuLoginSense/OcrRunner.cs",
    ]:
        (tool / rel).parent.mkdir(parents=True, exist_ok=True)
        (tool / rel).write_bytes(rel.encode())
    helper.mkdir()
    for name in ["SkuLoginSense.exe", "SkuLoginSense.exe.config", "SkuLoginSense.pdb"]:
        (helper / name).write_bytes(name.encode())
    entries = logintool_entries(tool, helper)
    assert sorted(entries) == [
        "data/data.ini",
        "data/localization/koKR.txt",
        "helper/SkuLoginSense.exe",
        "helper/SkuLoginSense.exe.config",
        "v2/START.ahk",
        "v2/includes/forever.ahk",
    ]
    assert entries["v2/includes/forever.ahk"] == b"v2/includes/forever.ahk"


def test_installer_logintool_payload_matches_ko_checkout() -> None:
    """설치 프로그램에 넣은 로그인 툴 payload 가 Sku-WoW-Addon-TBC ko checkout 과 같아야 한다.

    다르면: uv run python -m tools.installer_loc payload 후 설치 프로그램을 다시 빌드한다.
    도우미 exe 는 빌드할 때마다 바이트가 달라서 있는지만 본다.
    """
    import zipfile

    from tools.installer_loc import LOGINTOOL_DIR, LOGINTOOL_PAYLOAD, logintool_entries

    with zipfile.ZipFile(LOGINTOOL_PAYLOAD) as z:
        packed = {n: z.read(n) for n in z.namelist()}
    current = logintool_entries(LOGINTOOL_DIR, None)
    helper = {"helper/SkuLoginSense.exe", "helper/SkuLoginSense.exe.config"}
    assert helper <= set(packed)
    # ko 에서 지운 파일이 payload 에 남아 있으면 설치 때 다시 생긴다(codex 2026-11-08).
    assert sorted(set(packed) - helper - set(current)) == [], "ko 에 없는 파일이 payload 에 남아 있다"
    stale = sorted(k for k in current if packed.get(k) != current[k])
    assert stale == [], f"로그인 툴 payload 가 낡았다: {stale}"


SIGN_SCRIPT = "param()\r\n$PinnedPeHashes = @{\r\n\t'AAAA' = 'engine'\r\n}\r\n$CertSubject = 'x'\r\n"


def test_pin_sign_script_adds_the_proxy_pin_and_keeps_the_rest() -> None:
    from tools.installer_loc import SR_PIN_LABEL, pin_sign_script

    out = pin_sign_script(SIGN_SCRIPT, "B" * 64)
    assert f"\t'{'B' * 64}' = '{SR_PIN_LABEL}'\r\n" in out
    assert out.index("$PinnedPeHashes = @{") < out.index("B" * 64) < out.index("'AAAA' = 'engine'")
    assert out.replace(out[out.index("@{") + 2 : out.index("\t'AAAA'")], "\r\n") == SIGN_SCRIPT


def test_installer_sense_reader_payload_matches_bridge() -> None:
    """설치 프로그램에 넣은 센스 리더 payload 가 프록시 소스와 원본 브리지 서명 스크립트에 맞아야 한다.

    다르면: uv run python -m tools.installer_loc payload 후 설치 프로그램을 다시 빌드한다.
    DLL 은 빌드마다 바이트가 달라서, 표지가 있고 서명 스크립트가 그 DLL 의 고정 해시를 담는지 본다.
    """
    import tempfile
    import zipfile
    from pathlib import Path

    from tools.installer_loc import BRIDGE_PAYLOAD, SR_PAYLOAD, pe_hash, pin_sign_script

    with zipfile.ZipFile(SR_PAYLOAD) as z:
        assert sorted(z.namelist()) == ["nvdaControllerClient.dll", "sign.ps1"]
        dll, script = z.read("nvdaControllerClient.dll"), z.read("sign.ps1")
    with zipfile.ZipFile(BRIDGE_PAYLOAD) as z:
        sku_script = z.read("sku-nvda-voice-sign.ps1")
    assert b"WowVisionKoreanSenseReaderProxy/" in dll
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "p.dll").write_bytes(dll)
        (Path(tmp) / "s.ps1").write_bytes(sku_script)
        expected = pin_sign_script(
            sku_script.decode("utf-8-sig"), pe_hash(Path(tmp) / "p.dll", Path(tmp) / "s.ps1")
        )
    assert script.decode("utf-8-sig") == expected


def test_sense_reader_submodule_problem_rejects_anything_but_the_recorded_clean_commit() -> None:
    """payload 는 installer 가 기록한 korean 커밋 그대로일 때만 만든다."""
    from tools.installer_loc import sense_reader_submodule_problem as problem

    ok = " 672edc2e4f63066af838df94e0d2e567dfb09d4d korean (heads/main)"
    assert problem(ok, "") is None
    assert "초기화" in problem("-672edc2e4f63066af838df94e0d2e567dfb09d4d korean", "")  # type: ignore[operator]
    assert "기록된 커밋" in problem("+1111111e4f63066af838df94e0d2e567dfb09d4d korean (heads/main)", "")  # type: ignore[operator]
    assert "충돌" in problem("U672edc2e4f63066af838df94e0d2e567dfb09d4d korean", "")  # type: ignore[operator]
    assert "koSenseReader.c" in problem(ok, " M sense-reader-bridge/koSenseReader.c\n")  # type: ignore[operator]
    assert "출력이 없다" in problem("", "")  # type: ignore[operator]

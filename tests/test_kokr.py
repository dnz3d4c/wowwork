"""koKR 번역 파일이 enUS 원문과 어긋나지 않는지 검사한다."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from tools.locale_lib import KOKR_DIR, format_specs, parse_locale_file, upstream_locale_dir

ENUS_DIR = upstream_locale_dir() / "enUS"
ENUS_FILES = sorted(p.name for p in ENUS_DIR.glob("*.lua"))
HEADER = 'local L = LibStub("AceLocale-3.0"):NewLocale("WowVision", "koKR")\nif not L then return end\n'


def test_upstream_found() -> None:
    assert ENUS_FILES, f"enUS 원문을 찾지 못했다: {ENUS_DIR}"


@pytest.mark.parametrize("name", ENUS_FILES)
def test_file_exists_with_header(name: str) -> None:
    path = KOKR_DIR / name
    assert path.exists(), f"koKR/{name} 없음"
    assert path.read_text(encoding="utf-8").startswith(HEADER)


@pytest.mark.parametrize("name", ENUS_FILES)
def test_keys_match(name: str) -> None:
    en = parse_locale_file(ENUS_DIR / name)
    ko = parse_locale_file(KOKR_DIR / name)
    assert sorted(set(en) - set(ko)) == [], "번역 누락"
    assert sorted(set(ko) - set(en)) == [], "원문에 없는 키"


@pytest.mark.parametrize("name", ENUS_FILES)
def test_values_valid(name: str) -> None:
    en = parse_locale_file(ENUS_DIR / name)
    ko = parse_locale_file(KOKR_DIR / name)
    for key, ko_val in ko.items():
        assert ko_val.strip(), f"빈 번역: {key!r}"
        assert format_specs(ko_val) == format_specs(en[key]), f"서식 지정자 불일치: {key!r} → {ko_val!r}"


def test_same_key_same_translation() -> None:
    """AceLocale 은 같은 키를 나중 파일 값으로 덮어쓰므로, 파일 간 번역이 다르면 한쪽이 조용히 사라진다."""
    seen: dict[str, tuple[str, str]] = {}
    conflicts = []
    for name in ENUS_FILES:
        for key, val in parse_locale_file(KOKR_DIR / name).items():
            if key in seen and seen[key][1] != val:
                conflicts.append(f"{key!r}: {seen[key][0]}={seen[key][1]!r} / {name}={val!r}")
            seen.setdefault(key, (name, val))
    assert conflicts == []


def test_modules_xml_lists_all_files() -> None:
    xml = (KOKR_DIR / "modules.xml").read_text(encoding="utf-8")
    for name in ENUS_FILES:
        assert f'<Script file="{name}" />' in xml


@pytest.mark.skipif(shutil.which("luajit") is None, reason="luajit 없음")
@pytest.mark.parametrize("name", ENUS_FILES)
def test_lua_syntax(name: str, tmp_path: Path) -> None:
    out = tmp_path / "out.bc"
    result = subprocess.run(
        ["luajit", "-b", str(KOKR_DIR / name), str(out)], capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, result.stderr

"""install.py: 게임 AddOns 폴더의 WowVision 에 koKR 을 넣는 로직."""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.install import INCLUDE_LINE, add_include, install

UPSTREAM_XML = """<Ui xmlns="http://www.blizzard.com/wow/ui/">

  <Include file="enUS/modules.xml" />
  <Include file="deDE/modules.xml" />
  <Include file="frFR/modules.xml" />

</Ui>"""


def test_add_include_after_last_include() -> None:
    out = add_include(UPSTREAM_XML)
    assert out.count(INCLUDE_LINE) == 1
    assert out.index("frFR/modules.xml") < out.index(INCLUDE_LINE) < out.index("</Ui>")


def test_add_include_idempotent() -> None:
    once = add_include(UPSTREAM_XML)
    assert add_include(once) == once


def test_add_include_rejects_unknown_format() -> None:
    with pytest.raises(ValueError):
        add_include("<Ui></Ui>")


def _fake_addon(root: Path) -> Path:
    locale = root / "WowVision" / "locale"
    (locale / "enUS").mkdir(parents=True)
    (locale / "modules.xml").write_text(UPSTREAM_XML, encoding="utf-8")
    return root


def _fake_kokr(root: Path) -> Path:
    src = root / "koKR"
    src.mkdir()
    (src / "modules.xml").write_text("<Ui />", encoding="utf-8")
    (src / "ui.lua").write_text("-- ko", encoding="utf-8")
    return src


def test_install_copies_and_patches(tmp_path: Path) -> None:
    addons = _fake_addon(tmp_path / "AddOns")
    src = _fake_kokr(tmp_path)
    (addons / "WowVision" / "locale" / "koKR").mkdir()
    (addons / "WowVision" / "locale" / "koKR" / "stale.lua").write_text("old", encoding="utf-8")

    install(addons, src)

    dest = addons / "WowVision" / "locale" / "koKR"
    assert sorted(p.name for p in dest.iterdir()) == ["modules.xml", "ui.lua"]
    xml = (addons / "WowVision" / "locale" / "modules.xml").read_text(encoding="utf-8")
    assert xml.count(INCLUDE_LINE) == 1


def test_install_requires_wowvision(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        install(tmp_path, _fake_kokr(tmp_path))

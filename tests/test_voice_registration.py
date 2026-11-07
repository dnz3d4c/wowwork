"""설치 프로그램이 audio/voice.lua 에 붙이는 Yuna 등록 줄이 Lua 로 실행되는지 검사한다(2026-11-07).

등록 줄은 KoreanVoice.cs 에서 읽고, 원본 voice.lua 뒤에 붙여 luajit 으로 실행한다.
"""

import re
import shutil
import subprocess

import pytest

from tools.locale_lib import KO_WORK_ROOT, WOWVISION_DIR

KOREAN_VOICE_CS = KO_WORK_ROOT / "wowvision-installer" / "WowVisionInstaller" / "KoreanVoice.cs"


def register_line() -> str:
    m = re.search(r'RegisterLine\s*=\s*"((?:[^"\\]|\\.)*)";', KOREAN_VOICE_CS.read_text(encoding="utf-8"))
    assert m, "KoreanVoice.cs 에서 RegisterLine 을 찾지 못했다"
    return m.group(1).replace('\\"', '"')


@pytest.mark.skipif(shutil.which("luajit") is None, reason="luajit 없음")
def test_voice_lua_with_yuna_runs_and_registers_three_packs(tmp_path) -> None:  # type: ignore[no-untyped-def]
    lua = (WOWVISION_DIR / "audio" / "voice.lua").read_text(encoding="utf-8")
    if not lua.endswith("\n"):
        lua += "\n"
    stub = (
        "local seen = {}\n"
        "WowVision = { audio = { registerVoicePack = function(self, info) seen[#seen + 1] = info end } }\n"
        + lua
        + register_line()
        + "\nfor _, p in ipairs(seen) do print(p.key .. '|' .. p.label .. '|' .. p.filePath) end\n"
    )
    script = tmp_path / "voice_check.lua"
    script.write_text(stub, encoding="utf-8")
    out = subprocess.run(["luajit", str(script)], capture_output=True, text=True, check=True).stdout.split()
    assert [line.split("|")[0] for line in out] == ["Matthew", "Joanna", "Yuna"]
    assert out[-1] == "Yuna|Yuna|Interface/AddOns/WowVision/audio/voice/Yuna"

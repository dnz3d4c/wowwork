"""한국어 음성 팩을 만든다. 원본 음성 팩(Matthew, Joanna)과 같은 파일을 한국어 TTS로 녹음한다.

사용: uv run python -m tools.voice_pack build [--voice "<SAPI 음성 이름>"] [--out <폴더>]

파일 목록은 원본 core/audio/AudioPack.lua 의 VoicePack:setup 에서 뽑는다(방향 8개, 숫자 1~100).
방향 낱말은 koKR 값(TTS 출력이 말하는 것과 같은 말), 숫자는 한글 수사로 적어 TTS가 읽는 방식에 맡기지 않는다.
형식은 원본 팩과 같은 mp3 16kHz 모노 128kbps이고, 앞뒤 무음을 잘라낸다.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from tools.locale_lib import KOKR_DIR, REPO_ROOT, WOWVISION_DIR, parse_locale_file

AUDIO_PACK_LUA = WOWVISION_DIR / "core" / "audio" / "AudioPack.lua"
# SAPI COM 의 음성 설명(GetDescription). 같은 PC의 "Code Factory Vocalizer Yuna (한국어) - Embedded High"는
# NVDA 밖에서 녹음이 잘려 나와서 쓰지 않는다(2026-11-07 실측, too_short 가 잡는다).
DEFAULT_VOICE = "Vocalizer Expressive Yuna Harpo 22kHz"
DEFAULT_RATE = 0  # SAPI 속도 -10~10, 0이 보통
DEFAULT_OUT = REPO_ROOT / "assets" / "voice" / "Yuna"

_DIGITS = ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]


def hangul_number(n: int) -> str:
    """1~100 을 한글 수사(한자어)로 적는다. 10은 "일십"이 아니라 "십"."""
    if not 1 <= n <= 100:
        raise ValueError(n)
    if n == 100:
        return "백"
    tens, ones = divmod(n, 10)
    head = "" if tens == 0 else ("십" if tens == 1 else _DIGITS[tens] + "십")
    return head + _DIGITS[ones]


def pack_files(lua: str) -> list[str]:
    """VoicePack:setup 이 등록하는 파일을 '하위폴더/파일' 로 돌려준다."""
    files: list[str] = []
    var_to_dir = dict(re.findall(r'local\s+(\w+)\s*=\s*root:addSubdirectory\(\{\s*key\s*=\s*"(\w+)"', lua))
    for var, body in re.findall(r"(\w+):addFiles\(\{(.*?)\}\)", lua, re.DOTALL):
        files += [f"{var_to_dir[var]}/{name}" for name in re.findall(r'"([^"]+)"', body)]
    for start, end, var, suffix in re.findall(
        r"for\s+i\s*=\s*(\d+)\s*,\s*(\d+)\s+do\s+(\w+):addFile\(i\s*\.\.\s*\"([^\"]+)\"\)", lua
    ):
        files += [f"{var_to_dir[var]}/{i}{suffix}" for i in range(int(start), int(end) + 1)]
    return files


def text_for(rel: str, directions: dict[str, str]) -> str:
    folder, name = rel.split("/", 1)
    stem = name.rsplit(".", 1)[0]
    if folder == "directions":
        return directions[stem]
    if folder == "numbers":
        return hangul_number(int(stem))
    raise ValueError(f"모르는 음성 팩 폴더: {rel}")


def pack_entries() -> list[tuple[str, str]]:
    directions = parse_locale_file(KOKR_DIR / "navigation.lua")
    files = pack_files(AUDIO_PACK_LUA.read_text(encoding="utf-8"))
    return [(rel, text_for(rel, directions)) for rel in files]


# SAPI5 COM(SAPI.SpVoice)으로 녹음한다. .NET System.Speech 는 Vocalizer Expressive 음성을 SelectVoice 하지 못했다
# (2026-11-07 실측). 음성은 GetDescription() 이 정확히 같은 것을 고른다.
_PS = r"""
$ErrorActionPreference = 'Stop'
$v = New-Object -ComObject SAPI.SpVoice
$token = $null
foreach ($t in $v.GetVoices()) { if ($t.GetDescription() -eq $args[0]) { $token = $t } }
if ($token -eq $null) { throw ("SAPI voice not found: " + $args[0]) }
$v.Voice = $token
# 속도는 PC의 SAPI 기본값을 따르지 않고 지정한다.
$v.Rate = [int]$args[2]
foreach ($line in [IO.File]::ReadAllLines($args[1], [Text.Encoding]::UTF8)) {
    $parts = $line.Split("`t")
    $fs = New-Object -ComObject SAPI.SpFileStream
    $fmt = New-Object -ComObject SAPI.SpAudioFormat
    $fmt.Type = 22  # SAFT22kHz16BitMono
    $fs.Format = $fmt
    $fs.Open($parts[0], 3, $false)
    $v.AudioOutputStream = $fs
    [void]$v.Speak($parts[1])
    $fs.Close()
}
"""

# 음절당 이보다 짧으면 녹음이 잘린 것으로 본다. 정상 녹음은 음절당 0.12초 이상이었고,
# Code Factory Yuna 가 NVDA 밖에서 잘라 낸 녹음은 약 0.055초였다(2026-11-07 실측).
MIN_SECONDS_PER_SYLLABLE = 0.09


def too_short(durations: dict[str, float], texts: dict[str, str]) -> list[str]:
    return [rel for rel, sec in durations.items() if sec < MIN_SECONDS_PER_SYLLABLE * len(texts[rel])]


def duration(path: Path) -> float:
    """끝까지 디코딩해서 잰 길이(초). mp3 헤더의 추정값은 쓰지 않는다."""
    err = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-f", "null", "-"],
        capture_output=True,
        text=True,
        check=False,
    ).stderr
    h, m, s = re.findall(r"time=(\d+):(\d+):([\d.]+)", err)[-1]
    return int(h) * 3600 + int(m) * 60 + float(s)


# 앞 무음을 자르고, 뒤집어서 다시 잘라 뒤 무음도 없앤다.
_TRIM = "silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse"


def build(voice: str, out: Path, rate: int = DEFAULT_RATE) -> int:
    entries = pack_entries()
    with tempfile.TemporaryDirectory() as tmp_name:
        tmp = Path(tmp_name)
        script = tmp / "synth.ps1"
        script.write_text(_PS, encoding="utf-8-sig")
        listing = tmp / "list.tsv"
        wavs = {rel: tmp / (rel.replace("/", "_") + ".wav") for rel, _ in entries}
        listing.write_text("\n".join(f"{wavs[rel]}\t{text}" for rel, text in entries), encoding="utf-8")
        subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(script),
                voice,
                str(listing),
                str(rate),
            ],
            check=True,
        )
        if out.exists():
            shutil.rmtree(out)
        for rel, _ in entries:
            target = out / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                [
                    "ffmpeg",
                    "-v",
                    "error",
                    "-y",
                    "-i",
                    str(wavs[rel]),
                    "-af",
                    _TRIM,
                    "-ar",
                    "16000",
                    "-ac",
                    "1",
                    "-c:a",
                    "libmp3lame",
                    "-b:a",
                    "128k",
                    str(target),
                ],
                check=True,
            )
    texts = dict(entries)
    short = too_short({rel: duration(out / rel) for rel in texts}, texts)
    if short:
        raise SystemExit(
            f"녹음이 잘린 것으로 보이는 파일 {len(short)}개(음절당 {MIN_SECONDS_PER_SYLLABLE}초 미만): {short[:10]}"
        )
    return len(entries)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["build"])
    ap.add_argument("--voice", default=DEFAULT_VOICE)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--rate", type=int, default=DEFAULT_RATE)
    args = ap.parse_args()
    n = build(args.voice, args.out, args.rate)
    print(f"{n}개 파일 -> {args.out}")


if __name__ == "__main__":
    main()

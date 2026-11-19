"""한국어 음성 팩(Yuna)의 파일 목록과 낭독 문구를 검사한다.

2026-11-07: 나침반 방향("east")과 숫자 알림이 영어 녹음(Matthew, Joanna)으로만 나왔다.
원본 음성 팩이 담는 파일은 core/audio/AudioPack.lua 의 VoicePack:setup 이 정한다.
목록을 손으로 적지 않고 그 파일에서 뽑으므로, 원본에 파일이 늘면 이 검사가 실패한다.
"""

from tools.voice_pack import AUDIO_PACK_LUA, hangul_number, pack_entries, pack_files


def test_hangul_number_basic() -> None:
    assert [hangul_number(n) for n in (1, 2, 10, 11, 20, 21, 99, 100)] == [
        "일",
        "이",
        "십",
        "십일",
        "이십",
        "이십일",
        "구십구",
        "백",
    ]


def test_pack_files_follow_upstream_voice_pack() -> None:
    files = pack_files(AUDIO_PACK_LUA.read_text(encoding="utf-8"))
    assert len(files) == 108
    assert "directions/east.mp3" in files
    assert "numbers/1.mp3" in files and "numbers/100.mp3" in files


def test_pack_files_parse_setup_shape() -> None:
    lua = """
    local directions = root:addSubdirectory({ key = "directions", label = "directions" })
    directions:addFiles({ "north.mp3", "east.mp3" })
    local numbers = root:addSubdirectory({ key = "numbers", label = "numbers" })
    for i = 1, 3 do
        numbers:addFile(i .. ".mp3")
    end
    """
    assert pack_files(lua) == [
        "directions/north.mp3",
        "directions/east.mp3",
        "numbers/1.mp3",
        "numbers/2.mp3",
        "numbers/3.mp3",
    ]


def test_entries_use_kokr_direction_words() -> None:
    entries = dict(pack_entries())
    assert entries["directions/east.mp3"] == "동쪽"
    assert entries["directions/northwest.mp3"] == "북서쪽"
    assert entries["numbers/21.mp3"] == "이십일"
    assert all(text for text in entries.values())


def test_too_short_flags_truncated_recordings() -> None:
    """2026-11-07: Code Factory Yuna 는 NVDA 밖에서 "동쪽"을 0.11초로 잘라 녹음했다(음절당 약 0.055초)."""
    from tools.voice_pack import too_short

    durations = {"directions/east.mp3": 0.11, "numbers/2.mp3": 0.16, "numbers/77.mp3": 0.36}
    texts = {"directions/east.mp3": "동쪽", "numbers/2.mp3": "이", "numbers/77.mp3": "칠십칠"}
    assert too_short(durations, texts) == ["directions/east.mp3"]


def test_too_loud_flags_peaks() -> None:
    """2026-11-08: SAPI 볼륨 100 녹음은 wav 단계에서 이미 0 dBFS로 잘렸다(77개 파일 피크 -0.1 dB 이상)."""
    from tools.voice_pack import MAX_PEAK_DB, too_loud

    assert MAX_PEAK_DB <= -1.0
    peaks = {"numbers/1.mp3": 0.0, "numbers/2.mp3": -0.5, "numbers/3.mp3": -9.3}
    assert too_loud(peaks) == ["numbers/1.mp3", "numbers/2.mp3"]


def test_volume_out_of_range_is_rejected() -> None:
    """codex 지적(2026-11-08): SAPI 볼륨은 0~100. 범위 밖 값은 녹음 전에 막는다."""
    import argparse

    import pytest

    from tools.voice_pack import sapi_volume

    assert sapi_volume("60") == 60
    for bad in ("-1", "101", "abc"):
        with pytest.raises(argparse.ArgumentTypeError):
            sapi_volume(bad)


def test_ffmpeg_output_without_value_names_the_file() -> None:
    """codex 지적(2026-11-08): ffmpeg 출력에서 값을 못 찾으면 IndexError 대신 파일 이름을 담은 오류로 끝낸다."""
    from pathlib import Path

    import pytest

    from tools.voice_pack import last_match

    assert last_match(r"max_volume: (-?[\d.]+) dB", "max_volume: -9.5 dB", Path("a.mp3")) == ("-9.5",)
    with pytest.raises(SystemExit, match="a.mp3"):
        last_match(r"max_volume: (-?[\d.]+) dB", "Invalid data found", Path("a.mp3"))

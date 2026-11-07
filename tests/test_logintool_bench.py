"""로그인 툴 캐릭터 선택 화면 OCR 측정 도구를 검사한다.

2026-11-07: 사용자 캐릭터 하나만으로는 이름 인식률을 알 수 없어서, 게임 글꼴로 그린 이름 묶음을
읽혀 정답률을 잰다. 묶음이 한글 상용 음절을 빠짐없이 덮는지와 평가 지표 계산을 여기서 확인한다.
"""

import pytest

from tools.logintool_bench.corpus import COMMON, GS_KO, build_names, lua_data
from tools.logintool_bench.evaluate import cer, has_level_word, match_lines, norm, parse_truth

# word 종류는 cache/gs_koKR.csv(git 제외)에서 뽑는다. 캐시가 없는 체크아웃에서는 건너뛴다.
needs_cache = pytest.mark.skipif(not GS_KO.exists(), reason="cache/gs_koKR.csv 없음")


def test_common_syllables_are_ks_x_1001() -> None:
    assert len(COMMON) == 2350
    assert "가" in COMMON and "힐" in COMMON and "똠" not in COMMON


def test_names_cover_every_common_syllable() -> None:
    names = build_names(seed=1)
    used = {ch for n in names for ch in n["name"]}
    assert COMMON <= used


@needs_cache
def test_names_have_valid_lengths_and_kinds() -> None:
    names = build_names(seed=1)
    for n in names:
        if n["kind"] == "latin":
            assert n["name"].isascii() and 3 <= len(n["name"]) <= 12
        else:
            assert 2 <= len(n["name"]) <= 6, n
            assert all("가" <= ch <= "힣" for ch in n["name"]), n
    kinds = {n["kind"] for n in names}
    assert kinds == {"coverage", "rare", "word", "complex", "repeat", "latin"}
    assert len({n["name"] for n in names}) == len(names)


def test_names_are_deterministic() -> None:
    assert build_names(seed=7) == build_names(seed=7)


def test_lua_data_escapes_and_lists_every_name() -> None:
    names = [{"name": "가나", "kind": "coverage"}, {"name": 'A"b\\c', "kind": "latin"}]
    text = lua_data(names)
    assert '{"가나","coverage"}' in text
    assert r'{"A\"b\\c","latin"}' in text


def test_norm_matches_tool_comparison() -> None:
    # forever.ahk FvNorm: case-folded, only letters and digits kept
    assert norm("〈뒤로-") == "뒤로"
    assert norm("1 레벨 성기사") == "1레벨성기사"
    assert norm("Log In") == "login"


def test_cer() -> None:
    assert cer("까다로운힐링", "까다로운힐링") == 0
    assert cer("까다로운힐링", "까다로운일렁") == 2 / 6
    assert cer("가나", "") == 1


def test_has_level_word_uses_korean() -> None:
    assert has_level_word("1 레벨 성기사")
    assert not has_level_word("던 모로")


def test_parse_truth_reads_saved_variables() -> None:
    sv = (
        'LoginToolOcrBenchDB = {\n["screen"] = "1920x1080",\n["items"] = {\n'
        '"1\\t1.000\\tname\\tcoverage\\t까다로운힐링\\t100\\t200\\t370\\t222",\n'
        '"1\\t1.000\\tinfo\\t전사\\t60 레벨 전사\\t100\\t226\\t370\\t244",\n},\n}\n'
    )
    items = parse_truth(sv)
    assert items[0] == {
        "page": 1, "k": 1.0, "role": "name", "tag": "coverage", "text": "까다로운힐링",
        "l": 100, "t": 200, "r": 370, "b": 222,
    }
    assert items[1]["role"] == "info"


def test_match_lines_joins_split_lines_in_box() -> None:
    item = {"l": 100, "t": 200, "r": 370, "b": 222}
    lines = [
        {"text": "힐링", "x": 160, "y": 201, "w": 40, "h": 20},
        {"text": "까다로운", "x": 102, "y": 202, "w": 50, "h": 19},
        {"text": "다른 줄", "x": 102, "y": 230, "w": 50, "h": 18},
    ]
    assert match_lines(item, lines) == "까다로운 힐링"


def test_pick_pages_keeps_first_capture_per_marker() -> None:
    from tools.logintool_bench.evaluate import pick_pages

    marks = [("c_00001", "PAGE 1"), ("c_00002", "PAGE 1"), ("c_00003", "PAGE 2"),
             ("c_00004", ""), ("c_00005", "PAGE 4"), ("c_00006", "DONE"), ("c_00007", "PAGE 1O")]
    assert pick_pages(marks) == {1: "c_00001", 2: "c_00003", 4: "c_00005"}

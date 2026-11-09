from __future__ import annotations

from pathlib import Path

import pytest

from tools.manual import check, slug, structure, term_sheet

EN = """# Using the Interface

Press **Enter** to click. See [Alerts](alerts.md#picking-a-sound) and [below](#letter-navigation-in-menus).

## Letter Navigation in Menus

| Key | What |
|-----|------|
| `F10` | Navigation |

```
/wv
```
"""

KO = """<!-- source: docs/src/user/en/basics/interface.md @ abc1234 -->
# 인터페이스 사용

**Enter**를 눌러 클릭합니다. [알림](alerts.md#소리-고르기)과 [아래](#메뉴에서-글자로-이동)를 보십시오.

## 메뉴에서 글자로 이동

| 키 | 기능 |
|-----|------|
| `F10` | 길 안내 |

```
/wv
```
"""

ALERTS_KO = "# 알림\n\n## 소리 고르기\n"


def test_slug_matches_mdbook_rules() -> None:
    assert slug("Letter Navigation in Menus") == "letter-navigation-in-menus"
    assert slug("메뉴에서 글자로 이동") == "메뉴에서-글자로-이동"
    assert slug("What `F10` does, (really)?") == "what-f10-does-really"


def test_structure_extracts_comparable_parts() -> None:
    s = structure(EN)
    assert s["headings"] == [1, 2]
    assert s["tables"] == [3]
    assert s["links"] == ["alerts.md", ""]
    assert s["code"] == ["`F10`"]
    assert s["blocks"] == ["```\n/wv\n```"]
    assert s["columns"] == [2]
    assert s["lists"] == [0]


def test_check_reports_list_items_and_table_columns(tmp_path: Path) -> None:
    """translation-guide.md `### 문체`가 약속한 목록 항목 수와 표 열 수도 대조한다."""
    en = "# A\n\n- one\n- two\n  1. nested\n\n| K | V | N |\n|---|---|---|\n| a | b | c |\n"
    good = "<!-- source: docs/src/user/en/a.md @ abc1234 -->\n# 가\n\n- 하나\n- 둘\n  1. 안쪽\n\n| 키 | 값 | 비고 |\n|---|---|---|\n| a | b | c |\n"
    ko = tmp_path / "a.md"
    assert check(en, good, ko, terms=[]) == []
    merged = (
        good.replace("- 하나\n- 둘", "- 하나와 둘")
        .replace("| 키 | 값 | 비고 |", "| 키 | 값 |")
        .replace("|---|---|---|", "|---|---|")
        .replace("| a | b | c |", "| a | b |")
    )
    problems = "\n".join(check(en, merged, ko, terms=[]))
    assert "목록 항목" in problems
    assert "표 열" in problems


def test_check_passes_good_translation(tmp_path: Path) -> None:
    (tmp_path / "basics").mkdir()
    (tmp_path / "basics" / "alerts.md").write_text(ALERTS_KO, "utf-8")
    ko = tmp_path / "basics" / "interface.md"
    ko.write_text(KO, "utf-8")
    assert check(EN, KO, ko) == []


def test_check_reports_structure_and_anchor_problems(tmp_path: Path) -> None:
    (tmp_path / "alerts.md").write_text(ALERTS_KO, "utf-8")
    bad = (
        KO.replace("## 메뉴에서", "### 메뉴에서")
        .replace("`F10`", "F10")
        .replace("#소리-고르기", "#picking-a-sound")
        .replace("<!-- source", "<!-- x")
    )
    ko = tmp_path / "interface.md"
    ko.write_text(bad, "utf-8")
    problems = "\n".join(check(EN, bad, ko))
    assert "source" in problems
    assert "제목" in problems
    assert "인라인 코드" in problems
    assert "alerts.md#picking-a-sound" in problems


def test_term_sheet_finds_ui_strings_with_korean_values() -> None:
    en_values = {"Letter Navigation in Menus": "메뉴에서 글자로 이동", "Navigation": "길 안내", "Off": "끄기"}
    sheet = term_sheet(EN, en_values)
    assert {"en": "Letter Navigation in Menus", "ko": "메뉴에서 글자로 이동"} in sheet
    assert {"en": "Navigation", "ko": "길 안내"} in sheet
    assert all(t["en"] != "Off" for t in sheet)


def test_check_rejects_haeyo_style(tmp_path: Path) -> None:
    ko = tmp_path / "interface.md"
    bad = KO.replace("보십시오.", "보세요.")
    ko.write_text(bad, "utf-8")
    (tmp_path / "alerts.md").write_text(ALERTS_KO, "utf-8")
    problems = "\n".join(check(EN, bad, ko))
    assert "해요체" in problems and "보세요." in problems


def test_check_applies_glossary_per_file(tmp_path: Path) -> None:
    """확정 용어집은 설명서에도 적용한다(파일 단위: 원문에 용어가 있으면 번역문에 정해진 번역이 있어야 한다).
    2026-11-09 실측: reference/glossary.md 가 network 를 "연결망"으로 옮겼다(다른 곳 48곳은 "네트워크")."""
    from tools.glossary import Term

    terms = [
        Term("network", ("네트워크",), frozenset(), ""),
        Term("focus", ("주시 대상",), frozenset({"manual::*"}), ""),
    ]
    ko = tmp_path / "p.md"
    en = "# Map data\n\nThe network of waypoints. Keyboard focus moves. `network`\n"
    bad = "<!-- source: docs/src/user/en/p.md @ abc1234 -->\n# 지도 데이터\n\n경유지 연결망. 초점이 움직입니다. `network`\n"
    ko.write_text(bad, "utf-8")
    problems = check(en, bad, ko, terms)
    assert len(problems) == 1 and "network" in problems[0] and "네트워크" in problems[0]
    good = bad.replace("연결망", "네트워크")
    assert check(en, good, ko, terms) == []


def test_check_rejects_bakkuda_outside_quotes(tmp_path: Path) -> None:
    """2026-11-09 사용자 결정: 설명서 본문은 바꾸다·바뀌다 대신 변경하다·변경되다(전역 낱말 표).
    화면 문구 인용("바꾸기"는 koKR Replace 값)과 인라인 코드는 실물 그대로라 검사하지 않는다."""
    ko = tmp_path / "interface.md"
    (tmp_path / "alerts.md").write_text(ALERTS_KO, "utf-8")
    bad = KO.replace("클릭합니다.", '클릭합니다. 설정을 바꿉니다. 값이 바뀌면 "바꾸기"를 고릅니다.')
    ko.write_text(bad, "utf-8")
    problems = "\n".join(check(EN, bad, ko))
    assert "바꿉니다" in problems and "바뀌면" in problems and "바꾸기" not in problems
    good = KO.replace("클릭합니다.", '클릭합니다. 설정을 변경합니다. 값이 변경되면 "바꾸기"를 고릅니다.')
    assert check(EN, good, ko) == []


def test_check_allows_bakkuda_in_glossary_names(tmp_path: Path) -> None:
    """2026-11-09 회귀 확인(두 회사 치명): 게임 탭 이름 "무엇이 바뀌었나요?"를 "무엇이 변경되었나요?"로
    바꿔 화면 이름과 달라졌다. 용어집에 오른 이름은 따옴표가 없어도 실물 그대로 둔다."""
    from tools.glossary import Term

    terms = [Term("What Has Changed", ("무엇이 바뀌었나요?",), frozenset(), "")]
    ko = tmp_path / "p.md"
    en = "# Tabs\n\nThe What Has Changed tab.\n"
    text = "<!-- source: docs/src/user/en/p.md @ abc1234 -->\n# 탭\n\n무엇이 바뀌었나요? 탭.\n"
    ko.write_text(text, "utf-8")
    assert check(en, text, ko, terms) == []
    renamed = text.replace("바뀌었나요", "변경되었나요")
    assert "What Has Changed" in "\n".join(check(en, renamed, ko, terms))


def test_translated_manual_passes_check() -> None:
    """0단계 기계 검사: 번역된 설명서 전체가 구조·앵커·해요체·용어집 검사를 통과한다.
    그전에는 `tools.manual check`를 따로 실행해야 해서 `uv run pytest -q`가 설명서를 보지 않았다."""
    from tools.manual import EN_ROOT, KO_ROOT

    if not KO_ROOT.exists():
        pytest.skip("한국어 설명서 없음")
    problems = {
        p.relative_to(KO_ROOT).as_posix(): check(
            (EN_ROOT / p.relative_to(KO_ROOT)).read_text(encoding="utf-8"), p.read_text(encoding="utf-8"), p
        )
        for p in sorted(KO_ROOT.rglob("*.md"))
        if (EN_ROOT / p.relative_to(KO_ROOT)).exists()
    }
    assert {k: v for k, v in problems.items() if v} == {}


def test_korean_summary_titles_match_page_headings() -> None:
    """목차(SUMMARY.md)의 한국어 항목은 그 페이지의 제목(# 줄)과 같아야 한다.

    2026-11-07: 페이지 제목을 경보→알림, 대상 지정→목표 선택, 키 바인딩 목록→단축키 목록으로 바꿨는데
    목차는 그대로 남았다. mdBook은 목차 글자를 탐색 메뉴에 쓰므로 페이지 제목과 갈라진다.
    """
    import re

    from tools.manual import KO_ROOT

    src = KO_ROOT.parents[1]
    summary = (src / "SUMMARY.md").read_text(encoding="utf-8")
    entries = re.findall(r"\[([^\]]+)\]\(\./(user/ko/[^)]+)\)", summary)
    assert entries, "목차에 한국어 항목이 없다"
    bad = []
    for title, rel in entries:
        heading = next(
            (
                ln[2:].strip()
                for ln in (src / rel).read_text(encoding="utf-8").splitlines()
                if ln.startswith("# ")
            ),
            "",
        )
        if title != heading:
            bad.append(f"{rel}: 목차 '{title}' / 제목 '{heading}'")
    assert bad == []


def test_source_diff_shows_english_changes_since_translated_commit(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """V1.0.1 재번역(2026-11-08): 파일 전체를 다시 번역하면 다듬기와 사용자 결정이 사라진다.
    번역 파일 첫 줄의 원문 커밋 이후 영어가 어떻게 바뀌었는지를 번역자와 평가자에게 준다."""
    import subprocess

    from tools.manual import source_diff

    def git(*a: str) -> str:
        return subprocess.run(
            ["git", "-C", str(tmp_path), *a], check=True, capture_output=True, text=True
        ).stdout

    en = tmp_path / "docs" / "src" / "user" / "en" / "a.md"
    en.parent.mkdir(parents=True)
    en.write_text("# Title\n\nOld line.\n", encoding="utf-8")
    git("init", "-q")
    git("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qam", "x", "--allow-empty")
    git("add", ".")
    git("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "en")
    commit = git("rev-parse", "--short", "HEAD").strip()
    ko = f"<!-- source: docs/src/user/en/a.md @ {commit} -->\n# 제목\n"
    assert source_diff(ko, "a.md", repo=tmp_path) == ""
    en.write_text("# Title\n\nNew line.\n", encoding="utf-8")
    d = source_diff(ko, "a.md", repo=tmp_path)
    assert "-Old line." in d and "+New line." in d

from __future__ import annotations

from pathlib import Path

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

**Enter**를 눌러 클릭합니다. [경보](alerts.md#소리-고르기)와 [아래](#메뉴에서-글자로-이동)를 보십시오.

## 메뉴에서 글자로 이동

| 키 | 기능 |
|-----|------|
| `F10` | 길 안내 |

```
/wv
```
"""

ALERTS_KO = "# 경보\n\n## 소리 고르기\n"


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

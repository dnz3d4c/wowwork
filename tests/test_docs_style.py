"""저장소의 한국어 문서(README, 지침, 스킬, docs)에 남기 쉬운 번역투와 군더더기를 잡는다.

번역 설명서는 tools.manual check 가 따로 검사한다. 이 검사는 사람이 직접 쓰는 저장소 문서용이다.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.manual import broken_links, doc_style_problems

ROOT = Path(__file__).resolve().parent.parent
DOCS = sorted(
    [ROOT / "README.md", ROOT / "CLAUDE.md", ROOT / "reviews" / "README.md", ROOT / "tests" / "README.md"]
    + list((ROOT / "docs").glob("*.md"))
    + list((ROOT / ".claude").rglob("*.md"))
)


def test_flags_demonstrative_and_filler_endings() -> None:
    text = "`pwsh`를 입력하면 그 폴더에서 창이 열립니다. 해당 파일을 엽니다. 버튼을 누르지 않은 것입니다. 확인하세요.\n"
    problems = "\n".join(doc_style_problems(text))
    assert "그 폴더에서" in problems
    assert "해당 파일을" in problems
    assert "것입니다" in problems
    assert "확인하세요" in problems


def test_ignores_code_quotes_and_this() -> None:
    text = '이 저장소의 `그 값`과 "그 창"은 인용입니다. 그대로 두고, 그다음 실행합니다. 이 규칙에 해당하지 않습니다. 비고: 해당 없음.\n'
    assert doc_style_problems(text) == []


def test_allows_time_and_scope_idioms() -> None:
    """그 뒤, 그 전, 그 밖에처럼 시간과 범위를 나타내는 관용 표현은 지시어 번역투가 아니다."""
    text = "그 뒤 다시 실행합니다. 그 전에 확인합니다. 그 밖에는 고치지 않습니다. 그 결과 통과했습니다.\n"
    assert doc_style_problems(text) == []


@pytest.mark.parametrize("path", DOCS, ids=lambda p: p.relative_to(ROOT).as_posix())
def test_repo_docs_pass_style_check(path: Path) -> None:
    assert doc_style_problems(path.read_text(encoding="utf-8")) == []


def test_broken_links_reports_missing_file_and_heading(tmp_path: Path) -> None:
    """문서 사이 링크는 제목을 바꾸면 조용히 깨진다(2026-11-19: decisions.tsv 가 README 의 옛 절 번호를 가리켰다)."""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "b.md").write_text("# B\n\n## 다시 만드는 법\n", encoding="utf-8")
    (tmp_path / "docs" / "t.tsv").write_text("a\tb\n", encoding="utf-8")
    doc = tmp_path / "a.md"
    ok = "[`b`](docs/b.md#다시-만드는-법) [t](docs/t.tsv) [위](#a) [웹](https://example.com/x#y)\n\n# A\n"
    assert broken_links(ok, doc) == []
    bad = (
        "[b](docs/b.md#옛-제목) [없음](docs/none.md)\n\n- 목록\n\n    [목록 안](docs/in-list.md)\n\n"
        "`[인라인](inline-code.md)`\n\n~~~\n[블록](tilde-block.md)\n~~~\n"
    )
    problems = "\n".join(broken_links(bad, doc))
    assert "docs/b.md#옛-제목" in problems and "docs/none.md" in problems and "docs/in-list.md" in problems
    assert "inline-code.md" not in problems and "tilde-block.md" not in problems


@pytest.mark.parametrize("path", DOCS, ids=lambda p: p.relative_to(ROOT).as_posix())
def test_repo_docs_links_resolve(path: Path) -> None:
    assert broken_links(path.read_text(encoding="utf-8"), path) == []

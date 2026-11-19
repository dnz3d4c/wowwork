"""저장소의 한국어 문서(README, 지침, 스킬, docs)에 남기 쉬운 번역투와 군더더기를 잡는다.

번역 설명서는 tools.manual check 가 따로 검사한다. 이 검사는 사람이 직접 쓰는 저장소 문서용이다.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.manual import doc_style_problems

ROOT = Path(__file__).resolve().parent.parent
DOCS = sorted(
    [ROOT / "README.md", ROOT / "CLAUDE.md", ROOT / "reviews" / "README.md"]
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

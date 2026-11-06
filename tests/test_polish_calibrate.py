"""설명서 다듬기 평가 구조 검증 도구: 오류 심기, 격리 폴더, 채점."""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.review.polish_calibrate import apply_doc_seeds, build_doc_sandbox, hits, score_doc

DOC = "# 제목\n\n단축키 화면은 키를 보여 줍니다. 이 페이지는 단축키 화면 사용법을 설명합니다.\n"


def test_apply_replaces_each_original_once() -> None:
    seeds = [
        {"id": "a", "origin": "claude", "original": "단축키 화면 사용법", "seeded": "그 화면을 쓰는 방법"}
    ]
    assert "그 화면을 쓰는 방법을 설명합니다" in apply_doc_seeds(DOC, seeds)


def test_apply_rejects_missing_or_ambiguous_original() -> None:
    with pytest.raises(ValueError, match="없음"):
        apply_doc_seeds(DOC, [{"id": "a", "origin": "gpt", "original": "없는 문장", "seeded": "x"}])
    with pytest.raises(ValueError, match="2번"):
        apply_doc_seeds(DOC, [{"id": "a", "origin": "gpt", "original": "단축키 화면", "seeded": "x"}])


def test_apply_rejects_overlapping_seeds() -> None:
    seeds = [
        {"id": "a", "origin": "claude", "original": "키를 보여 줍니다", "seeded": "키를 보여줌"},
        {"id": "b", "origin": "gpt", "original": "보여 줍니다. 이 페이지", "seeded": "보임. 이 쪽"},
    ]
    with pytest.raises(ValueError, match="겹침"):
        apply_doc_seeds(DOC, seeds)


def test_hits_matches_overlapping_quote() -> None:
    assert hits("이 페이지는 그 화면을 쓰는 방법을 설명합니다.", "그 화면을 쓰는 방법")
    assert hits("그 화면을", "그 화면을 쓰는 방법")  # 평가자가 일부만 인용
    assert not hits("단축키 화면은 키를 보여 줍니다.", "그 화면을 쓰는 방법")


def test_score_counts_recall_and_non_seed_findings() -> None:
    key = [
        {"id": "a", "origin": "claude", "seeded": "그 화면을 쓰는 방법"},
        {"id": "b", "origin": "gpt", "seeded": "경보 편집기"},
    ]
    runs = [
        {
            "provider": "claude",
            "persona": "manual-editor",
            "findings": [{"quote": "그 화면을 쓰는 방법을"}, {"quote": "다른 문장"}],
        },
        {"provider": "gpt", "persona": "newcomer", "findings": []},
    ]
    s = score_doc(runs, key)
    assert s["claude"]["recall"] == "1/2"
    assert s["claude"]["by_origin"] == {"claude": "1/1", "gpt": "0/1"}
    assert s["claude"]["non_seed"] == 1
    assert s["gpt"]["recall"] == "0/2"
    assert s["combined"]["missed"] == ["b"]


def test_sandbox_holds_seeded_file_but_no_original_or_key(tmp_path: Path) -> None:
    work, app, loc = tmp_path / "wowwork", tmp_path / "WowVision", tmp_path / "vision-locale"
    (work / "tools/review/prompts").mkdir(parents=True)
    (work / "tools/review/prompts/polish-base.md").write_text("p", encoding="utf-8")
    (work / "tools/review/polish-findings.schema.json").write_text("{}", encoding="utf-8")
    (work / "docs").mkdir()
    (work / "docs/decisions.tsv").write_text("d", encoding="utf-8")
    for lang in ("en", "ko"):
        (app / "docs/src/user" / lang / "basics").mkdir(parents=True)
    (app / "docs/src/user/en/basics/k.md").write_text("en", encoding="utf-8")
    (app / "docs/src/user/ko/basics/k.md").write_text(DOC, encoding="utf-8")
    (app / "Core").mkdir()
    (app / "Core/a.lua").write_text("lua", encoding="utf-8")
    for lang in ("enUS", "koKR"):
        (loc / lang).mkdir(parents=True)
        (loc / lang / "a.lua").write_text(lang, encoding="utf-8")
    root = tmp_path / "sb"
    seeded = DOC.replace("단축키 화면 사용법", "그 화면을 쓰는 방법")
    build_doc_sandbox(root, "basics/k.md", seeded, work_dir=work, app_dir=app, locale_dir=loc)
    ko = root / "wowvision-ko/WowVision/docs/src/user/ko/basics/k.md"
    assert ko.read_text(encoding="utf-8") == seeded
    assert (root / "wowvision-ko/WowVision/Core/a.lua").exists()
    assert (root / "wowvision-ko/vision-locale/koKR/a.lua").exists()
    assert (root / "wowwork/tools/review/prompts/polish-base.md").exists()
    assert not (root / "wowwork/reviews").exists()
    all_text = "".join(p.read_text(encoding="utf-8", errors="ignore") for p in root.rglob("*") if p.is_file())
    assert "단축키 화면 사용법" not in all_text

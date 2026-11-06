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
    seed = {"original": "단축키 화면 사용법을 설명합니다", "seeded": "그 화면을 쓰는 방법을 설명합니다"}
    assert hits("이 페이지는 그 화면을 쓰는 방법을 설명합니다.", seed)
    assert hits("그 화면을", seed)  # 평가자가 바뀐 부분만 인용
    assert not hits("단축키 화면은 키를 보여 줍니다.", seed)


def test_hits_ignores_overlap_only_in_unchanged_words() -> None:
    """바뀐 부분이 아니라 흔한 구절('Enter를 누릅니다')만 겹치는 지적은 검출이 아니다."""
    seed = {
        "original": "음성 메뉴에서 음성 종류로 이동해 Enter를 누릅니다.",
        "seeded": "말하기 설정에서 음성 종류로 이동해 Enter를 누릅니다.",
    }
    assert hits("말하기 설정에서 음성 종류로", seed)
    assert not hits("음성 항목이 들릴 때까지 Down을 누른 다음 Enter를 누릅니다", seed)


def test_score_counts_recall_and_non_seed_findings() -> None:
    key = [
        {"id": "a", "origin": "claude", "original": "단축키 화면 사용법", "seeded": "그 화면을 쓰는 방법"},
        {"id": "b", "origin": "gpt", "original": "TTS 경보 편집기", "seeded": "경보 편집기"},
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


def test_runs_from_journal_pairs_labels_with_results(tmp_path: Path) -> None:
    from tools.review.polish_calibrate import runs_from_journal

    j = tmp_path / "journal.jsonl"
    j.write_text(
        '{"type":"launched"}\n'
        '{"type":"started","key":"k1","label":"claude:newcomer"}\n'
        '{"type":"started","key":"k2","label":"gpt:wow-veteran"}\n'
        '{"type":"result","key":"k2","result":{"ok":true,"findings":[{"quote":"q"}]}}\n'
        '{"type":"result","key":"k1","result":{"findings":[]}}\n',
        encoding="utf-8",
    )
    out = runs_from_journal(j)
    assert out["failedReviewers"] == 0
    assert {(r["provider"], r["persona"], len(r["findings"])) for r in out["result"]} == {
        ("claude", "newcomer", 0),
        ("gpt", "wow-veteran", 1),
    }


def test_runs_from_journal_counts_failed_gpt(tmp_path: Path) -> None:
    from tools.review.polish_calibrate import runs_from_journal

    j = tmp_path / "journal.jsonl"
    j.write_text(
        '{"type":"started","key":"k1","label":"gpt:newcomer"}\n'
        '{"type":"result","key":"k1","result":{"ok":false,"findings":[]}}\n',
        encoding="utf-8",
    )
    assert runs_from_journal(j)["failedReviewers"] == 1


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

"""평가 절차 보완 장치: 용어집 검사, 관련 번역 첨부, 판정 근거 검사, 접근 경로 감사, 오류 목록 병합."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tools.glossary import Term, violations
from tools.review.build_batch import related_entries
from tools.review.guard import foreign_paths, valid_evidence
from tools.review.seed import merge_seeds

ROOT = "C:/sandbox/calib"


def test_glossary_flags_missing_term_and_honours_alternatives_and_exceptions() -> None:
    terms = [
        Term("beacon", ("비컨",), frozenset(), ""),
        Term("the route goes on after it", ("이후 경로 계속", "그 후 경로가 이어집니다"), frozenset(), ""),
        Term("healer", ("치유 전담",), frozenset({"a.lua::spirit healer"}), ""),
    ]
    entries = {
        ("a.lua", "Beacon Sound"): ("Beacon Sound", "신호 소리"),
        ("a.lua", "Dive"): ("Dive; the route goes on after it", "잠수; 이후 경로 계속"),
        ("a.lua", "Wait"): ("Wait; the route goes on after it", "기다리십시오; 그 후 경로가 이어집니다"),
        ("a.lua", "spirit healer"): ("spirit healer", "영혼의 치유사"),
        ("a.lua", "Beacons"): ("Beacons", "비컨 목록"),
    }
    assert violations(terms, entries) == ["a.lua::Beacon Sound: 'beacon' -> '비컨' 없음 ('신호 소리')"]


def test_related_entries_share_phrases_and_skip_self() -> None:
    others = {
        "n.lua::Use %s; the route goes on after it": (
            "Use %s; the route goes on after it",
            "%s 이용; 이후 경로 계속",
        ),
        "n.lua::Dive here; the route goes on after it": (
            "Dive here; the route goes on after it",
            "여기서 잠수; 이후 경로 계속",
        ),
        "n.lua::Beacon": ("Beacon", "비컨"),
    }
    item = {"id": "n.lua::Wait; the route goes on after it", "en": "Wait; the route goes on after it"}
    others[item["id"]] = (item["en"], "x")
    rel = related_entries(item, others, limit=5)
    assert {r["id"] for r in rel} == {
        "n.lua::Use %s; the route goes on after it",
        "n.lua::Dive here; the route goes on after it",
    }
    assert all(r["ko"] for r in rel)


def test_related_entries_ignore_stopword_only_phrases() -> None:
    others = {"x.lua::A": ("Go to the", "가기"), "x.lua::B": ("Wind Bridge waiting point", "대기")}
    rel = related_entries({"id": "x.lua::C", "en": "Arrive at the Wind Bridge"}, others, limit=5)
    assert [r["id"] for r in rel] == ["x.lua::B"]


def test_valid_evidence_accepts_only_primary_sources() -> None:
    assert valid_evidence(["wowvision-ko/WowVision/tbc/petStable.lua:87", "input"])
    assert valid_evidence(["wowwork/cache/gs_koKR.csv:7919", "wowwork/docs/decisions.tsv"])
    assert valid_evidence(["wowwork/docs/translation-guide.md"])
    assert valid_evidence(["wowvision-ko/wowvision-installer/WowVisionInstaller/AddonInstaller.cs:383"])
    assert not valid_evidence([])
    assert not valid_evidence(["wowwork/docs/manual-plan.md:111"])
    assert not valid_evidence(["input", "wowwork/reviews/x/rebut.json"])


def test_foreign_paths_flags_access_outside_sandbox() -> None:
    text = (
        f'Get-Content "{ROOT}/wowwork/docs/translation-guide.md"; rg Free C:\\sandbox\\calib\\wowvision-ko; '
        "type C:/project/games/wowvision-ko/vision-locale/koKR/targeting.lua"
    )
    assert foreign_paths(text, ROOT) == ["C:/project/games/wowvision-ko/vision-locale/koKR/targeting.lua"]


def test_merge_seeds_keeps_first_on_conflict(tmp_path: Path) -> None:
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    a.write_text(json.dumps({"x::1": ["가", "뜻 반전", "accuracy"]}), "utf-8")
    b.write_text(
        json.dumps({"x::1": ["나", "용어", "terminology"], "x::2": ["다", "누락", "accuracy"]}), "utf-8"
    )
    merged = merge_seeds({"claude": a, "gpt": b})
    assert merged == {
        "x::1": ["가", "뜻 반전", "accuracy", "claude"],
        "x::2": ["다", "누락", "accuracy", "gpt"],
    }


def test_apply_seeds_patches_item_and_related_lists() -> None:
    from tools.review.seed import apply_seeds

    data: dict[str, Any] = {
        "items": [
            {"id": "t.lua::Free", "ko": "해제됨", "related": []},
            {
                "id": "t.lua::Free Sound",
                "ko": "해제 소리",
                "related": [{"id": "t.lua::Free", "en": "Free", "ko": "해제됨"}],
            },
        ]
    }
    answers = apply_seeds(data, {"t.lua::Free": ["자유", "불일치", "terminology", "claude"]})
    assert data["items"][0]["ko"] == "자유"
    assert data["items"][1]["related"][0]["ko"] == "자유"
    assert answers == {
        "t.lua::Free": {
            "original": "해제됨",
            "seeded": "자유",
            "kind": "불일치",
            "lens": "terminology",
            "origin": "claude",
        }
    }


def test_sandbox_has_no_seeded_originals(tmp_path: Path) -> None:
    from tools.review.sandbox import build_sandbox

    loc = tmp_path / "loc"
    (loc / "enUS").mkdir(parents=True)
    (loc / "koKR").mkdir()
    (loc / "enUS" / "t.lua").write_text('local L = x\n\nL["Free"] = true\nL["Other"] = true\n', "utf-8")
    hdr = 'local L = LibStub("AceLocale-3.0"):NewLocale("WowVision", "koKR")\nif not L then return end\n'
    (loc / "koKR" / "t.lua").write_text(hdr + '\nL["Free"] = "해제됨"\nL["Other"] = "기타"\n', "utf-8")
    app = tmp_path / "app"
    (app / "core").mkdir(parents=True)
    (app / "core" / "m.lua").write_text('return L["Free"]\n', "utf-8")
    (app / ".git").mkdir()
    (app / ".git" / "secret").write_text("해제됨", "utf-8")
    work = tmp_path / "work"
    for d in ("docs", "cache", "tools/review/prompts"):
        (work / d).mkdir(parents=True)
    (work / "docs" / "translation-guide.md").write_text("지침", "utf-8")
    (work / "docs" / "manual-plan.md").write_text('L["Free"] = "해제됨"', "utf-8")
    (work / "tools" / "review" / "prompts" / "common.md").write_text("공통", "utf-8")
    root = tmp_path / "sb"
    batch = {"items": [{"id": "t.lua::Free", "ko": "자유", "related": []}]}
    build_sandbox(root, batch, {"t.lua::Free": "자유"}, locale_dir=loc, app_dir=app, work_dir=work)
    texts = [p.read_text("utf-8", errors="replace") for p in root.rglob("*") if p.is_file()]
    assert not any('L["Free"] = "해제됨"' in t for t in texts)
    assert any('L["Free"] = "자유"' in t for t in texts)
    assert (root / "wowwork" / "docs" / "translation-guide.md").exists()
    assert not (root / "wowwork" / "docs" / "manual-plan.md").exists()
    assert not (root / "wowvision-ko" / "WowVision" / ".git").exists()
    assert (root / "batch.json").exists()


def test_audit_codex_ignores_shell_exe_and_flags_escape() -> None:
    from tools.review.audit import codex_commands, suspicious

    ev = {
        "type": "item.completed",
        "item": {
            "type": "command_execution",
            "command": r'"C:\Program Files\PowerShell\7\pwsh.exe" -Command "Get-Content ..\..\koKR\t.lua"',
        },
    }
    cmds = codex_commands([json.dumps(ev), "not json"])
    assert len(cmds) == 1
    assert suspicious(cmds[0], ROOT) == [r'상위 폴더 이동: ..\..\koKR\t.lua"']
    ok = r'"C:\Program Files\PowerShell\7\pwsh.exe" -Command "rg Free C:/sandbox/calib/wowvision-ko"'
    assert suspicious(ok, ROOT) == []


def test_audit_claude_only_reviewer_transcripts() -> None:
    from tools.review.audit import claude_tool_inputs

    reviewer = [
        json.dumps({"type": "user", "message": {"content": "너는 번역 평가자다."}}),
        json.dumps(
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {"type": "tool_use", "name": "Read", "input": {"file_path": "C:/project/x.lua"}}
                    ]
                },
            }
        ),
    ]
    runner = [json.dumps({"type": "user", "message": {"content": "다음 명령을 실행한다"}})]
    assert claude_tool_inputs(reviewer) == ["C:/project/x.lua"]
    assert claude_tool_inputs(runner) is None


def test_score_recall_by_provider_and_origin() -> None:
    from tools.review.score import score

    key = {"a::1": {"origin": "claude"}, "a::2": {"origin": "gpt"}}
    runs = [
        {"provider": "claude", "lens": "accuracy", "findings": [{"id": "a::1"}, {"id": "a::9"}]},
        {"provider": "claude", "lens": "context", "findings": [{"id": "a::1"}]},
        {"provider": "gpt", "lens": "accuracy", "findings": [{"id": "a::1"}, {"id": "a::2"}]},
    ]
    s = score(runs, key)
    assert s["claude"]["recall"] == "1/2"
    assert s["claude"]["by_origin"] == {"claude": "1/1", "gpt": "0/1"}
    assert s["claude"]["missed"] == ["a::2"]
    assert s["claude"]["non_seed_flagged"] == ["a::9"]
    assert s["gpt"]["recall"] == "2/2"
    assert s["combined"]["recall"] == "2/2"


def test_foreign_paths_collapses_doubled_separators() -> None:
    from tools.review.audit import suspicious

    assert suspicious(r'"C:\Program Files\PowerShell\7\pwsh.exe" -Command "rg x"', ROOT) == []
    assert foreign_paths(r"C:\project\games\x.lua", ROOT) == ["C:/project/games/x.lua"]


def test_audit_claude_finds_reviewer_prompt_after_harness_relay() -> None:
    from tools.review.audit import claude_tool_inputs

    lines = [
        json.dumps({"type": "user", "message": {"content": "[Workflow harness — user request] 번역 퀄리티"}}),
        json.dumps(
            {"type": "user", "message": {"content": "[Workflow harness — computed task] 너는 번역 평가자다."}}
        ),
        json.dumps(
            {
                "type": "assistant",
                "message": {
                    "content": [{"type": "tool_use", "name": "Grep", "input": {"path": "C:/project/games"}}]
                },
            }
        ),
    ]
    assert claude_tool_inputs(lines) == ["C:/project/games"]


def test_valid_evidence_rejects_lookalike_paths() -> None:
    assert not valid_evidence(["wowwork/docs/decisions.tsv.fake"])
    assert not valid_evidence(["wowwork/reviews/rebut.json#wowwork/docs/decisions.tsv"])
    assert not valid_evidence(["wowwork/cache/gs_fake.csv"])
    assert not valid_evidence(["notwowwork/docs/decisions.tsv"])
    assert valid_evidence(["C:/project/games/wowwork/docs/decisions.tsv"])
    assert valid_evidence(["wowwork/cache/gs_koKR.csv:7919-7920"])
    assert valid_evidence([r"C:\project\games\wowvision-ko\WowVision\tbc\petStable.lua:87"])


def test_merge_seeds_accepts_generator_output_format(tmp_path: Path) -> None:
    g = tmp_path / "g.json"
    g.write_text(
        json.dumps({"seeds": [{"id": "x::1", "seeded": "가", "kind": "누락", "lens": "accuracy"}]}), "utf-8"
    )
    assert merge_seeds({"gpt": g}) == {"x::1": ["가", "누락", "accuracy", "gpt"]}


def test_decisions_refuse_incomplete_batches() -> None:
    from tools.review.decisions import incomplete_batches

    result: list[dict[str, Any]] = [
        {"batch": "b1", "failedReviewers": 0},
        {"batch": "b2", "failedReviewers": 1},
        {"batch": "b3"},
    ]
    assert incomplete_batches(result) == ["b2", "b3"]


def test_glossary_blocks_reverted_translations() -> None:
    """2026-11-06 최종 검수에서 다시 들어올 뻔한 번역 두 개를 확정 용어집이 막는다.

    - "카메라 따라가기 방식": 게임 공식 CAMERA_FOLLOWING_STYLE은 "시점 전환 방식". 2026-11-05에 한 번 되돌렸는데 다시 제안됐다.
    - "추가 전리품 주사위": "추가 전리품"은 Bonus Loot의 공식 번역이다. bonus roll의 공식 번역은 "보너스 주사위".
    """
    from tools.glossary import load_glossary

    camera_en = "You can change the camera following style in the game options under Controls."
    entries = {
        ("navigation.lua", "camera"): (
            camera_en,
            "카메라 따라가기 방식은 게임 설정의 조작 설정에서 바꿀 수 있습니다.",
        ),
        ("bindings.lua", "Roll Bonus"): ("Roll Bonus", "추가 전리품 주사위"),
    }
    assert len(violations(load_glossary(), entries)) == 2
    ok = {
        ("navigation.lua", "camera"): (
            camera_en,
            "시점 전환 방식은 게임 설정의 조작 설정에서 바꿀 수 있습니다.",
        ),
        ("bindings.lua", "Roll Bonus"): ("Roll Bonus", "보너스 주사위"),
    }
    assert violations(load_glossary(), ok) == []

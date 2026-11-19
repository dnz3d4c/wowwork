"""판정 결과로 확정 번역을 정하는 규칙(tools/review/decisions.py).

2026-11-08: 이 규칙이 full.js·manual.js·logintool_loc.py 에 따로 있었다. 한곳으로 모으면서
두 판정자의 근거를 판정자마다 검사하고(codex C·D), 에이전트 실패가 있으면 반영 목록을 쓰지 않게 했다(codex B).
"""

from __future__ import annotations

from typing import Any

import pytest

from tools.review.decisions import decide, decide_batch, decide_judged

OK = ["wowvision-ko/WowVision/a.lua:3"]


def v(ref: str, uphold: bool, final_ko: str = "", evidence: list[str] | None = None) -> dict[str, Any]:
    return {
        "ref": ref,
        "uphold": uphold,
        "final_ko": final_ko,
        "reason": "r",
        "evidence_sources": OK if evidence is None else evidence,
    }


def group(id_: str, providers: list[str], category: str = "listening") -> dict[str, Any]:
    return {
        "id": id_,
        "providers": providers,
        "consensus": len(providers) == 2,
        "findings": [{"by": f"{p}-x", "category": category, "severity": "major"} for p in providers],
    }


def batch(
    groups: list[dict[str, Any]],
    responses: list[dict[str, Any]],
    judged: list[str],
    gpt: list[dict[str, Any]] | None,
    claude: list[dict[str, Any]] | None,
    failed: int = 0,
) -> dict[str, Any]:
    return {
        "batch": "b1",
        "failedReviewers": failed,
        "groups": groups,
        "responses": responses,
        "judged": judged,
        "verdicts": {"gpt": gpt, "claude": claude},
    }


def resp(id_: str, action: str, final_ko: str) -> dict[str, Any]:
    return {"id": id_, "action": action, "final_ko": final_ko, "reason": "r"}


def test_accepted_finding_is_applied_and_consensus_dispute_goes_to_user() -> None:
    b = batch(
        [group("a::1", ["gpt"]), group("a::2", ["gpt", "claude"])],
        [resp("a::1", "accept", "새것"), resp("a::2", "dispute", "옛것")],
        [],
        [],
        [],
    )
    decisions, esc = decide_batch(b)
    assert [(d["id"], d["final_ko"]) for d in decisions] == [("a::1", "새것")]
    assert [e["id"] for e in esc] == ["a::2"]


def test_dispute_upheld_by_both_uses_other_company_wording() -> None:
    """GPT가 지적했으면 확정 문장은 Claude 판정자의 것."""
    b = batch(
        [group("a::1", ["gpt"])],
        [resp("a::1", "dispute", "옛것")],
        ["a::1"],
        [v("a::1", True, "gpt안")],
        [v("a::1", True, "claude안")],
    )
    decisions, esc = decide_batch(b)
    assert [d["final_ko"] for d in decisions] == ["claude안"] and esc == []


def test_one_judge_without_evidence_is_not_a_decision() -> None:
    """codex C·D: 근거를 합쳐서 보면 한 판정자가 근거를 비워도 통과했다."""
    b = batch(
        [group("a::1", ["gpt"])],
        [resp("a::1", "dispute", "옛것")],
        ["a::1"],
        [v("a::1", True, "gpt안", evidence=[])],
        [v("a::1", True, "claude안")],
    )
    decisions, esc = decide_batch(b)
    assert decisions == [] and "근거" in esc[0]["why"]


def test_accepted_terminology_finding_rejected_by_both_keeps_current() -> None:
    b = batch(
        [group("a::1", ["gpt"], "terminology")],
        [resp("a::1", "accept", "새 용어")],
        ["a::1"],
        [v("a::1", False)],
        [v("a::1", False)],
    )
    assert decide_batch(b) == ([], [])


def test_accepted_terminology_finding_upheld_uses_translator_wording() -> None:
    b = batch(
        [group("a::1", ["gpt"], "terminology")],
        [resp("a::1", "accept", "새 용어")],
        ["a::1"],
        [v("a::1", True, "다른 안")],
        [v("a::1", True, "또 다른 안")],
    )
    decisions, _ = decide_batch(b)
    assert [d["final_ko"] for d in decisions] == ["새 용어"]


def test_split_verdicts_go_to_user() -> None:
    b = batch(
        [group("a::1", ["gpt"])],
        [resp("a::1", "dispute", "옛것")],
        ["a::1"],
        [v("a::1", True, "x")],
        [v("a::1", False)],
    )
    decisions, esc = decide_batch(b)
    assert decisions == [] and esc[0]["why"] == "두 판정자의 결론이 다름"


def test_decide_writes_nothing_when_an_agent_failed() -> None:
    """codex B: 판정자가 실패해 빠진 항목이 있어도 반영 목록을 썼다. 다시 돌린 뒤 한 번에 반영한다."""
    failed_judge = batch(
        [group("a::1", ["gpt"])], [resp("a::1", "dispute", "옛것")], ["a::1"], None, [v("a::1", True, "x")]
    )
    with pytest.raises(SystemExit):
        decide([failed_judge], {})
    no_translator = batch([group("a::1", ["gpt"])], [], [], [], [])
    with pytest.raises(SystemExit):
        decide([no_translator], {})
    with pytest.raises(SystemExit):
        decide([batch([], [], [], [], [], failed=1)], {})


def test_decide_lists_only_changed_translations() -> None:
    b = batch(
        [group("a::1", ["gpt"]), group("a::2", ["gpt"])],
        [resp("a::1", "accept", "새것"), resp("a::2", "accept", "그대로")],
        [],
        [],
        [],
    )
    rows, esc = decide([b], {"a::1": "옛것", "a::2": "그대로"})
    assert rows == [{"id": "a::1", "before": "옛것", "ko": "새것"}] and esc == []


def test_decide_judged_for_manual() -> None:
    """설명서: 번역자가 반박한 지적만 판정한다. 인정된 것은 quote 와 확정 문장을 돌려준다."""
    items = [
        {"ref": "f#gpt-0", "provider": "gpt", "quote": "옛 문장"},
        {"ref": "f#claude-0", "provider": "claude", "quote": "다른 문장"},
    ]
    out = decide_judged(
        items,
        [v("f#gpt-0", True, "g"), v("f#claude-0", False)],
        [v("f#gpt-0", True, "c"), v("f#claude-0", False)],
    )
    assert out["upheld"] == [{"ref": "f#gpt-0", "quote": "옛 문장", "final_ko": "c", "evidence": OK + OK}]
    assert out["disputeWon"] == 1 and out["escalations"] == []

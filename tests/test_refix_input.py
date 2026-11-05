from tools.review.refix_input import build_items, overlaps


def test_overlaps_ignores_whitespace_and_needs_containment() -> None:
    assert overlaps("가 나  다", "나 다")
    assert not overlaps("가 나", "다 라")
    assert not overlaps("", "가")


def test_consensus_only_across_providers() -> None:
    blocking = [
        {"by": "claude", "quote": "같은 문장 전체"},
        {"by": "gpt", "quote": "같은 문장"},
        {"by": "claude", "quote": "다른 곳"},
        {"by": "claude", "quote": "다른 곳 하나 더"},
    ]
    items = build_items("a/b.md", blocking)
    assert [f["consensus"] for f in items] == [True, True, False, False]
    assert items[1]["ref"] == "a/b.md#reg-gpt-1"


def test_judge_builds_gpt_input_for_disputed_refs_only(tmp_path) -> None:
    import json

    from tools.review.refix_input import judge

    d = tmp_path / "a" / "b"
    d.mkdir(parents=True)
    finding = {
        "category": "accuracy",
        "severity": "major",
        "quote": "q",
        "suggestion": "s",
        "problem": "p",
        "evidence": "e",
    }
    items = [
        {**finding, "ref": "a/b.md#reg-claude-0", "by": "claude"},
        {**finding, "ref": "a/b.md#reg-gpt-1", "by": "gpt"},
    ]
    (d / "refix-input.json").write_text(json.dumps(items), encoding="utf-8")
    rebut = {"responses": [{"ref": "a/b.md#reg-gpt-1", "action": "dispute", "reason": "r", "upstream": ""}]}
    (d / "refix-rebut.json").write_text(json.dumps(rebut), encoding="utf-8")
    assert judge(tmp_path, "a/b.md", ["a/b.md#reg-gpt-1"]) == 0
    out = json.loads((d / "refix-judge-gpt-input.json").read_text(encoding="utf-8"))
    assert [i["ref"] for i in out["items"]] == ["a/b.md#reg-gpt-1"]
    assert out["items"][0]["translator"]["action"] == "dispute"


def test_judge_accepts_rebut_saved_as_bare_list(tmp_path) -> None:
    import json

    from tools.review.refix_input import judge

    d = tmp_path / "a" / "b"
    d.mkdir(parents=True)
    finding = {
        "category": "accuracy",
        "severity": "major",
        "quote": "q",
        "suggestion": "s",
        "problem": "p",
        "evidence": "e",
    }
    (d / "refix-input.json").write_text(json.dumps([{**finding, "ref": "r1", "by": "gpt"}]), encoding="utf-8")
    (d / "refix-rebut.json").write_text(
        json.dumps([{"ref": "r1", "action": "dispute", "reason": "x", "upstream": ""}]), encoding="utf-8"
    )
    assert judge(tmp_path, "a/b.md", ["r1"]) == 0
    out = json.loads((d / "refix-judge-gpt-input.json").read_text(encoding="utf-8"))
    assert out["items"][0]["translator"]["reason"] == "x"


def test_load_rebut_rejects_malformed_and_duplicate_entries(tmp_path) -> None:
    import json

    import pytest

    from tools.review.refix_input import load_rebut

    p = tmp_path / "refix-rebut.json"
    ok = {"ref": "r1", "action": "dispute", "reason": "x", "upstream": ""}
    for bad in ([{"ref": "r1"}], [ok, ok], [{**ok, "action": "maybe"}], {"nope": []}, "text"):
        p.write_text(json.dumps(bad), encoding="utf-8")
        with pytest.raises(ValueError):
            load_rebut(p)
    p.write_text(json.dumps({"responses": [ok]}), encoding="utf-8")
    assert load_rebut(p) == {"r1": ok}

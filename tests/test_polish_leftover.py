"""다듬기 뒤 남은 지적 모으기."""

from __future__ import annotations

from tools.review.polish_leftover import collect

B = {
    "by": "gpt",
    "category": "accuracy",
    "severity": "major",
    "suggestion": "s",
    "problem": "p",
    "evidence": "e",
}


def test_keeps_items_whose_quote_is_still_in_file_and_counts_gone() -> None:
    main = {
        "reviewed": [
            {
                "file": "a.md",
                "escalations": [
                    {
                        "ref": "a.md#gpt-x-0",
                        "why": "두 판정자의 결론이 다름",
                        "quote": "남은 문장",
                        "suggestion": "새",
                        "gpt": "g",
                        "claude": "c",
                    },
                    {
                        "ref": "a.md#gpt-x-1",
                        "why": "편집자 응답 없음",
                        "quote": "사라진 문장",
                        "suggestion": "새",
                    },
                    {"ref": "a.md", "why": "평가자 전원 실패"},
                ],
            }
        ]
    }
    reg = {
        "failed": [{"file": "a.md", "blocking": [{**B, "quote": "리테일과"}, {**B, "quote": "남은 문장"}]}]
    }
    by_file, gone = collect(main, reg, {"a.md": "여기 남은 문장이 있다. Retail과"})
    kinds = sorted(i["kind"] for i in by_file["a.md"])
    assert kinds == ["regression", "split"]
    assert gone == 2

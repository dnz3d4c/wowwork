"""평가 결과로 확정 번역을 정한다. 판정 규칙은 여기 한 곳에만 있다.

Workflow 스크립트(full.js, manual.js)는 누구에게 무엇을 물을지만 정하고, 받은 답으로 무엇을 확정할지는
이 모듈이 정한다(2026-11-08, 그전에는 같은 규칙이 full.js, manual.js, logintool_loc.py 에 따로 있었다).

사용:
  uv run python -m tools.review.decisions <full.js 출력.json> <평가 폴더>
      UI 문자열. <평가 폴더>/apply.tsv(file, key, ko)와 escalations.json(사용자 판단 목록)을 쓴다.
      apply.tsv 는 `uv run python -m tools.sync_locale <apply.tsv>` 로 반영한다.
  uv run python -m tools.review.decisions manual <판정 입력.json> <출력.json>
      설명서. manual.js 의 수정 에이전트가 판정을 받은 뒤 실행해 고칠 목록을 받는다.

에이전트(평가자, 번역자, 판정자)가 하나라도 실패하면 아무것도 쓰지 않고 끝난다. 같은 Run ID 로
Workflow 를 이어서 실행하면 끝난 에이전트는 캐시를 쓰므로 다시 돌리는 비용이 작다.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

from tools.review.guard import valid_evidence

Verdict = dict[str, Any]


def incomplete_batches(result: list[dict[str, Any]]) -> list[str]:
    """평가자가 하나라도 실패했거나 실패 수 기록이 없는 묶음."""
    return [b["batch"] for b in result if b.get("failedReviewers", 1) != 0]


def _by_ref(verdicts: list[Verdict] | None) -> dict[str, Verdict] | None:
    return None if verdicts is None else {x["ref"]: x for x in verdicts}


def outcome(ref: str, gpt: dict[str, Verdict] | None, claude: dict[str, Verdict] | None) -> dict[str, Any]:
    """두 회사 판정 → {"uphold": bool, "gpt": 판정, "claude": 판정, "evidence": [...]} 또는 {"why": 사유}.

    판정자마다 근거가 허용 자료여야 한다. 한쪽 근거만 보면 근거 없이 동의한 판정이 확정에 참여한다.
    """
    a = (gpt or {}).get(ref)
    c = (claude or {}).get(ref)
    if a is None or c is None:
        return {"why": f"판정 누락 (gpt {a is not None}, claude {c is not None})", "retry": True}
    bad = [
        name for name, x in (("gpt", a), ("claude", c)) if not valid_evidence(x.get("evidence_sources") or [])
    ]
    if bad:
        return {
            "why": f"판정 근거가 허용 자료가 아님 ({', '.join(bad)})",
            "evidence": {"gpt": a.get("evidence_sources"), "claude": c.get("evidence_sources")},
        }
    if a["uphold"] != c["uphold"]:
        return {
            "why": "두 판정자의 결론이 다름",
            "gpt": {"uphold": a["uphold"], "final_ko": a["final_ko"], "reason": a["reason"]},
            "claude": {"uphold": c["uphold"], "final_ko": c["final_ko"], "reason": c["reason"]},
        }
    return {
        "uphold": a["uphold"],
        "gpt": a,
        "claude": c,
        "evidence": [*a["evidence_sources"], *c["evidence_sources"]],
        "reason": f"gpt: {a['reason']} / claude: {c['reason']}",
    }


def decide_batch(b: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """full.js 묶음 하나 → (확정 결정, 확정하지 못한 항목).

    번역자가 수용한 지적은 그대로 확정한다. 판정에 보낸 항목(judged)은 두 판정이 일치해야 확정한다.
    지적을 인정할 때 확정 문장은 반박이면 지적한 회사가 아닌 쪽 판정자의 것, 수용이면 번역자의 것이다.
    """
    resp = {r["id"]: r for r in b.get("responses") or []}
    judged = set(b.get("judged") or [])
    verdicts = b.get("verdicts") or {}
    gpt, claude = _by_ref(verdicts.get("gpt")), _by_ref(verdicts.get("claude"))
    decisions: list[dict[str, Any]] = []
    escalations: list[dict[str, Any]] = []
    for g in b.get("groups") or []:
        r = resp.get(g["id"])
        sev = [f["severity"] for f in g["findings"]]
        if r is None:
            escalations.append({"id": g["id"], "why": "번역자 응답 없음", "retry": True})
            continue
        if g["id"] not in judged:
            if r["action"] == "accept":
                decisions.append(
                    {
                        "id": g["id"],
                        "final_ko": r["final_ko"],
                        "how": "consensus" if g["consensus"] else "accepted",
                        "sev": sev,
                    }
                )
            elif g["consensus"]:
                escalations.append(
                    {"id": g["id"], "why": "두 회사가 모두 지적했는데 번역자가 반박", "reason": r["reason"]}
                )
            continue
        o = outcome(g["id"], gpt, claude)
        if "why" in o:
            escalations.append({"id": g["id"], **o})
            continue
        if not o["uphold"]:
            continue  # 지금 번역 유지
        if r["action"] == "accept":
            final, how = r["final_ko"], "upheld-accept"
        else:
            final, how = (
                (o["gpt"] if g["providers"][0] == "claude" else o["claude"])["final_ko"],
                "upheld-by-both",
            )
        decisions.append(
            {
                "id": g["id"],
                "final_ko": final,
                "how": how,
                "reason": o["reason"],
                "evidence": o["evidence"],
                "sev": sev,
            }
        )
    return decisions, escalations


def decide(
    result: list[dict[str, Any]], current: dict[str, str]
) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    """full.js 출력 전체 → (바뀌는 항목 [{id, before, ko}], 사용자 판단 목록). current: id → 지금 번역."""
    broken = incomplete_batches(result)
    if broken:
        raise SystemExit(
            f"평가자가 실패한 묶음이 있어 반영하지 않는다(같은 Run ID 로 이어서 실행할 것): {broken}"
        )
    decisions: list[dict[str, Any]] = []
    escalations: list[dict[str, Any]] = []
    for b in result:
        d, e = decide_batch(b)
        decisions += d
        escalations += [{"batch": b["batch"], **x} for x in e]
    retry = [e for e in escalations if e.get("retry")]
    if retry:
        raise SystemExit(
            f"번역자·판정자가 실패한 항목 {len(retry)}건이 있어 반영하지 않는다(같은 Run ID 로 이어서 실행할 것): "
            f"{[(e['id'], e['why']) for e in retry]}"
        )
    rows = [
        {"id": d["id"], "before": current.get(d["id"], ""), "ko": d["final_ko"]}
        for d in decisions
        if d["final_ko"] != current.get(d["id"], "")
    ]
    return rows, escalations


def decide_judged(
    items: list[dict[str, Any]], gpt: list[Verdict] | None, claude: list[Verdict] | None
) -> dict[str, Any]:
    """설명서: 판정에 보낸 지적 [{ref, provider, quote}] → {upheld, disputeWon, escalations}."""
    gv, cv = _by_ref(gpt), _by_ref(claude)
    upheld: list[dict[str, Any]] = []
    escalations: list[dict[str, Any]] = []
    won = 0
    for f in items:
        o = outcome(f["ref"], gv, cv)
        if "why" in o:
            escalations.append({"ref": f["ref"], "quote": f["quote"], **o})
        elif o["uphold"]:
            other = o["gpt"] if f["provider"] == "claude" else o["claude"]
            upheld.append(
                {
                    "ref": f["ref"],
                    "quote": f["quote"],
                    "final_ko": other["final_ko"],
                    "evidence": o["evidence"],
                }
            )
        else:
            won += 1
    return {"upheld": upheld, "disputeWon": won, "escalations": escalations}


def main(argv: list[str]) -> int:
    if argv[0] == "manual":
        data = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
        out = decide_judged(data["items"], data["gpt"], data["claude"])
        Path(argv[2]).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print(
            f"고칠 곳 {len(out['upheld'])}, 반박 인정 {out['disputeWon']}, 사용자 판단 {len(out['escalations'])} -> {argv[2]}"
        )
        return 0
    from tools.locale_lib import KOKR_DIR, parse_locale_file

    out_json, review_dir = Path(argv[0]), Path(argv[1])
    result = json.loads(out_json.read_text(encoding="utf-8"))["result"]
    current = {f"{p.name}::{k}": v for p in KOKR_DIR.glob("*.lua") for k, v in parse_locale_file(p).items()}
    rows, escalations = decide(result, current)
    (review_dir / "escalations.json").write_text(
        json.dumps(escalations, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    with (review_dir / "apply.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["file", "key", "ko"])
        w.writerows([*r["id"].split("::", 1), r["ko"]] for r in rows)
    print(
        f"번역 변경 {len(rows)}건 -> {review_dir / 'apply.tsv'}, 사용자 판단 {len(escalations)}건 -> escalations.json"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

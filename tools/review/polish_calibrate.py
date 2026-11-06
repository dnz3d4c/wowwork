"""설명서 다듬기 평가 구조 검증: 설명서 한 파일에 오류를 심고, 격리 폴더를 만들고, 채점한다.

사용:
  uv run python -m tools.review.polish_calibrate build <격리폴더> <상대경로> <정답표.json> <심을목록.json>...
  uv run python -m tools.review.polish_calibrate journal <journal.jsonl> <결과.json>
  uv run python -m tools.review.polish_calibrate score <결과.json> <정답표.json>
심을 목록: [{"id", "origin"(claude|gpt), "original"(번역문에 한 번만 있는 구절), "seeded", "type"}]
격리 폴더에는 오류를 심은 번역문만 들어가고, 원래 문장과 정답표는 들어가지 않는다.
"""

from __future__ import annotations

import itertools
import json
import re
import shutil
import sys
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

from tools.locale_lib import REPO_ROOT, WOWVISION_DIR, upstream_locale_dir

WORK_FILES = (
    "docs/translation-guide.md",
    "docs/decisions.tsv",
    "docs/glossary.tsv",
    "cache/gs_enUS.csv",
    "cache/gs_koKR.csv",
    "cache/game_terms.tsv",
)
APP_IGNORE = shutil.ignore_patterns(".git", "docs", "audio", "mapdata", "*.ogg", "*.mp3", "*.blp", "*.tga")
MIN_SHARED = 6  # 평가자가 심은 구절의 일부만 인용해도 이만큼 겹치면 잡은 것으로 본다


def apply_doc_seeds(text: str, seeds: list[dict[str, str]]) -> str:
    spans: list[tuple[int, int, str]] = []
    for s in seeds:
        n = text.count(s["original"])
        if n == 0:
            raise ValueError(f"{s['id']}: 원래 구절 없음: {s['original']}")
        if n > 1:
            raise ValueError(f"{s['id']}: 원래 구절이 {n}번 나온다: {s['original']}")
        start = text.index(s["original"])
        spans.append((start, start + len(s["original"]), s["id"]))
    spans.sort()
    for (_, end, a), (start, _, b) in itertools.pairwise(spans):
        if start < end:
            raise ValueError(f"{a}와 {b}의 구절이 겹침")
    for s in sorted(seeds, key=lambda s: -text.index(s["original"])):
        i = text.index(s["original"])
        text = text[:i] + s["seeded"] + text[i + len(s["original"]) :]
    return text


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def _changed(original: str, seeded: str) -> tuple[int, int]:
    """seeded 안에서 원래 구절과 달라진 구간 [start, end). 지우기만 했으면 start == end."""
    p = 0
    while p < min(len(original), len(seeded)) and original[p] == seeded[p]:
        p += 1
    s = 0
    while s < min(len(original), len(seeded)) - p and original[-1 - s] == seeded[-1 - s]:
        s += 1
    return p, len(seeded) - s


def hits(quote: str, seed: dict[str, str]) -> bool:
    """지적이 심은 오류를 잡았는가: 지적 인용이 심은 구절과 겹치고, 그 겹침이 바뀐 구간에 닿아야 한다."""
    q, s = _norm(quote), _norm(seed["seeded"])
    if not q or not s:
        return False
    start, end = _changed(_norm(seed["original"]), s)
    lo, hi = (start, end) if end > start else (max(start - 1, 0), start + 1)
    blocks = SequenceMatcher(None, q, s, autojunk=False).get_matching_blocks()
    covered = [(b.b, b.b + b.size) for b in blocks if b.size >= min(4, len(s))]
    shared = sum(e - b for b, e in covered)
    touches = any(b < hi and lo < e for b, e in covered)
    return touches and shared >= min(MIN_SHARED, len(s), len(q))


def _summary(found: list[str], seeded_hit: dict[str, bool], key: list[dict[str, str]]) -> dict[str, Any]:
    origins = sorted({k["origin"] for k in key})
    return {
        "recall": f"{sum(seeded_hit.values())}/{len(key)}",
        "by_origin": {
            o: f"{sum(seeded_hit[k['id']] for k in key if k['origin'] == o)}/{sum(k['origin'] == o for k in key)}"
            for o in origins
        },
        "missed": [k["id"] for k in key if not seeded_hit[k["id"]]],
        "non_seed": len(found),
    }


def score_doc(runs: list[dict[str, Any]], key: list[dict[str, str]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    every: dict[str, bool] = {k["id"]: False for k in key}
    every_non: list[str] = []
    for prov in sorted({r["provider"] for r in runs}):
        quotes = [(r["persona"], f["quote"]) for r in runs if r["provider"] == prov for f in r["findings"]]
        hit = {k["id"]: any(hits(q, k) for _, q in quotes) for k in key}
        non = [q for _, q in quotes if not any(hits(q, k) for k in key)]
        out[prov] = _summary(non, hit, key)
        out[prov]["by_persona"] = {
            p: sorted(k["id"] for k in key if any(hits(q, k) for pp, q in quotes if pp == p))
            for p in sorted({p for p, _ in quotes} | {r["persona"] for r in runs if r["provider"] == prov})
        }
        for i, v in hit.items():
            every[i] = every[i] or v
        every_non += non
    out["combined"] = _summary(every_non, every, key)
    return out


def build_doc_sandbox(
    root: Path, rel: str, seeded_text: str, *, work_dir: Path, app_dir: Path, locale_dir: Path
) -> None:
    if root.exists():
        shutil.rmtree(root)
    work = root / "wowwork"
    for f in WORK_FILES:
        if (work_dir / f).exists():
            (work / f).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(work_dir / f, work / f)
    shutil.copytree(work_dir / "tools/review/prompts", work / "tools/review/prompts")
    for schema in (work_dir / "tools/review").glob("*.schema.json"):
        shutil.copy2(schema, work / "tools/review" / schema.name)
    app = root / "wowvision-ko/WowVision"
    shutil.copytree(app_dir, app, ignore=APP_IGNORE)
    for lang in ("en", "ko"):
        shutil.copytree(app_dir / "docs/src/user" / lang, app / "docs/src/user" / lang)
    (app / "docs/src/user/ko" / rel).write_text(seeded_text, encoding="utf-8", newline="\n")
    for lang in ("enUS", "koKR"):
        shutil.copytree(locale_dir / lang, root / "wowvision-ko/vision-locale" / lang)


def runs_from_journal(path: Path) -> dict[str, Any]:
    """Workflow 기록(journal.jsonl)에서 평가자별 결과를 모은다. 라벨은 '회사:페르소나'."""
    labels: dict[str, str] = {}
    runs, failed = [], 0
    for line in path.read_text(encoding="utf-8").splitlines():
        o = json.loads(line)
        if o["type"] == "started":
            labels[o["key"]] = o["label"]
        elif o["type"] == "result":
            provider, persona = labels[o["key"]].split(":", 1)
            r = o.get("result")
            if not r or r.get("ok") is False:
                failed += 1
                continue
            runs.append({"provider": provider, "persona": persona, "findings": r["findings"]})
    return {"failedReviewers": failed, "result": runs}


def main() -> int:
    cmd, rest = sys.argv[1], sys.argv[2:]
    if cmd == "journal":
        Path(rest[1]).write_text(
            json.dumps(runs_from_journal(Path(rest[0])), ensure_ascii=False, indent=1), encoding="utf-8"
        )
        return 0
    if cmd == "build":
        from tools.manual import EN_ROOT, KO_ROOT, locale_pairs, term_sheet

        root, rel, key_out = Path(rest[0]), rest[1], Path(rest[2])
        seeds = [s for p in rest[3:] for s in json.loads(Path(p).read_text(encoding="utf-8"))]
        if len({s["id"] for s in seeds}) != len(seeds):
            raise SystemExit("심을 목록의 id가 겹친다")
        en = (EN_ROOT / rel).read_text(encoding="utf-8")
        seeded = apply_doc_seeds((KO_ROOT / rel).read_text(encoding="utf-8"), seeds)
        build_doc_sandbox(
            root, rel, seeded, work_dir=REPO_ROOT, app_dir=WOWVISION_DIR, locale_dir=upstream_locale_dir()
        )
        batch = {"file": rel, "en": en, "ko": seeded, "terms": term_sheet(en, locale_pairs())}
        (root / "batch.json").write_text(json.dumps(batch, ensure_ascii=False, indent=1), encoding="utf-8")
        key_out.write_text(json.dumps(seeds, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{len(seeds)}개 심음 -> {root}")
        return 0
    if cmd == "score":
        result = json.loads(Path(rest[0]).read_text(encoding="utf-8"))
        if result.get("failedReviewers", 1) != 0:
            raise SystemExit(
                f"평가자 실패 {result.get('failedReviewers')}명: 이 검증은 무효라 채점하지 않는다"
            )
        key = json.loads(Path(rest[1]).read_text(encoding="utf-8"))
        for prov, s in score_doc(result["result"], key).items():
            print(prov, json.dumps(s, ensure_ascii=False))
        return 0
    raise SystemExit(f"모르는 명령: {cmd}")


if __name__ == "__main__":
    sys.exit(main())

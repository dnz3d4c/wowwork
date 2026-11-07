"""측정 애드온이 그린 카드 캡처를 로그인 툴과 같은 OCR로 읽고 정답과 비교한다.

정답은 애드온의 SavedVariables(LoginToolOcrBenchDB)에 있다. 줄마다
"페이지<TAB>배율<TAB>역할<TAB>꼬리표<TAB>문자열<TAB>왼쪽<TAB>위<TAB>오른쪽<TAB>아래"(화면 픽셀)이다.
역할: marker(페이지 표지 "PAGE n"), name, info("%d 레벨 %s"), zone.

사용:
  uv run python -m tools.logintool_bench.evaluate <SavedVariables 파일> <캡처 폴더> <보고서.md>
      [--helper <SkuLoginSense.exe>] [--extra "<보조 프로그램에 더 줄 인자>"]
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "WoW Login Tool Korean"
LEVEL_WORDS = ["Stufe", "Level", "Niveau", "Nivel", "Уровень", "레벨"]


def norm(text: str) -> str:
    """forever.ahk FvNorm 과 같은 비교: 소문자, 글자와 숫자만."""
    return "".join(ch for ch in text.lower() if ch.isalnum())


def cer(truth: str, got: str) -> float:
    a, b = norm(truth), norm(got)
    if not a:
        return 0.0 if not b else 1.0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return min(1.0, prev[-1] / len(a))


def has_level_word(text: str) -> bool:
    return any(w in text for w in LEVEL_WORDS)


def _unescape(s: str) -> str:
    return re.sub(r"\\(.)", lambda m: {"t": "\t", "n": "\n"}.get(m.group(1), m.group(1)), s)


def parse_truth(sv_text: str) -> list[dict[str, Any]]:
    items = []
    for raw in re.findall(r'^\s*"((?:[^"\\]|\\.)*)",\s*(?:--.*)?$', sv_text, re.MULTILINE):
        parts = _unescape(raw).split("\t")
        if len(parts) != 9:
            continue
        page, k, role, tag, text, left, top, right, bottom = parts
        items.append({
            "page": int(page), "k": float(k), "role": role, "tag": tag, "text": text,
            "l": int(left), "t": int(top), "r": int(right), "b": int(bottom),
        })
    return items


def match_lines(item: dict[str, Any], lines: list[dict[str, Any]], dx: int = 0, dy: int = 0) -> str:
    """정답 상자 안에 중심이 있는 OCR 줄을 왼쪽부터 이어 붙인다(OCR이 한 줄을 쪼개는 경우)."""
    h = item["b"] - item["t"]
    l, r = item["l"] + dx - h * 0.5, item["r"] + dx + h * 0.5
    t, b = item["t"] + dy - h * 0.3, item["b"] + dy + h * 0.3
    hits = [ln for ln in lines
            if l <= ln["x"] + ln["w"] / 2 <= r and t <= ln["y"] + ln["h"] / 2 <= b]
    return " ".join(ln["text"] for ln in sorted(hits, key=lambda ln: ln["x"]))


def run_helper(helper: Path, image: Path, extra: list[str]) -> dict[str, Any]:
    cmd = [str(helper), "sense", "--image", str(image), "--lang", "ko-KR",
           "--data", str(TOOL / "data" / "data.ini"), "--gametype", "Forever", *extra]
    out = subprocess.run(cmd, capture_output=True, check=False, timeout=120)
    text = out.stdout.decode("utf-8", errors="replace").strip().splitlines()
    return json.loads(text[-1]) if text else {"error": out.stderr.decode("utf-8", "replace")}


def _offset(marker: dict[str, Any], lines: list[dict[str, Any]]) -> tuple[int, int] | None:
    want = norm(marker["text"])
    for ln in lines:
        if norm(ln["text"]) == want:
            return ln["x"] - marker["l"], ln["y"] - marker["t"]
    return None


def _subs(truth: str, got: str) -> list[tuple[str, str]]:
    a, b = norm(truth), norm(got)
    pairs = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if op == "replace" and i2 - i1 == j2 - j1:
            pairs += list(zip(a[i1:i2], b[j1:j2]))
        elif op in ("replace", "delete"):
            pairs += [(ch, "∅") for ch in a[i1:i2]] if op == "delete" else [(a[i1:i2], b[j1:j2])]
    return pairs


def evaluate(items: list[dict[str, Any]], pages: dict[int, list[dict[str, Any]]]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    lost_pages = []
    by_page: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for it in items:
        by_page[it["page"]].append(it)
    for page, its in sorted(by_page.items()):
        lines = pages.get(page)
        marker = next((i for i in its if i["role"] == "marker"), None)
        off = _offset(marker, lines) if (lines is not None and marker) else None
        if off is None or lines is None:
            lost_pages.append(page)
            continue
        for it in its:
            if it["role"] == "marker":
                continue
            got = match_lines(it, lines, *off)
            rows.append({**it, "got": got, "exact": norm(got) == norm(it["text"]),
                         "cer": cer(it["text"], got), "level": has_level_word(got)})
    return {"rows": rows, "lost_pages": lost_pages}


def _rate(rs: list[dict[str, Any]], key: str) -> str:
    if not rs:
        return "-"
    return f"{sum(1 for r in rs if r[key]) / len(rs) * 100:.1f}% ({sum(1 for r in rs if r[key])}/{len(rs)})"


def report(result: dict[str, Any], title: str) -> str:
    rows = result["rows"]
    out = [f"# {title}", ""]
    if result["lost_pages"]:
        out += [f"표지를 읽지 못해 뺀 페이지: {len(result['lost_pages'])}개 {result['lost_pages'][:20]}", ""]
    ks = sorted({r["k"] for r in rows})
    out += ["## 배율별 요약", "", "| 배율(px/단위) | 이름 정확 | 이름 평균 CER | 레벨 줄 인식 | 레벨 줄 정확 | 지역 정확 |",
            "|---|---|---|---|---|---|"]
    for k in ks:
        nm = [r for r in rows if r["k"] == k and r["role"] == "name"]
        inf = [r for r in rows if r["k"] == k and r["role"] == "info"]
        zn = [r for r in rows if r["k"] == k and r["role"] == "zone"]
        mean_cer = sum(r["cer"] for r in nm) / len(nm) * 100 if nm else 0
        out.append(f"| {k:g} | {_rate(nm, 'exact')} | {mean_cer:.1f}% | {_rate(inf, 'level')} | "
                   f"{_rate(inf, 'exact')} | {_rate(zn, 'exact')} |")
    out += ["", "## 이름 종류별 정확도 (배율별)", "", "| 종류 | " + " | ".join(f"{k:g}" for k in ks) + " |",
            "|---|" + "---|" * len(ks)]
    for kind in sorted({r["tag"] for r in rows if r["role"] == "name"}):
        cells = [_rate([r for r in rows if r["k"] == k and r["role"] == "name" and r["tag"] == kind], "exact")
                 for k in ks]
        out.append(f"| {kind} | " + " | ".join(cells) + " |")
    out += ["", "## 직업별 레벨 줄 인식 (전체 배율)", "", "| 직업 | 레벨 단어 인식 | 줄 정확 |", "|---|---|---|"]
    for tag in sorted({r["tag"] for r in rows if r["role"] == "info"}):
        rs = [r for r in rows if r["role"] == "info" and r["tag"] == tag]
        out.append(f"| {tag} | {_rate(rs, 'level')} | {_rate(rs, 'exact')} |")
    subs: Counter[tuple[str, str]] = Counter()
    for r in rows:
        if r["role"] == "name" and not r["exact"]:
            subs.update(_subs(r["text"], r["got"]))
    out += ["", "## 이름에서 자주 틀린 글자 (정답 → 읽은 값)", ""]
    out += [f"- {a} → {b}: {n}회" for (a, b), n in subs.most_common(40)]
    out += ["", "## 틀린 이름 예시 (배율 1 부근)", ""]
    near = min(ks, key=lambda k: abs(k - 1.0)) if ks else 1.0
    bad = [r for r in rows if r["role"] == "name" and r["k"] == near and not r["exact"]]
    out += [f"- [{r['tag']}] {r['text']} → {r['got'] or '(못 읽음)'}" for r in bad[:60]]
    return "\n".join(out) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("sv")
    ap.add_argument("captures")
    ap.add_argument("out")
    ap.add_argument("--helper", default=str(TOOL / "helper" / "SkuLoginSense.exe"))
    ap.add_argument("--extra", default="")
    ap.add_argument("--title", default="캐릭터 선택 화면 OCR 측정")
    a = ap.parse_args()
    items = parse_truth(Path(a.sv).read_text(encoding="utf-8"))
    cache = Path(a.out).with_suffix(".ocr.json")
    pages: dict[int, list[dict[str, Any]]] = {}
    for png in sorted(Path(a.captures).glob("p_*.png")):
        res = run_helper(Path(a.helper), png, a.extra.split())
        pages[int(png.stem.split("_")[1])] = res.get("lines", [])
    cache.write_text(json.dumps({str(k): v for k, v in pages.items()}, ensure_ascii=False), encoding="utf-8")
    result = evaluate(items, pages)
    Path(a.out).write_text(report(result, a.title), encoding="utf-8")
    Path(a.out).with_suffix(".rows.json").write_text(
        json.dumps(result["rows"], ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"{len(result['rows'])} rows, lost pages {len(result['lost_pages'])} -> {a.out}")


if __name__ == "__main__":
    main()

"""WoW Login Tool 한국어 문자열의 평가 묶음을 만들고, 확정 번역을 반영한다.

대상
- logintool/data/localization/koKR.txt: "영어 키==한국어" 줄. id 는 "koKR.txt::<키>".
- logintool/v2/includes/forever.ahk: 툴이 직접 말하는 낱말. Map("de", .., "en", .., "fr", .., "ko", ..)
  의 "ko" 값과 "ko_button". id 는 "forever.ahk::<영어>".
  화면 판별 문구("login_button", Map(...) 꼴)와 경험 사전 설정 카드(gFvPresetCards)는 게임 화면 글자와
  같아야 하는 값이라 번역 평가에서 뺀다.

사용:
  uv run python -m tools.logintool_loc export <출력 폴더> [--size 110]
  uv run python -m tools.logintool_loc apply <ko.tsv>      # id, ko 열
  uv run python -m tools.logintool_loc sandbox <격리 폴더> <묶음.json> <정답표 출력.json> <출처=심을목록.json>...
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any

from tools.locale_lib import KO_WORK_ROOT, REPO_ROOT

LOGINTOOL = KO_WORK_ROOT / "Sku-WoW-Addon-TBC" / "logintool"
LOC_DIR = LOGINTOOL / "data" / "localization"
FOREVER_AHK = LOGINTOOL / "v2" / "includes" / "forever.ahk"
REFS = ("deDE", "frFR", "esES", "ruRU")

_ANCHOR = re.compile(r'^\s*"\w+",\s*Map\(')
_MAP = re.compile(r"Map\(((?:\s*\"[a-z]{2}\",\s*\"(?:[^\"\\]|\\.)*\",?)+)\s*\)")
_PAIR = re.compile(r'"([a-z]{2})",\s*"((?:[^"\\]|\\.)*)"')
_BUTTON = re.compile(r'"(\w\w)_button",\s*"((?:[^"\\]|\\.)*)"')


def parse_txt(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in text.lstrip("﻿").splitlines():
        if "==" in line:
            key, value = line.split("==", 1)
            out.setdefault(key, value)
    return out


def forever_items(src: str) -> list[dict[str, str]]:
    items: dict[str, dict[str, str]] = {}
    buttons: dict[str, str] = {}
    for line in src.splitlines():
        for lang, word in _BUTTON.findall(line):
            buttons[lang] = word
        if _ANCHOR.match(line):
            continue
        for m in _MAP.finditer(line):
            vals = dict(_PAIR.findall(m.group(1)))
            if "en" in vals and "ko" in vals:
                items.setdefault(vals["en"], {"id": f"forever.ahk::{vals['en']}", "key": vals["en"], "en": vals["en"],
                                              "de": vals.get("de", ""), "fr": vals.get("fr", ""), "ko": vals["ko"]})
    out = list(items.values())
    if "ko" in buttons:
        out.append({"id": "forever.ahk::Button", "key": "Button", "en": buttons.get("en", "Button"),
                    "de": buttons.get("de", ""), "fr": buttons.get("fr", ""), "ko": buttons["ko"]})
    return out


def apply_forever(src: str, changes: dict[str, str]) -> str:
    known = {i["id"] for i in forever_items(src)}
    unknown = set(changes) - known
    if unknown:
        raise KeyError(f"forever.ahk 에 없는 id: {sorted(unknown)}")
    lines = src.split("\n")
    for n, line in enumerate(lines):
        if _ANCHOR.match(line):
            continue
        for item_id, ko in changes.items():
            en = item_id.split("::", 1)[1]
            # replacement text for re.sub: group 1, then the quoted value (backslashes escaped for re)
            repl = r"\g<1>" + '"' + ko.replace('"', '`"').replace("\\", "\\\\") + '"'
            if item_id == "forever.ahk::Button":
                line = re.sub(r'("ko_button",\s*)"(?:[^"\\]|\\.)*"', repl, line)
                continue
            if f'"en", "{en}"' in line:
                line = re.sub(r'(Map\([^)]*"en", "' + re.escape(en) + r'"[^)]*"ko", )"(?:[^"\\]|\\.)*"', repl, line)
        lines[n] = line
    return "\n".join(lines)


def apply_txt(raw: bytes, changes: dict[str, str]) -> bytes:
    text = raw.decode("utf-8")
    nl = "\r\n" if "\r\n" in text else "\n"
    keys = {i.split("::", 1)[1]: v for i, v in changes.items() if i.startswith("koKR.txt::")}
    out, seen = [], set()
    for line in text.split(nl):
        bare = line.lstrip("﻿")
        if "==" in bare:
            key = bare.split("==", 1)[0]
            if key in keys and key not in seen:
                line = line[: len(line) - len(bare)] + key + "==" + keys[key]
                seen.add(key)
        out.append(line)
    missing = set(keys) - seen
    if missing:
        raise KeyError(f"koKR.txt 에 없는 키: {sorted(missing)}")
    return nl.join(out).encode("utf-8")


def _game_terms() -> dict[str, list[str]]:
    en_path, ko_path = REPO_ROOT / "cache" / "gs_enUS.csv", REPO_ROOT / "cache" / "gs_koKR.csv"
    if not en_path.exists() or not ko_path.exists():
        return {}

    def load(p: Path) -> dict[str, str]:
        with p.open(encoding="utf-8", newline="") as f:
            return {r["BaseTag"]: r["TagText_lang"] for r in csv.DictReader(f)}

    en, ko = load(en_path), load(ko_path)
    out: dict[str, list[str]] = defaultdict(list)
    for tag, text in en.items():
        k = ko.get(tag, "")
        if k and k not in out[text.strip().lower()]:
            out[text.strip().lower()].append(k)
    return out


def _code_index() -> list[tuple[str, int, str]]:
    idx = []
    for p in sorted((LOGINTOOL / "v2").rglob("*.ahk")):
        for n, line in enumerate(p.read_text(encoding="utf-8-sig", errors="replace").splitlines(), 1):
            idx.append((p.relative_to(LOGINTOOL).as_posix(), n, line.strip()))
    data = LOGINTOOL / "data" / "data.ini"
    if data.exists():
        for n, line in enumerate(data.read_text(encoding="utf-16", errors="replace").splitlines(), 1):
            idx.append(("data/data.ini", n, line.strip()))
    return idx


def _usages(idx: list[tuple[str, int, str]], key: str, limit: int = 6) -> list[str]:
    q = f'"{key}"'.lower()
    word = re.compile(r"(?<![\w])" + re.escape(key.lower()) + r"(?![\w])")
    hits = [f"{f}:{n}: {t[:200]}" for f, n, t in idx if q in t.lower()]
    if not hits:
        hits = [f"{f}:{n}: {t[:200]}" for f, n, t in idx if f.endswith(".ini") and word.search(t.lower())]
    return hits[:limit]


def collect() -> list[dict[str, Any]]:
    en = parse_txt((LOC_DIR / "enEN.txt").read_text(encoding="utf-8"))
    ko = parse_txt((LOC_DIR / "koKR.txt").read_text(encoding="utf-8"))
    refs = {r: parse_txt((LOC_DIR / f"{r}.txt").read_text(encoding="utf-8")) for r in REFS}
    terms = _game_terms()
    idx = _code_index()
    items: list[dict[str, Any]] = []
    for key, ko_text in ko.items():
        en_text = en.get(key, key)
        items.append({"id": f"koKR.txt::{key}", "file": "koKR.txt", "key": key, "en": en_text, "ko": ko_text,
                      **{r[:2]: refs[r].get(key, "") for r in REFS},
                      "code": _usages(idx, key), "game_term": " | ".join(terms.get(en_text.strip().lower(), [])[:4]),
                      "related": [], "shared_key": []})
    for it in forever_items(FOREVER_AHK.read_text(encoding="utf-8")):
        items.append({**it, "file": "forever.ahk", "code": _usages(idx, it["en"]),
                      "game_term": " | ".join(terms.get(it["en"].strip().lower(), [])[:4]),
                      "related": [], "shared_key": []})
    return items


def build_sandbox(root: Path, batch: dict[str, Any], seeded: dict[str, str], *,
                  logintool_dir: Path, work_dir: Path) -> None:
    """평가 구조 검증용 격리 폴더. 평가자는 이 폴더만 본다(tools/review/sandbox.py 의 로그인 툴판).

    들어가는 것: 오류를 심은 묶음, 프롬프트·스키마, 번역 지침·결정·용어집, 게임 문자열, 오류를 심은
    로그인 툴 사본(v2, data). 들어가지 않는 것: 원래 번역, 정답표, 평가 기록(reviews).
    """
    from tools.review.sandbox import WORK_FILES

    if root.exists():
        shutil.rmtree(root)
    work = root / "wowwork"
    for rel in WORK_FILES:
        src = work_dir / rel
        if src.exists():
            (work / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, work / rel)
    shutil.copytree(work_dir / "tools" / "review" / "prompts", work / "tools" / "review" / "prompts")
    for schema in (work_dir / "tools" / "review").glob("*.schema.json"):
        shutil.copy2(schema, work / "tools" / "review" / schema.name)
    lt = root / "wowvision-ko" / "Sku-WoW-Addon-TBC" / "logintool"
    for part in ("v2", "data"):
        shutil.copytree(logintool_dir / part, lt / part, ignore=shutil.ignore_patterns("screenshots", "settings.ini"))
    txt = lt / "data" / "localization" / "koKR.txt"
    txt.write_bytes(apply_txt(txt.read_bytes(), {k: v for k, v in seeded.items() if k.startswith("koKR.txt::")}))
    fv_seeds = {k: v for k, v in seeded.items() if k.startswith("forever.ahk::")}
    if fv_seeds:
        fv = lt / "v2" / "includes" / "forever.ahk"
        fv.write_text(apply_forever(fv.read_text(encoding="utf-8"), fv_seeds), encoding="utf-8", newline="")
    (root / "batch.json").write_text(json.dumps(batch, ensure_ascii=False, indent=1), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("export")
    e.add_argument("out", type=Path)
    e.add_argument("--size", type=int, default=110)
    a_ = sub.add_parser("apply")
    a_.add_argument("tsv", type=Path)
    s = sub.add_parser("sandbox")
    s.add_argument("root", type=Path)
    s.add_argument("batch", type=Path)
    s.add_argument("key_out", type=Path)
    s.add_argument("sources", nargs="+")
    a = ap.parse_args()
    if a.cmd == "sandbox":
        from tools.review.seed import apply_seeds, merge_seeds

        seeds = merge_seeds({n: Path(p) for n, p in (x.split("=", 1) for x in a.sources)})
        batch = json.loads(a.batch.read_text(encoding="utf-8"))
        answers = apply_seeds(batch, seeds)
        build_sandbox(a.root, batch, {i: v[0] for i, v in seeds.items()}, logintool_dir=LOGINTOOL, work_dir=REPO_ROOT)
        a.key_out.write_text(json.dumps(answers, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{len(answers)}개 심음 -> {a.root}")
        return
    if a.cmd == "export":
        items = collect()
        a.out.mkdir(parents=True, exist_ok=True)
        parts = [items[i : i + a.size] for i in range(0, len(items), a.size)]
        for n, part in enumerate(parts, 1):
            (a.out / f"batch-{n:02d}.json").write_text(
                json.dumps({"items": part}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{len(items)}개 항목 -> {a.out} ({len(parts)}개 묶음)")
        return
    with a.tsv.open(encoding="utf-8", newline="") as f:
        changes = {r["id"]: r["ko"] for r in csv.DictReader(f, delimiter="\t")}
    txt = LOC_DIR / "koKR.txt"
    txt.write_bytes(apply_txt(txt.read_bytes(), changes))
    fv = {k: v for k, v in changes.items() if k.startswith("forever.ahk::")}
    if fv:
        FOREVER_AHK.write_text(apply_forever(FOREVER_AHK.read_text(encoding="utf-8"), fv), encoding="utf-8",
                               newline="")
    print(f"반영: koKR.txt {sum(k.startswith('koKR.txt::') for k in changes)}개, forever.ahk {len(fv)}개")


if __name__ == "__main__":
    main()

"""WoW Login Tool 한국어 문자열에 확정 번역을 반영한다.

대상
- logintool/data/localization/koKR.txt: "영어 키==한국어" 줄. id 는 "koKR.txt::<키>".
- logintool/v2/includes/forever.ahk: 툴이 직접 말하는 낱말. Map("de", .., "en", .., "fr", .., "ko", ..)
  의 "ko" 값과 "ko_button". id 는 "forever.ahk::<영어>".
  화면 판별 문구("login_button", Map(...) 꼴)와 경험 사전 설정 카드(gFvPresetCards)는 게임 화면 글자와
  같아야 하는 값이라 번역 평가에서 뺀다.

사용:
  uv run python -m tools.logintool_loc apply <ko.tsv>      # id, ko 열
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

from tools.locale_lib import KO_WORK_ROOT

LOGINTOOL = KO_WORK_ROOT / "Sku-WoW-Addon-TBC" / "logintool"
LOC_DIR = LOGINTOOL / "data" / "localization"
FOREVER_AHK = LOGINTOOL / "v2" / "includes" / "forever.ahk"

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


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a_ = sub.add_parser("apply")
    a_.add_argument("tsv", type=Path)
    a = ap.parse_args()
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

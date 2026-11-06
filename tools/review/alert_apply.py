"""2026-11-07 사용자 결정(alert=알림, Buffered=모아 말하기)을 koKR 반영 목록(apply.tsv)으로 만든다.

사용: uv run python -m tools.review.alert_apply <apply.tsv 출력>
영어에 alert가 있는 키는 한국어의 "경보"를 "알림"으로 바꾼다. 영어에 alert가 없는데 "경보"를 쓰는 키가
있으면 멈춘다(그 키는 다른 뜻일 수 있어 사람이 봐야 한다).
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

from tools.locale_lib import KOKR_DIR, parse_locale_file, upstream_locale_dir

FIXED = {("speech.lua", "Buffered"): "모아 말하기"}


def plan(en: dict[tuple[str, str], str], ko: dict[tuple[str, str], str]) -> tuple[list[list[str]], list[str]]:
    rows, odd = [], []
    for (file, key), value in sorted(ko.items()):
        if (file, key) in FIXED:
            rows.append([file, key, value, FIXED[(file, key)]])
        elif "경보" in value:
            if re.search(r"alert", en.get((file, key), ""), re.IGNORECASE):
                rows.append([file, key, value, value.replace("경보", "알림")])
            else:
                odd.append(f"{file}::{key} = {value}")
    return rows, odd


def main() -> int:
    en_dir = upstream_locale_dir() / "enUS"
    en = {(p.name, k): v for p in en_dir.glob("*.lua") for k, v in parse_locale_file(p).items()}
    ko = {(p.name, k): v for p in KOKR_DIR.glob("*.lua") for k, v in parse_locale_file(p).items()}
    rows, odd = plan(en, ko)
    if odd:
        print("영어에 alert가 없는데 경보를 쓰는 키:\n" + "\n".join(odd), file=sys.stderr)
        return 1
    with Path(sys.argv[1]).open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["file", "key", "en", "ko"])  # en 열에는 바뀌기 전 번역 (tools.review.decisions 형식)
        w.writerows(rows)
    print(f"{len(rows)}건 -> {sys.argv[1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""enUS 원문 중 게임 GlobalStrings 와 정확히 일치하는 문자열의 공식 koKR 번역을 뽑는다.

출처: wago.tools db2 GlobalStrings (리테일). 결과는 cache/game_terms.tsv.
같은 영어 문구에 한국어가 여러 개면 전부 나열한다(번역 시 문맥으로 고른다).
"""

from __future__ import annotations

import csv
import sys
import urllib.request
from collections import defaultdict

from tools.locale_lib import REPO_ROOT, parse_locale_file, upstream_locale_dir

CACHE = REPO_ROOT / "cache"
URL = "https://wago.tools/db2/GlobalStrings/csv?locale={loc}"


def load(loc: str) -> dict[str, str]:
    path = CACHE / f"gs_{loc}.csv"
    if not path.exists():
        CACHE.mkdir(exist_ok=True)
        req = urllib.request.Request(URL.format(loc=loc), headers={"User-Agent": "wowwork-locale"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            path.write_bytes(resp.read())
    csv.field_size_limit(sys.maxsize)
    with path.open(encoding="utf-8", newline="") as f:
        return {row["BaseTag"]: row["TagText_lang"] for row in csv.DictReader(f)}


def by_text(en: dict[str, str], ko: dict[str, str]) -> dict[str, list[str]]:
    """영어 문구(소문자) → 공식 한국어 목록(처음 나온 순서, 중복 없음). 로그인 툴 묶음도 이것을 쓴다."""
    out: dict[str, list[str]] = defaultdict(list)
    for tag, text in en.items():
        k = ko.get(tag, "").strip()
        if k and k not in out[text.strip().lower()]:
            out[text.strip().lower()].append(k)
    return out


def main() -> None:
    terms = by_text(load("enUS"), load("koKR"))

    rows = []
    for path in sorted((upstream_locale_dir() / "enUS").glob("*.lua")):
        for key, val in parse_locale_file(path).items():
            hits = terms.get(val.strip().lower())
            if hits:
                rows.append((path.name, key, val, " | ".join(sorted(hits))))

    out = CACHE / "game_terms.tsv"
    with out.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f, delimiter="\t").writerows([("file", "key", "en", "ko"), *rows])
    print(f"{len(rows)} matches -> {out}")


if __name__ == "__main__":
    main()

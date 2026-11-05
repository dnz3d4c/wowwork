"""평가용 묶음 JSON 을 만든다. 항목마다 원문·번역·코드에서 쓰이는 곳·게임 공식 용어 후보를 담는다.

사용: uv run python -m tools.review.build_batch <출력폴더> [--keys 키목록.tsv] [--size 100]
--keys 는 file, key 열을 가진 TSV(예: cache/missing.tsv). 없으면 전체 문자열.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from tools.locale_lib import REPO_ROOT, WOWVISION_DIR, parse_locale_file, upstream_locale_dir
from tools.sync_locale import lua_quote

Index = list[tuple[str, int, str]]
SKIP_DIRS = {"locale", "libs", "externals", "mapdata", ".git"}


def collect_items(locale_dir: Path, only: set[tuple[str, str]] | None = None) -> list[dict[str, str]]:
    items = []
    for en_path in sorted((locale_dir / "enUS").glob("*.lua")):
        ko_path = locale_dir / "koKR" / en_path.name
        ko = parse_locale_file(ko_path) if ko_path.exists() else {}
        for key, en in parse_locale_file(en_path).items():
            if only is not None and (en_path.name, key) not in only:
                continue
            items.append(
                {
                    "id": f"{en_path.name}::{key}",
                    "file": en_path.name,
                    "key": key,
                    "en": en,
                    "ko": ko.get(key, ""),
                }
            )
    return items


def index_sources(root: Path) -> Index:
    idx: Index = []
    for path in sorted(root.rglob("*.lua")):
        rel = path.relative_to(root)
        if SKIP_DIRS & set(rel.parts):
            continue
        for n, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if 'L["' in line:
                idx.append((rel.as_posix(), n, line.strip()))
    return idx


def code_usages(idx: Index, key: str, limit: int = 4) -> list[str]:
    needle = f"L[{lua_quote(key)}]"
    return [f"{rel}:{n}: {text[:200]}" for rel, n, text in idx if needle in text][:limit]


def chunk(items: list, size: int) -> list[list]:  # type: ignore[type-arg]
    return [items[i : i + size] for i in range(0, len(items), size)]


def load_terms() -> dict[str, str]:
    path = REPO_ROOT / "cache" / "game_terms.tsv"
    if not path.exists():
        return {}
    with path.open(encoding="utf-8", newline="") as f:
        return {r["key"]: r["ko"] for r in csv.DictReader(f, delimiter="\t")}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("out", type=Path)
    ap.add_argument("--keys", type=Path)
    ap.add_argument("--size", type=int, default=100)
    a = ap.parse_args()
    only = None
    if a.keys:
        with a.keys.open(encoding="utf-8", newline="") as f:
            only = {(r["file"], r["key"]) for r in csv.DictReader(f, delimiter="\t")}
    items = collect_items(upstream_locale_dir(), only)
    idx = index_sources(WOWVISION_DIR)
    terms = load_terms()
    for item in items:
        item["code"] = code_usages(idx, item["key"])  # type: ignore[assignment]
        item["game_term"] = terms.get(item["key"], "")
    a.out.mkdir(parents=True, exist_ok=True)
    for n, part in enumerate(chunk(items, a.size), 1):
        (a.out / f"batch-{n:02d}.json").write_text(
            json.dumps({"items": part}, ensure_ascii=False, indent=1), encoding="utf-8"
        )
    print(f"{len(items)}개 항목 -> {a.out} ({len(chunk(items, a.size))}개 묶음)")


if __name__ == "__main__":
    main()

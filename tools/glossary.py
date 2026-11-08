"""확정 용어집(docs/glossary.tsv) 검사. 영어에 용어가 있으면 한국어에 정해진 번역이 들어 있어야 한다.

용어집 열: en(영어 용어, 복수형 s 허용), ko(번역, `|`로 대체 표기), except(예외 항목 id, `;` 구분), note

항목 id: koKR 은 `<파일>::<키>`, 설명서는 `manual::<상대경로>`(파일 단위로 검사). 예외 id 끝의 `*`는
접두 일치다(`manual::*`는 설명서 전체).
"""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import NamedTuple

from tools.locale_lib import REPO_ROOT

GLOSSARY_TSV = REPO_ROOT / "docs" / "glossary.tsv"


class Term(NamedTuple):
    en: str
    ko: tuple[str, ...]
    except_ids: frozenset[str]
    note: str


def load_glossary(path: Path = GLOSSARY_TSV) -> list[Term]:
    with path.open(encoding="utf-8", newline="") as f:
        return [
            Term(
                r["en"],
                tuple(s.strip() for s in r["ko"].split("|")),
                frozenset(s.strip() for s in r["except"].split(";") if s.strip()),
                r["note"],
            )
            for r in csv.DictReader(f, delimiter="\t")
        ]


def _excepted(item_id: str, except_ids: frozenset[str]) -> bool:
    return item_id in except_ids or any(e.endswith("*") and item_id.startswith(e[:-1]) for e in except_ids)


def violations(terms: list[Term], entries: dict[tuple[str, str], tuple[str, str]]) -> list[str]:
    """entries: (file, key) → (영어 값, 한국어 값)."""
    out = []
    for term in terms:
        pat = re.compile(r"\b" + re.escape(term.en) + r"s?\b", re.IGNORECASE)
        for (file, key), (en, ko) in entries.items():
            item_id = f"{file}::{key}"
            if _excepted(item_id, term.except_ids) or not pat.search(en):
                continue
            if not any(alt in ko for alt in term.ko):
                out.append(f"{item_id}: {term.en!r} -> {'|'.join(term.ko)!r} 없음 ({ko[:60]!r})")
    return out

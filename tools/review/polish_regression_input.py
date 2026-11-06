"""다듬기 회귀 확인 입력: 평가 입력(원문, 번역문, 용어표)에 다듬기 전후로 바뀐 줄을 더한다.

사용: uv run python -m tools.review.polish_regression_input <상대경로> <다듬기 전 커밋> <출력.json>
"""

from __future__ import annotations

import difflib
import json
import subprocess
import sys
from pathlib import Path

from tools.locale_lib import WOWVISION_DIR
from tools.manual import EN_ROOT, KO_ROOT, locale_pairs, term_sheet


def changed_lines(old: str, new: str) -> list[dict[str, str]]:
    a, b = old.splitlines(), new.splitlines()
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag != "equal":
            out.append({"before": "\n".join(a[i1:i2]), "after": "\n".join(b[j1:j2])})
    return out


def main() -> int:
    rel, base, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    old = subprocess.run(
        ["git", "-C", str(WOWVISION_DIR), "show", f"{base}:docs/src/user/ko/{rel}"],
        capture_output=True, text=True, encoding="utf-8", check=True,
    ).stdout  # fmt: skip
    en = (EN_ROOT / rel).read_text(encoding="utf-8")
    ko = (KO_ROOT / rel).read_text(encoding="utf-8")
    batch = {
        "file": rel,
        "en": en,
        "ko": ko,
        "terms": term_sheet(en, locale_pairs()),
        "changes": changed_lines(old, ko),
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(batch, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{rel}: 바뀐 곳 {len(batch['changes'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

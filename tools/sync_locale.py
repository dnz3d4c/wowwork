"""enUS 원문을 틀로 koKR 파일을 다시 만든다. upstream 을 업데이트한 뒤 실행한다.

사용: uv run python -m tools.sync_locale [번역.tsv]

- 줄 순서·주석·빈 줄은 enUS 를 따른다. 기존 번역 줄은 키로 찾아 그대로 옮긴다.
- 원문에서 사라진 키는 빠진다.
- 새 키의 번역은 TSV(열: file, key, en, ko)에서 채운다.
- 번역이 없는 키가 하나라도 있으면 아무 파일도 쓰지 않고 cache/missing.tsv 에
  빈 ko 열을 가진 목록을 만든다. ko 열을 채워 그 파일을 인자로 다시 실행한다.
- koKR/modules.xml 은 enUS/modules.xml 을 그대로 복사한다.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

from tools.locale_lib import KOKR_DIR, REPO_ROOT, parse_locale_file, unescape, upstream_locale_dir

HEADER = 'local L = LibStub("AceLocale-3.0"):NewLocale("WowVision", "koKR")\nif not L then return end\n'
MISSING_TSV = REPO_ROOT / "cache" / "missing.tsv"
_HEADER_LINE = re.compile(r"^(local L = .*|if not L then return end)$")
_KEY = re.compile(r'^L\["((?:[^"\\]|\\.)*)"\] = ')


def lua_quote(s: str) -> str:
    escaped = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")
    return f'"{escaped}"'


def rebuild(en_text: str, ko_text: str | None, new: dict[str, str]) -> tuple[str, list[str]]:
    """koKR 파일 내용과 번역이 없는 키 목록(enUS 순서)을 돌려준다."""
    ko_lines: dict[str, str] = {}
    for line in (ko_text or "").splitlines():
        m = _KEY.match(line)
        if m:
            ko_lines[unescape(m.group(1))] = line
    out: list[str] = []
    missing: list[str] = []
    for line in en_text.splitlines():
        if _HEADER_LINE.match(line):
            continue
        m = _KEY.match(line)
        if not m:
            out.append(line)
            continue
        key = unescape(m.group(1))
        if key in ko_lines:
            out.append(ko_lines[key])
        elif key in new:
            out.append(f'L["{m.group(1)}"] = {lua_quote(new[key])}')
        else:
            missing.append(key)
    return HEADER + "\n".join(out) + "\n", missing


def read_tsv(path: Path) -> dict[str, dict[str, str]]:
    """file → {key: ko}. ko 가 빈 줄은 무시한다."""
    result: dict[str, dict[str, str]] = {}
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["ko"]:
                result.setdefault(row["file"], {})[row["key"]] = row["ko"]
    return result


def main(argv: list[str]) -> int:
    new = read_tsv(Path(argv[0])) if argv else {}
    en_dir = upstream_locale_dir() / "enUS"
    outputs: dict[Path, str] = {}
    rows: list[list[str]] = []
    for en_path in sorted(en_dir.glob("*.lua")):
        ko_path = KOKR_DIR / en_path.name
        ko_text = ko_path.read_text(encoding="utf-8") if ko_path.exists() else None
        text, missing = rebuild(en_path.read_text(encoding="utf-8"), ko_text, new.get(en_path.name, {}))
        outputs[ko_path] = text
        en = parse_locale_file(en_path)
        rows += [[en_path.name, key, en[key], ""] for key in missing]
    if rows:
        MISSING_TSV.parent.mkdir(exist_ok=True)
        with MISSING_TSV.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter="\t", lineterminator="\n")
            writer.writerow(["file", "key", "en", "ko"])
            writer.writerows(rows)
        print(f"번역 없는 키 {len(rows)}개 -> {MISSING_TSV} (파일은 쓰지 않음)")
        return 1
    changed = [
        p.name for p, text in outputs.items() if not p.exists() or p.read_text(encoding="utf-8") != text
    ]
    for path, text in outputs.items():
        path.write_text(text, encoding="utf-8", newline="\n")
    xml = (en_dir / "modules.xml").read_text(encoding="utf-8")
    (KOKR_DIR / "modules.xml").write_text(xml, encoding="utf-8", newline="\n")
    stale = sorted({p.name for p in KOKR_DIR.glob("*.lua")} - {p.name for p in outputs})
    print(f"변경된 파일 {len(changed)}개: {', '.join(changed)}")
    if stale:
        print(f"enUS 에 없는 koKR 파일(직접 확인 후 삭제): {', '.join(stale)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

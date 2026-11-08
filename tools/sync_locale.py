"""enUS 원문을 틀로 koKR 파일을 다시 만든다. vision-locale 에 upstream 을 병합한 뒤 실행한다.

사용: uv run python -m tools.sync_locale [번역.tsv]

- 줄 순서·주석·빈 줄은 enUS 를 따른다. 기존 번역 줄은 키로 찾아 그대로 옮긴다.
- 원문에서 사라진 키는 빠진다.
- 키는 그대로인데 영어 값이 바뀐 키는 다시 번역해야 하는 키로 취급한다.
  비교 기준은 마지막으로 성공한 동기화 때의 enUS 값(state/enUS.tsv)이다.
- 새 키와 바뀐 키의 번역은 TSV(열: file, key, en, ko)에서 채운다.
- 번역이 없는 키가 하나라도 있으면 아무 파일도 쓰지 않고 cache/missing.tsv 에
  빈 ko 열을 가진 목록을 만든다(바뀐 키는 old_en 열에 이전 영어 값). ko 열을 채워 다시 실행한다.
- koKR/modules.xml 은 enUS/modules.xml 을 그대로 복사한다.
- 파일은 전부 임시 파일에 먼저 쓴 뒤 교체한다. 쓰기 하나가 실패하면 아무 파일도 바뀌지 않는다.
"""

from __future__ import annotations

import csv
import os
import re
import sys
from pathlib import Path

from tools.locale_lib import KOKR_DIR, REPO_ROOT, parse_locale_file, unescape, upstream_locale_dir

HEADER = 'local L = LibStub("AceLocale-3.0"):NewLocale("WowVision", "koKR")\nif not L then return end\n'
MISSING_TSV = REPO_ROOT / "cache" / "missing.tsv"
SNAPSHOT_TSV = REPO_ROOT / "state" / "enUS.tsv"
_HEADER_LINE = re.compile(r"^(local L = .*|if not L then return end)$")
_KEY = re.compile(r'^L\["((?:[^"\\]|\\.)*)"\] = ')

Snapshot = dict[tuple[str, str], str]


def lua_quote(s: str) -> str:
    escaped = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")
    return f'"{escaped}"'


def rebuild(
    en_text: str, ko_text: str | None, new: dict[str, str], changed: set[str] | None = None
) -> tuple[str, list[str]]:
    """koKR 파일 내용과 번역이 없는 키 목록(enUS 순서)을 돌려준다.

    changed 의 키는 기존 번역을 버리고 new 에서만 채운다.
    """
    changed = changed or set()
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
        if key in new:
            out.append(f'L["{m.group(1)}"] = {lua_quote(new[key])}')
        elif key in ko_lines and key not in changed:
            out.append(ko_lines[key])
        else:
            missing.append(key)
    return HEADER + "\n".join(out) + "\n", missing


def changed_keys(snapshot: Snapshot, file: str, en: dict[str, str]) -> set[str]:
    """스냅숏에 있던 키 중 영어 값이 달라진 키."""
    return {k for k, v in en.items() if (file, k) in snapshot and snapshot[(file, k)] != v}


def load_snapshot(path: Path) -> Snapshot:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8", newline="") as f:
        return {(r["file"], r["key"]): r["en"] for r in csv.DictReader(f, delimiter="\t")}


def save_snapshot(path: Path, data: Snapshot) -> None:
    path.parent.mkdir(exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(["file", "key", "en"])
        writer.writerows([file, key, en] for (file, key), en in sorted(data.items()))


def write_all(outputs: dict[Path, str]) -> None:
    """전부 임시 파일에 쓴 다음 교체한다. 임시 파일 단계에서 실패하면 원본은 그대로다."""
    temps: list[tuple[Path, Path]] = []
    try:
        for path, text in outputs.items():
            tmp = path.with_name(path.name + ".tmp")
            temps.append((tmp, path))
            tmp.write_text(text, encoding="utf-8", newline="\n")
    except OSError:
        for tmp, _ in temps:
            tmp.unlink(missing_ok=True)
        raise
    for tmp, path in temps:
        os.replace(tmp, path)


def read_tsv(path: Path) -> dict[str, dict[str, str]]:
    """file → {key: ko}. ko 가 빈 줄은 무시한다."""
    result: dict[str, dict[str, str]] = {}
    with path.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            if row["ko"]:
                result.setdefault(row["file"], {})[row["key"]] = row["ko"]
    return result


def unknown_rows(new: dict[str, dict[str, str]], en: dict[str, dict[str, str]]) -> list[tuple[str, str]]:
    """반영 목록에 있지만 enUS 에 없는 (파일, 키). 이런 줄은 반영되지 않으므로 알려야 한다."""
    return sorted((f, k) for f, keys in new.items() for k in keys if k not in en.get(f, {}))


def main(argv: list[str]) -> int:
    new = read_tsv(Path(argv[0])) if argv else {}
    en_dir = upstream_locale_dir() / "enUS"
    unknown = unknown_rows(new, {p.name: parse_locale_file(p) for p in en_dir.glob("*.lua")})
    if unknown:
        print(f"enUS 에 없는 파일·키 {len(unknown)}개라 반영할 수 없음(파일은 쓰지 않음): {unknown}")
        return 1
    snapshot = load_snapshot(SNAPSHOT_TSV)
    current: Snapshot = {}
    outputs: dict[Path, str] = {}
    rows: list[list[str]] = []
    for en_path in sorted(en_dir.glob("*.lua")):
        ko_path = KOKR_DIR / en_path.name
        ko_text = ko_path.read_text(encoding="utf-8") if ko_path.exists() else None
        en = parse_locale_file(en_path)
        current.update({(en_path.name, k): v for k, v in en.items()})
        changed = changed_keys(snapshot, en_path.name, en)
        text, missing = rebuild(
            en_path.read_text(encoding="utf-8"), ko_text, new.get(en_path.name, {}), changed
        )
        outputs[ko_path] = text
        rows += [[en_path.name, k, en[k], "", snapshot.get((en_path.name, k), "")] for k in missing]
    if rows:
        MISSING_TSV.parent.mkdir(exist_ok=True)
        with MISSING_TSV.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter="\t", lineterminator="\n")
            writer.writerow(["file", "key", "en", "ko", "old_en"])
            writer.writerows(rows)
        print(f"번역 없는 키 {len(rows)}개 -> {MISSING_TSV} (파일은 쓰지 않음)")
        return 1
    changed_files = [
        p.name for p, text in outputs.items() if not p.exists() or p.read_text(encoding="utf-8") != text
    ]
    KOKR_DIR.mkdir(exist_ok=True)
    outputs[KOKR_DIR / "modules.xml"] = (en_dir / "modules.xml").read_text(encoding="utf-8")
    write_all(outputs)
    save_snapshot(SNAPSHOT_TSV, current)
    stale = sorted({p.name for p in KOKR_DIR.glob("*.lua")} - {p.name for p in outputs})
    print(f"변경된 파일 {len(changed_files)}개: {', '.join(changed_files)}")
    if stale:
        print(f"enUS 에 없는 koKR 파일(직접 확인 후 삭제): {', '.join(stale)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

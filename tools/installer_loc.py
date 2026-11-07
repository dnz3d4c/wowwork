"""설치 프로그램(wowvision-installer) Loc.cs 의 한국어 표를 만든다.

영어 표(En)를 틀로 삼아 줄 순서·주석·정렬을 그대로 따르고 값만 한국어로 바꾼 Ko 표를
마지막 언어 표 뒤에 넣는다(이미 있으면 교체). 키가 하나라도 빠지면 쓰지 않는다.

사용:
  uv run python -m tools.installer_loc export <출력.tsv>   # key, en, de, fr, ko(현재 값) 목록
  uv run python -m tools.installer_loc apply <번역.tsv>    # ko 열로 Ko 표를 만들어 Loc.cs 에 쓴다
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

from tools.locale_lib import KO_WORK_ROOT

LOC_CS = KO_WORK_ROOT / "wowvision-installer" / "WowVisionInstaller" / "Loc.cs"
_ENTRY = re.compile(r'^(\s*\["([^"]+)"\]\s*=\s*)"((?:[^"\\]|\\.)*)"(,?)\s*$')
_ESC = {"n": "\n", "t": "\t", '"': '"', "\\": "\\"}


def unquote(s: str) -> str:
    return re.sub(r"\\(.)", lambda m: _ESC.get(m.group(1), "\\" + m.group(1)), s)


def cs_quote(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t") + '"'


def _block(text: str, name: str) -> tuple[int, int] | None:
    """`Dictionary<string, string> <name> = ...` 선언 줄 시작부터 닫는 `};` 줄 끝까지(앞의 주석은 제외)."""
    m = re.search(rf"^[^\n]*Dictionary<string, string> {name} = new[^\n]*\n", text, re.MULTILINE)
    if not m:
        return None
    end = text.index("\n        };\n", m.end()) + len("\n        };\n")
    return m.start(), end


def parse_table(text: str, name: str) -> dict[str, str]:
    span = _block(text, name)
    if span is None:
        return {}
    out = {}
    for line in text[span[0] : span[1]].splitlines():
        m = _ENTRY.match(line)
        if m:
            out[m.group(2)] = unquote(m.group(3))
    return out


def apply_ko(text: str, ko: dict[str, str]) -> tuple[str, list[str]]:
    en_span = _block(text, "En")
    if en_span is None:
        raise ValueError("En 표를 찾지 못했다")
    en_lines = text[en_span[0] : en_span[1]].splitlines(keepends=True)
    missing = [m.group(2) for line in en_lines if (m := _ENTRY.match(line)) and m.group(2) not in ko]
    if missing:
        return text, missing
    out_lines = []
    for line in en_lines:
        m = _ENTRY.match(line)
        if m:
            out_lines.append(f"{m.group(1)}{cs_quote(ko[m.group(2)])}{m.group(4)}\n")
        else:
            out_lines.append(line.replace("> En = new", "> Ko = new"))
    block = "".join(out_lines)
    header = "\n        // ── Korean ───────────────────────────────────────────────────────────\n" \
             "        // Same key set as En/De/Fr, same house rule.\n"  # fmt: skip
    ko_span = _block(text, "Ko")
    if ko_span is not None:
        return text[: ko_span[0]] + block + text[ko_span[1] :], []
    last = max((s for s in (_block(text, n) for n in ("En", "De", "Fr")) if s), key=lambda s: s[1])
    return text[: last[1]] + header + block + text[last[1] :], []


PAYLOAD = KO_WORK_ROOT / "wowvision-installer" / "WowVisionInstaller" / "payload" / "koKR.zip"


def build_payload(kokr_dir: Path, out: Path) -> int:
    """koKR 폴더를 `koKR/<파일>` 항목으로 묶는다. 날짜를 고정해 같은 입력이면 같은 바이트가 나온다."""
    import zipfile

    files = sorted(p for p in kokr_dir.iterdir() if p.is_file())
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            info = zipfile.ZipInfo(f"koKR/{p.name}", date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, p.read_bytes())
    return len(files)


VOICE_PAYLOAD = PAYLOAD.with_name("koVoice.zip")
VOICE_PACK = Path(__file__).resolve().parent.parent / "assets" / "voice" / "Yuna"


def build_voice_payload(pack_dir: Path, out: Path) -> int:
    """음성 팩 폴더를 `<팩 이름>/<하위폴더>/<파일>` 항목으로 묶는다. 날짜를 고정해 같은 입력이면 같은 바이트가 나온다."""
    import zipfile

    files = sorted(p for p in pack_dir.rglob("*") if p.is_file())
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            info = zipfile.ZipInfo(
                f"{pack_dir.name}/{p.relative_to(pack_dir).as_posix()}", date_time=(2026, 1, 1, 0, 0, 0)
            )
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, p.read_bytes())
    return len(files)


def installer_items(src_dir: Path) -> list[dict[str, object]]:
    """평가 묶음 항목: 원문·번역·다른 언어 번역, 코드에서 키를 쓰는 줄(Loc.cs 제외)."""
    text = (src_dir / "Loc.cs").read_text(encoding="utf-8")
    tables = {n: parse_table(text, n) for n in ("En", "De", "Fr", "Ko")}
    code_lines = [
        (p.relative_to(src_dir).as_posix(), n, line.strip())
        for p in sorted(src_dir.rglob("*.cs"))
        if p.name != "Loc.cs"
        for n, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1)
        if "Loc." in line
    ]
    items: list[dict[str, object]] = []
    for key, en in tables["En"].items():
        needle = f'"{key}"'
        items.append({
            "id": f"Loc.cs::{key}", "file": "Loc.cs", "key": key, "en": en,
            "ko": tables["Ko"].get(key, ""), "de": tables["De"].get(key, ""), "fr": tables["Fr"].get(key, ""),
            "code": [f"{rel}:{n}: {t[:200]}" for rel, n, t in code_lines if needle in t][:6],
            "game_term": "", "related": [], "shared_key": [],
        })  # fmt: skip
    return items


def main() -> int:
    cmd = sys.argv[1]
    if cmd == "payload":  # vision-locale 의 koKR 을 설치 프로그램 payload 로
        from tools.locale_lib import KOKR_DIR

        n = build_payload(KOKR_DIR, PAYLOAD)
        print(f"koKR 파일 {n}개 -> {PAYLOAD}")
        n = build_voice_payload(VOICE_PACK, VOICE_PAYLOAD)
        print(f"음성 팩 파일 {n}개 -> {VOICE_PAYLOAD}")
        return 0
    path = Path(sys.argv[2])
    if cmd == "batch":
        import json

        items = installer_items(LOC_CS.parent)
        path.mkdir(parents=True, exist_ok=True)
        for n in range(0, len(items), 70):
            (path / f"batch-{n // 70 + 1:02d}.json").write_text(
                json.dumps({"items": items[n : n + 70]}, ensure_ascii=False, indent=1), encoding="utf-8"
            )
        print(f"{len(items)}개 항목 -> {path}")
        return 0
    text = LOC_CS.read_text(encoding="utf-8")
    if cmd == "export":
        tables = {n: parse_table(text, n) for n in ("En", "De", "Fr", "Ko")}
        with path.open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerow(["key", "en", "de", "fr", "ko"])
            for key, en in tables["En"].items():
                w.writerow(
                    [key, en, tables["De"].get(key, ""), tables["Fr"].get(key, ""), tables["Ko"].get(key, "")]
                )
        print(f"{len(tables['En'])}개 -> {path}")
        return 0
    with path.open(encoding="utf-8", newline="") as f:
        ko = {r["key"]: r["ko"] for r in csv.DictReader(f, delimiter="\t") if r["ko"]}
    out, missing = apply_ko(text, ko)
    if missing:
        print(f"번역 없는 키 {len(missing)}개, 쓰지 않음: {missing[:10]}")
        return 1
    LOC_CS.write_bytes(
        out.encode("utf-8-sig") if LOC_CS.read_bytes().startswith(b"\xef\xbb\xbf") else out.encode()
    )
    print(f"Ko 표 {len(ko)}개 -> {LOC_CS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

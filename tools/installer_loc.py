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
VOICE_PAYLOAD = PAYLOAD.with_name("koVoice.zip")
VOICE_PACK = Path(__file__).resolve().parent.parent / "assets" / "voice" / "Yuna"
LOGINTOOL_PAYLOAD = PAYLOAD.with_name("koLoginTool.zip")
LOGINTOOL_REPO = KO_WORK_ROOT / "Sku-WoW-Addon-TBC"
LOGINTOOL_DIR = LOGINTOOL_REPO / "logintool"
HELPER_PROJECT = LOGINTOOL_DIR / "helper" / "SkuLoginSense" / "SkuLoginSense.csproj"
HELPER_BUILD = HELPER_PROJECT.parent / "bin" / "Release" / "net48"
# scoop 은 dotnet SDK 의 shim 을 깔지 않아 PATH 로는 닿지 않는다(~/.claude/CLAUDE.md 환경 표).
DOTNET = Path.home() / "scoop" / "apps" / "dotnet-sdk" / "current" / "dotnet.exe"
# 센스 리더 프록시: 소스는 korean 서브모듈(dnz3d4c/wowvision-korean), 서명 스크립트는 공유 브리지 payload 의 것.
SR_BRIDGE = KO_WORK_ROOT / "wowvision-installer" / "korean" / "sense-reader-bridge"
SR_PAYLOAD = PAYLOAD.with_name("koSenseReader.zip")
BRIDGE_PAYLOAD = PAYLOAD.with_name("sapi2sr-payload.zip")
SR_PIN_LABEL = "nvdaControllerClient.dll x64 (WowVision Korean Sense Reader proxy)"


def write_zip(entries: dict[str, bytes], out: Path) -> int:
    """항목 이름 순으로 묶는다. 날짜를 고정해 같은 입력이면 같은 바이트가 나온다."""
    import zipfile

    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(entries):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, entries[name])
    return len(entries)


def build_payload(kokr_dir: Path, out: Path) -> int:
    """koKR 폴더를 `koKR/<파일>` 항목으로 묶는다."""
    return write_zip({f"koKR/{p.name}": p.read_bytes() for p in kokr_dir.iterdir() if p.is_file()}, out)


def build_voice_payload(pack_dir: Path, out: Path) -> int:
    """음성 팩 폴더를 `<팩 이름>/<하위폴더>/<파일>` 항목으로 묶는다."""
    files = [p for p in pack_dir.rglob("*") if p.is_file()]
    return write_zip(
        {f"{pack_dir.name}/{p.relative_to(pack_dir).as_posix()}": p.read_bytes() for p in files}, out
    )


def logintool_entries(tool_dir: Path, helper_build: Path | None) -> dict[str, bytes]:
    """로그인 툴 한국어판에서 설치 프로그램이 원본 릴리스 위에 덮어쓸 파일(설치 폴더 기준 경로 → 내용).

    범위는 프로젝트 CLAUDE.md `## WoW Login Tool`의 테스트 폴더 복사 범위와 같다: v2/ 전체, data/*.ini,
    data/localization/, 다시 빌드한 helper/SkuLoginSense.exe. data/settings.ini 는 사용자 설정이라 넣지 않는다.
    helper_build 가 None 이면 도우미는 뺀다(낡았는지 검사할 때, exe 는 빌드마다 바이트가 다르다).
    """
    files = [p for p in (tool_dir / "v2").rglob("*") if p.is_file()]
    files += [p for p in (tool_dir / "data").glob("*.ini") if p.name != "settings.ini"]
    files += [p for p in (tool_dir / "data" / "localization").rglob("*") if p.is_file()]
    entries = {p.relative_to(tool_dir).as_posix(): p.read_bytes() for p in files}
    if helper_build is not None:
        for name in ("SkuLoginSense.exe", "SkuLoginSense.exe.config"):
            entries[f"helper/{name}"] = (helper_build / name).read_bytes()
    return entries


def build_logintool_payload(out: Path) -> int:
    """ko 브랜치의 로그인 툴로 payload 를 만든다. 다른 브랜치가 checkout 돼 있으면 만들지 않는다."""
    import subprocess

    branch = subprocess.run(
        ["git", "-C", str(LOGINTOOL_REPO), "branch", "--show-current"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    if branch != "ko":
        raise SystemExit(
            f"로그인 툴 저장소가 ko 가 아니라 {branch!r} 브랜치다. ko 를 checkout 한 뒤 다시 실행한다."
        )
    subprocess.run(
        [str(DOTNET), "build", "-c", "Release", str(HELPER_PROJECT), "-nologo", "-v", "q"], check=True
    )
    return write_zip(logintool_entries(LOGINTOOL_DIR, HELPER_BUILD), out)


def pin_sign_script(script: str, pe_hash_hex: str) -> str:
    """브리지 서명 스크립트의 고정 해시 표 맨 앞에 프록시의 해시를 더한다. 나머지는 그대로 둔다.

    스크립트는 고정 해시가 맞는 파일만 서명하므로, 프록시를 서명하려면 그 해시가 표에 있어야 한다.
    공유 payload(Sku 설치 프로그램과 같은 바이트)는 고치지 않고 빌드 때마다 여기서 만든다.
    """
    anchor = "$PinnedPeHashes = @{"
    at = script.index(anchor) + len(anchor)
    nl = "\r\n" if "\r\n" in script else "\n"
    pin = f"{nl}\t# WowVision Korean build: Sense Reader proxy (wowvision-korean sense-reader-bridge).{nl}\t'{pe_hash_hex}' = '{SR_PIN_LABEL}'"
    return script[:at] + pin + script[at:]


def pe_hash(dll: Path, sign_script: Path) -> str:
    """서명 스크립트의 Pin 모드로 Authenticode PE 해시를 구한다(서명 여부와 무관한 해시)."""
    import re
    import subprocess

    out = subprocess.run(
        ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(sign_script),
         "-Mode", "Pin", "-DllPaths", str(dll)],
        capture_output=True, text=True, check=True,
    ).stdout  # fmt: skip
    m = re.search(r"'([0-9A-F]{64})'", out)
    if not m:
        raise RuntimeError(f"PE 해시를 얻지 못했다: {out!r}")
    return m.group(1)


def build_sense_reader_payload(out: Path) -> int:
    """프록시를 빌드하고 테스트를 돌린 뒤, 프록시와 해시를 더한 서명 스크립트를 묶는다."""
    import subprocess
    import tempfile
    import zipfile

    subprocess.run(["cmd", "/c", str(SR_BRIDGE / "build.bat"), "test"], check=True)
    dll = SR_BRIDGE / "out" / "nvdaControllerClient.dll"
    with zipfile.ZipFile(BRIDGE_PAYLOAD) as z:
        raw = z.read("sku-nvda-voice-sign.ps1")
    with tempfile.TemporaryDirectory() as tmp:
        sku_script = Path(tmp) / "sku-nvda-voice-sign.ps1"
        sku_script.write_bytes(raw)
        script = pin_sign_script(raw.decode("utf-8-sig"), pe_hash(dll, sku_script))
    encoded = script.encode("utf-8-sig" if raw.startswith(b"\xef\xbb\xbf") else "utf-8")
    return write_zip({"nvdaControllerClient.dll": dll.read_bytes(), "sign.ps1": encoded}, out)


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
        n = build_logintool_payload(LOGINTOOL_PAYLOAD)
        print(f"로그인 툴 한국어판 파일 {n}개 -> {LOGINTOOL_PAYLOAD}")
        n = build_sense_reader_payload(SR_PAYLOAD)
        print(f"센스 리더 프록시 파일 {n}개 -> {SR_PAYLOAD}")
        return 0
    path = Path(sys.argv[2])
    if cmd == "batch":
        from tools.review.build_batch import write_batches

        items = installer_items(LOC_CS.parent)
        print(f"{len(items)}개 항목 -> {path} ({write_batches(items, path, 70)}개 묶음)")
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

"""회귀 확인 결과를 재처리 Workflow 입력으로 바꾼다.

prepare <workflow 출력> <결과 폴더> <args 파일>
    통과하지 못한 파일마다 <결과 폴더>/<파일>/refix-input.json 을 만들고,
    Workflow에 넘길 짧은 args(파일과 ref·합의 여부·회사)를 <args 파일>에 쓴다.
judge <결과 폴더> <파일> <ref> [<ref> ...]
    refix-input.json 과 refix-rebut.json 에서 반박된 ref만 골라
    GPT 판정 입력(refix-judge-gpt-input.json)을 만든다.
"""

import json
import sys
from pathlib import Path


def _norm(s: str) -> str:
    return " ".join(s.split())


def overlaps(a: str, b: str) -> bool:
    x, y = _norm(a), _norm(b)
    return bool(x) and bool(y) and (x in y or y in x)


def build_items(rel: str, blocking: list[dict]) -> list[dict]:
    items = [{**f, "ref": f"{rel}#reg-{f['by']}-{i}"} for i, f in enumerate(blocking)]
    for f in items:
        f["consensus"] = any(g["by"] != f["by"] and overlaps(f["quote"], g["quote"]) for g in items)
    return items


def prepare(src: Path, out_dir: Path, args_path: Path) -> int:
    failed = json.loads(src.read_text(encoding="utf-8"))["result"]["failed"]
    files = []
    for entry in failed:
        if not entry["blocking"]:
            continue
        rel = entry["file"]
        items = build_items(rel, entry["blocking"])
        d = out_dir / rel.removesuffix(".md")
        d.mkdir(parents=True, exist_ok=True)
        (d / "refix-input.json").write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
        # by: 지적마다 c(claude)/g(gpt), agree: 지적마다 1(두 회사 합의)/0. ref는 Workflow가 파일과 순번으로 다시 만든다.
        files.append({"file": rel, "by": "".join(f["by"][0] for f in items),
                      "agree": "".join("1" if f["consensus"] else "0" for f in items)})  # fmt: skip
    args_path.write_text(
        json.dumps({"outDir": out_dir.as_posix(), "items": files}, ensure_ascii=False), encoding="utf-8"
    )
    print(f"파일 {len(files)}개, 지적 {sum(len(f['by']) for f in files)}건")
    return 0


def load_rebut(path: Path) -> dict[str, dict]:
    """번역자 반박 파일을 ref별로 읽는다. 형식이 틀리거나 ref가 겹치면 ValueError."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    # 번역자 에이전트가 {"responses": [...]} 대신 배열만 저장하는 경우가 있다(2026-11-06 windows/character.md).
    entries = raw.get("responses") if isinstance(raw, dict) else raw
    if not isinstance(entries, list):
        raise ValueError(f"{path}: responses 배열이 없음")  # noqa: TRY004 - 인자 타입이 아니라 파일 내용 형식 오류
    out: dict[str, dict] = {}
    for e in entries:
        if not (
            isinstance(e, dict)
            and isinstance(e.get("ref"), str)
            and e.get("action") in ("applied", "dispute")
        ):
            raise ValueError(f"{path}: 형식이 틀린 응답 {e!r}")
        if e["ref"] in out:
            raise ValueError(f"{path}: ref 중복 {e['ref']}")
        out[e["ref"]] = e
    return out


def judge(out_dir: Path, rel: str, refs: list[str]) -> int:
    d = out_dir / rel.removesuffix(".md")
    items = {f["ref"]: f for f in json.loads((d / "refix-input.json").read_text(encoding="utf-8"))}
    rebut = load_rebut(d / "refix-rebut.json")
    keys = ("category", "severity", "quote", "suggestion", "problem", "evidence")
    payload = [
        {"ref": r, "file": rel, "finding": {k: items[r][k] for k in keys}, "translator": rebut.get(r)}
        for r in refs
    ]
    data = {"file": rel, "en_path": f"wowvision-ko/WowVision/docs/src/user/en/{rel}",
            "ko_path": f"wowvision-ko/WowVision/docs/src/user/ko/{rel}", "items": payload}  # fmt: skip
    (d / "refix-judge-gpt-input.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(d / "refix-judge-gpt-input.json")
    return 0


def main() -> int:
    cmd, rest = sys.argv[1], sys.argv[2:]
    if cmd == "prepare":
        return prepare(Path(rest[0]), Path(rest[1]), Path(rest[2]))
    if cmd == "judge":
        return judge(Path(rest[0]), rest[1], rest[2:])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())

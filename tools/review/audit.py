"""평가자가 격리 폴더 밖에 접근했는지 감사한다.

사용: uv run python -m tools.review.audit <격리폴더> <기록 파일 또는 폴더>...
- codex 이벤트 기록(gpt_review --events 로 남긴 JSONL): 실행한 명령(command_execution)을 검사한다.
- Claude 에이전트 기록(agent-*.jsonl): 첫 프롬프트에 "번역 평가자"가 든 기록만, 도구 호출 입력을 검사한다.
밖을 가리키는 경로가 하나라도 있으면 종료 코드 1.
"""

from __future__ import annotations

import json
import re
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from tools.review.guard import foreign_paths

REVIEWER_MARK = "번역 평가자"
# codex 가 명령마다 앞에 붙이는 셸 실행 파일 같은 시스템 경로는 접근으로 보지 않는다.
# 경로 정규식이 공백에서 끊으므로 "C:\Program Files\..."는 "C:/Program"으로 잡힌다.
SYSTEM_PREFIXES = ("c:/program", "c:/windows")
_ESCAPE = re.compile(r"\S*\.\.[\\/]\S*")


def suspicious(text: str, root: str) -> list[str]:
    """격리 폴더 밖 절대 경로와 상위 폴더 이동(../)."""
    found = [p for p in foreign_paths(text, root) if not p.lower().startswith(SYSTEM_PREFIXES)]
    found += [f"상위 폴더 이동: {m.group(0)}" for m in _ESCAPE.finditer(text)]
    return found


def _walk_strings(obj: Any) -> Iterator[str]:
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _walk_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk_strings(v)


def codex_commands(lines: list[str]) -> list[str]:
    out = []
    for line in lines:
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        item = ev.get("item") or {}
        if item.get("type") == "command_execution" and item.get("command"):
            out.append(str(item["command"]))
    return out


def claude_tool_inputs(lines: list[str]) -> list[str] | None:
    """평가자 기록이면 도구 호출 입력 문자열들, 아니면 None."""
    records = []
    for line in lines:
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    first_user = next((r for r in records if r.get("type") == "user"), None)
    if first_user is None or REVIEWER_MARK not in json.dumps(first_user, ensure_ascii=False):
        return None
    out: list[str] = []
    for r in records:
        content = (r.get("message") or {}).get("content")
        if r.get("type") == "assistant" and isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    out.extend(_walk_strings(block.get("input")))
    return out


def audit(root: str, paths: list[Path]) -> dict[str, list[str]]:
    report: dict[str, list[str]] = {}
    files = [f for p in paths for f in (sorted(p.rglob("*.jsonl")) if p.is_dir() else [p])]
    for f in files:
        lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        strings = claude_tool_inputs(lines) if f.name.startswith("agent-") else codex_commands(lines)
        if strings is None:
            continue
        found = [p for s in strings for p in suspicious(s, root)]
        report[str(f)] = sorted(set(found))
    return report


def main() -> int:
    root, paths = sys.argv[1], [Path(p) for p in sys.argv[2:]]
    report = audit(root, paths)
    bad = {k: v for k, v in report.items() if v}
    print(f"감사한 기록 {len(report)}개, 밖 접근 {len(bad)}개")
    for k, v in bad.items():
        print(f"  {k}: {v[:5]}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

"""GPT(codex exec) 평가자 하나를 실행한다. 읽기 전용 샌드박스, 출력은 스키마를 따르는 JSON.

사용: uv run python -m tools.review.gpt_review --prompt a.md [--prompt b.md ...] --batch b.json
        --schema findings.schema.json --out out.json
--prompt 파일들을 순서대로 이어 붙이고, 마지막에 묶음 JSON 을 붙여 stdin 으로 넘긴다.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from tools.locale_lib import REPO_ROOT


def build_prompt(prompts: list[Path], batch: Path) -> str:
    parts = [p.read_text(encoding="utf-8") for p in prompts]
    parts.append("## 입력\n\n```json\n" + batch.read_text(encoding="utf-8") + "\n```\n")
    return "\n\n".join(parts)


def build_command(out: Path, schema: Path, cwd: Path) -> list[str]:
    return [
        "codex", "exec", "--profile", "review_strict", "--ephemeral", "--skip-git-repo-check",
        "--sandbox", "read-only", "--cd", str(cwd), "-c", "model_reasoning_effort=medium",
        "--output-schema", str(schema), "-o", str(out), "-",
    ]  # fmt: skip


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", type=Path, action="append", required=True)
    ap.add_argument("--batch", type=Path, required=True)
    ap.add_argument("--schema", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    exe = shutil.which("codex")
    if exe is None:
        print("codex 를 찾지 못했다", file=sys.stderr)
        return 2
    cmd = build_command(a.out, a.schema, REPO_ROOT.parent)
    cmd[0] = exe
    a.out.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        cmd, input=build_prompt(a.prompt, a.batch), text=True, encoding="utf-8",
        capture_output=True, timeout=1800, check=False,
    )  # fmt: skip
    if result.returncode != 0 or not a.out.exists():
        print(result.stderr[-3000:], file=sys.stderr)
        return 1
    print(a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())

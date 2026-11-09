"""원본에 낸 PR이 병합된 뒤 남은 브랜치를 지운다.

지우는 것은 우리 PR이 병합됐고, 브랜치 끝 커밋이 그 PR의 머리 커밋과 같거나 그 조상인 브랜치뿐이다.
그 내용은 원본의 PR 기록(refs/pull/N/head)에 남아서 GitHub PR 화면에서 브랜치를 되살릴 수 있다.
병합 없이 닫힌 PR과 병합 뒤 커밋이 더 생긴 브랜치는 지우지 않고 보고만 한다(사용자 확인 대상).
열린 PR의 브랜치, PR이 없는 브랜치, main·ko·master, 체크아웃된 브랜치는 보지 않는다.

대상: fork·origin 원격 브랜치와 로컬 브랜치. 다른 원격(upstream 등)은 건드리지 않는다.

    uv run python -m tools.pr_cleanup            # 지운다
    uv run python -m tools.pr_cleanup --dry-run  # 무엇을 지울지만 본다

`--hook`은 wowwork 세션 시작 훅(.claude/settings.json)이 부른다. 지운 브랜치와 확인이 필요한
브랜치, 처음 보는 병합 PR을 알리고, 아무 일도 없으면 침묵한다. 실패는 health `pr-cleanup`에 남긴다.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import NamedTuple, Protocol

if not __package__:  # 훅이 파일 경로로 실행하면 저장소 루트가 sys.path에 없다
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.locale_lib import KO_WORK_ROOT, REPO_ROOT

#: (로컬 복제본 폴더 이름, PR을 받는 원본 저장소)
REPOS = [("vision-locale", "wow-vision/vision-locale"), ("WowVision", "wow-vision/WowVision")]
PROTECTED = frozenset({"main", "master", "ko"})
CLEAN_REMOTES = ("fork", "origin")
TIMEOUT = 60
SEEN_PATH = REPO_ROOT / "cache" / "pr_cleanup_seen.json"
HEALTH_COMPONENT = "pr-cleanup"  # 훅 파일 이름(pr_cleanup)과 같으면 hook_runner가 실패 기록을 지운다
FOLLOW_UP = "후속 절차: CLAUDE.md `### PR이 병합된 뒤` 2~5단계"


class PR(NamedTuple):
    number: int
    ref: str
    sha: str
    state: str  # "open" | "closed"
    merged: bool
    title: str = ""


def decide(
    name: str, sha: str, prs: list[PR], is_ancestor: Callable[[str, str], bool]
) -> tuple[str, str] | None:
    """브랜치 하나의 처분. None이면 이 도구가 손대지도 알리지도 않는다."""
    if name in PROTECTED:
        return None
    mine = [p for p in prs if p.ref == name]
    if not mine or any(p.state == "open" for p in mine):
        return None
    for p in mine:
        if p.merged and is_ancestor(sha, p.sha):
            return ("delete", f"#{p.number} 병합됨")
    merged = [p for p in mine if p.merged]
    if merged:
        return ("keep", f"#{merged[0].number} 병합 뒤 커밋이 더 있음, 확인 필요")
    return ("keep", f"#{mine[0].number} 병합 없이 닫힘, 확인 필요")


def clean_remotes(remotes: list[str]) -> list[str]:
    return [r for r in remotes if r in CLEAN_REMOTES]


def _cmd(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), capture_output=True, text=True, encoding="utf-8", check=check, timeout=TIMEOUT
    )


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return _cmd("git", "-C", str(repo), *args, check=check)


def _my_prs(base: str, login: str) -> list[PR]:
    jq = (
        f'.[] | select(.user.login == "{login}") | '
        "{number, ref: .head.ref, sha: .head.sha, state, merged: (.merged_at != null), title}"
    )
    out = _cmd("gh", "api", "--paginate", f"repos/{base}/pulls?state=all&per_page=100", "--jq", jq)
    return [PR(**json.loads(line)) for line in out.stdout.splitlines() if line.strip()]


def _branches(repo: Path, prefix: str, strip: int) -> dict[str, str]:
    fmt = f"--format=%(symref) %(objectname) %(refname:lstrip={strip})"
    result = {}
    for line in _git(repo, "for-each-ref", fmt, prefix).stdout.splitlines():
        if line.startswith(" "):  # symref(origin/HEAD 등)는 첫 칸이 비어 있지 않다
            _, sha, name = line.split(" ", 2)
            result[name] = sha
    return result


def cleanup(repo: Path, base: str, login: str, dry_run: bool) -> tuple[list[str], dict[str, str]]:
    """(보고 줄, 병합된 우리 PR {"<폴더>#<번호>": 제목})"""
    remotes = clean_remotes(_git(repo, "remote").stdout.split())
    _git(repo, "fetch", "-q", "--prune", "--multiple", *remotes)
    prs = _my_prs(base, login)

    def is_ancestor(a: str, b: str) -> bool:
        return a == b or _git(repo, "merge-base", "--is-ancestor", a, b, check=False).returncode == 0

    current = _git(repo, "symbolic-ref", "-q", "--short", "HEAD", check=False).stdout.strip()
    targets: list[tuple[str | None, str, str]] = [
        (remote, name, sha)
        for remote in remotes
        for name, sha in _branches(repo, f"refs/remotes/{remote}", 3).items()
    ]
    targets += [
        (None, name, sha) for name, sha in _branches(repo, "refs/heads", 2).items() if name != current
    ]

    lines = []
    for remote, name, sha in targets:
        verdict = decide(name, sha, prs, is_ancestor)
        if verdict is None:
            continue
        action, reason = verdict
        where = f"{repo.name} {remote}/{name}" if remote else f"{repo.name} 로컬 {name}"
        if action == "delete" and not dry_run:
            if remote:
                _git(repo, "push", "-q", remote, "--delete", name)
            else:
                _git(repo, "branch", "-D", name)
        label = {"delete": "지울 것" if dry_run else "지움", "keep": "남김"}[action]
        lines.append(f"{label}: {where} ({reason})")
    merged = {f"{repo.name}#{p.number}": p.title for p in prs if p.merged}
    return lines, merged


def collect(dry_run: bool = False) -> tuple[list[str], dict[str, str]]:
    login = _cmd("gh", "api", "user", "--jq", ".login").stdout.strip()
    lines: list[str] = []
    merged: dict[str, str] = {}
    for folder, base in REPOS:
        more, m = cleanup(KO_WORK_ROOT / folder, base, login, dry_run)
        lines += more
        merged |= m
    return lines, merged


def describe(e: Exception) -> str:
    if isinstance(e, subprocess.CalledProcessError):
        tail = (e.stderr or "").strip().splitlines()[-1:] or [""]
        return f"{' '.join(map(str, e.cmd[:3]))} 종료 코드 {e.returncode}: {tail[0]}"
    if isinstance(e, subprocess.TimeoutExpired):
        return f"{' '.join(map(str, e.cmd[:3]))} {e.timeout:.0f}초 시간 초과"
    return f"{type(e).__name__}: {e}"


class Health(Protocol):
    def record_ok(self, component: str) -> None: ...
    def record_fail(self, component: str, error_tail: str, kind: str = ...) -> None: ...


def run_hook(
    collect_fn: Callable[[], tuple[list[str], dict[str, str]]], health: Health, seen_path: Path
) -> str:
    """세션 시작 훅 본체. 사용자에게 알릴 글(없으면 빈 문자열)을 돌려준다. 예외를 올리지 않는다."""
    try:
        lines, merged = collect_fn()
        seen = set(json.loads(seen_path.read_text(encoding="utf-8"))) if seen_path.exists() else None
        # 처음 실행에서는 이미 병합된 PR을 기록만 한다(후속 작업은 이미 끝났다)
        new = {} if seen is None else {k: t for k, t in merged.items() if k not in seen}
        seen_path.parent.mkdir(parents=True, exist_ok=True)
        seen_path.write_text(json.dumps(sorted((seen or set()) | merged.keys())), encoding="utf-8")
    except (subprocess.SubprocessError, OSError, ValueError) as e:
        desc = describe(e)
        health.record_fail(HEALTH_COMPONENT, desc)
        return f"[PR 정리] 실패: {desc}. 손으로 확인: uv run python -m tools.pr_cleanup --dry-run"
    health.record_ok(HEALTH_COMPONENT)
    if not lines and not new:
        return ""
    out = ["[PR 정리]"]
    out += [f"병합됨: {k} {t}" for k, t in new.items()]
    out += lines
    if new:
        out.append(FOLLOW_UP)
    return "\n".join(out)


class _NoHealth:
    def record_ok(self, component: str) -> None:
        pass

    def record_fail(self, component: str, error_tail: str, kind: str = "crash") -> None:
        pass


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    ap.add_argument("--dry-run", action="store_true", help="지우지 않고 무엇을 지울지만 보인다")
    ap.add_argument("--hook", action="store_true", help="세션 시작 훅으로 실행한다")
    args = ap.parse_args()
    if args.hook:
        try:
            import health_lib  # type: ignore[import-not-found]  # hook_runner가 ~/.claude/hooks를 sys.path에 넣는다

            health: Health = health_lib
        except ImportError:
            health = _NoHealth()
        text = run_hook(collect, health, SEEN_PATH)
        if text:
            print(text)
        return 0
    try:
        lines, _ = collect(args.dry_run)
    except (subprocess.SubprocessError, OSError) as e:
        print(f"실패: {describe(e)}", file=sys.stderr)
        return 1
    print("\n".join(lines) if lines else "정리할 PR 브랜치가 없다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

import subprocess

from tools.pr_cleanup import PR, clean_remotes, decide, run_hook

HEAD = "h" * 40


def same_or_listed(pairs: set[tuple[str, str]]):
    def is_ancestor(a: str, b: str) -> bool:
        return a == b or (a, b) in pairs

    return is_ancestor


NEVER = same_or_listed(set())


def test_merged_pr_branch_at_head_is_deleted():
    prs = [PR(66, "auction-scan-wording", HEAD, "closed", True)]
    assert decide("auction-scan-wording", HEAD, prs, NEVER) == ("delete", "#66 병합됨")


def test_branch_behind_merged_head_is_deleted():
    prs = [PR(66, "x", HEAD, "closed", True)]
    assert decide("x", "old", prs, same_or_listed({("old", HEAD)}))[0] == "delete"


def test_commits_after_merge_need_confirmation():
    prs = [PR(66, "x", HEAD, "closed", True)]
    action, reason = decide("x", "newer", prs, NEVER)
    assert action == "keep"
    assert "확인" in reason


def test_open_pr_branch_is_left_alone_silently():
    # 열린 PR은 확인할 일이 아니다. 매 세션 "남김"으로 보고하면 소음이 된다.
    prs = [PR(66, "x", HEAD, "closed", True), PR(80, "x", "other", "open", False)]
    assert decide("x", HEAD, prs, NEVER) is None


def test_closed_without_merge_needs_confirmation():
    prs = [PR(70, "x", HEAD, "closed", False)]
    action, reason = decide("x", HEAD, prs, NEVER)
    assert action == "keep"
    assert "#70" in reason


def test_branch_without_pr_is_ignored():
    prs = [PR(66, "x", HEAD, "closed", True)]
    assert decide("korean-locale", HEAD, prs, NEVER) is None


def test_protected_branch_is_ignored_even_if_pr_used_it():
    prs = [PR(66, "main", HEAD, "closed", True)]
    assert decide("main", HEAD, prs, NEVER) is None


def test_only_fork_and_origin_remotes_are_cleaned():
    assert clean_remotes(["origin", "upstream", "fork", "someone"]) == ["origin", "fork"]


class FakeHealth:
    def __init__(self):
        self.calls = []

    def record_ok(self, component):
        self.calls.append(("ok", component))

    def record_fail(self, component, error_tail, kind="crash"):
        self.calls.append(("fail", component, error_tail))


def test_hook_first_run_records_existing_merges_silently(tmp_path):
    state = tmp_path / "seen.json"
    health = FakeHealth()
    out = run_hook(lambda: ([], {"vision-locale#66": "old"}), health, state)
    assert out == ""
    assert health.calls == [("ok", "pr-cleanup")]
    out = run_hook(lambda: ([], {"vision-locale#66": "old"}), health, state)
    assert out == ""


def test_hook_announces_new_merge_once_even_without_branches(tmp_path):
    state = tmp_path / "seen.json"
    health = FakeHealth()
    run_hook(lambda: ([], {"vision-locale#66": "old"}), health, state)
    merged = {"vision-locale#66": "old", "WowVision#130": "nav: fix"}
    out = run_hook(lambda: (["지움: WowVision fork/x (#130 병합됨)"], merged), health, state)
    assert "WowVision#130 nav: fix" in out
    assert "지움: WowVision fork/x" in out
    assert "PR이 병합된 뒤" in out
    assert "#66" not in out.replace("지움", "")
    assert run_hook(lambda: ([], merged), health, state) == ""


def test_hook_repeats_branches_that_need_confirmation(tmp_path):
    state = tmp_path / "seen.json"
    line = "남김: WowVision fork/x (#130 병합 뒤 커밋이 더 있음, 확인 필요)"
    run_hook(lambda: ([line], {}), FakeHealth(), state)
    assert line in run_hook(lambda: ([line], {}), FakeHealth(), state)


def test_hook_failure_is_recorded_and_does_not_raise(tmp_path):
    def broken():
        raise subprocess.CalledProcessError(1, ["gh", "api"], stderr="HTTP 502")

    health = FakeHealth()
    out = run_hook(broken, health, tmp_path / "seen.json")
    assert "실패" in out
    assert health.calls[0][0:2] == ("fail", "pr-cleanup")
    assert "HTTP 502" in health.calls[0][2]


def test_hook_timeout_is_recorded(tmp_path):
    def slow():
        raise subprocess.TimeoutExpired(["git", "fetch"], 60)

    health = FakeHealth()
    run_hook(slow, health, tmp_path / "seen.json")
    assert health.calls[0][0:2] == ("fail", "pr-cleanup")

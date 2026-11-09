from tools.pr_cleanup import PR, decide

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


def test_open_pr_wins_over_earlier_merged_pr_with_same_name():
    prs = [PR(66, "x", HEAD, "closed", True), PR(80, "x", "other", "open", False)]
    assert decide("x", HEAD, prs, NEVER) == ("keep", "#80 열려 있음")


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

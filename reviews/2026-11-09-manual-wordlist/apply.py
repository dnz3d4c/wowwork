"""2026-11-09 낱말 치환 회귀 확인 반영. 두 회사가 함께 지적한 줄과, 한 회사만 지적했지만 영어 원문이
change 가 아닌(switch, replace, turn into, become, reforge into) 줄을 줄 단위로 바꾼다.

사용: uv run python -X utf8 reviews/2026-11-09-manual-wordlist/apply.py
"""

import json
from pathlib import Path

HERE = Path(__file__).parent
KO = HERE.parents[2] / "wowvision-ko" / "WowVision" / "docs" / "src" / "user" / "ko"

BOTH = {
    "windows/spells-and-talents.md:12", "windows/spells-and-talents.md:47", "windows/spells-and-talents.md:61",
    "information/buffers.md:35", "information/buffers.md:39", "information/buffers.md:116",
    "information/buffers.md:209", "information/buffers.md:210", "information/buffers.md:266",
    "information/buffers.md:350", "information/buffers.md:381", "getting-started/managing.md:29",
    "getting-started/installer.md:70", "information/monitors.md:106", "world/combat.md:133",
    "world/quests.md:139", "windows/professions.md:175", "windows/auction-house.md:198",
}
# 한 회사만 지적, 원문 낱말로 확인(괄호는 원문)
GPT_ONLY = {
    "basics/alerts.md:100",  # switch to
    "getting-started/sku-login.md:62",  # replaces the game fonts
    "information/monitors.md:64",  # switch every monitor
    "windows/group-finder.md:50",  # is replaced by
    "windows/overview.md:10",  # turns it into
    "windows/professions.md:133",  # stats you can reforge into
}
CLAUDE_ONLY = {
    "windows/auction-house.md:293",  # switches between
    "windows/character.md:143",  # switches the statistics between
    "windows/auction-house.md:59",  # is replaced by
    "controller.md:69",  # turns the D-pad into
    "windows/character.md:70",  # switch category
    "windows/social.md:86",  # Switch to the ignore list
}
# 원문 "become a count": 두 회사 수정안("개수로 전환") 대신 원문대로
MANUAL = {"world/combat.md:104": ("하나) 수로 변경됩니다.", "하나) 개수가 됩니다.")}


def load(name: str) -> dict[str, str]:
    data = json.loads((HERE / name).read_text(encoding="utf-8"))
    return {f["id"]: f["suggestion"] for f in data["findings"]}


def main() -> None:
    claude, gpt = load("claude.json"), load("gpt.json")
    plan: dict[str, str] = {}
    for i in BOTH | CLAUDE_ONLY:
        plan[i] = claude[i]
    for i in GPT_ONLY:
        plan[i] = gpt[i]
    files: dict[str, dict[int, str]] = {}
    for i, s in plan.items():
        rel, n = i.rsplit(":", 1)
        files.setdefault(rel, {})[int(n)] = s
    for rel, n_old_new in MANUAL.items():
        f, n = rel.rsplit(":", 1)
        p = KO / f
        lines = p.read_text(encoding="utf-8").split("\n")
        old, new = n_old_new
        assert lines[int(n) - 1].count(old) == 1, rel
        lines[int(n) - 1] = lines[int(n) - 1].replace(old, new)
        p.write_text("\n".join(lines), encoding="utf-8", newline="")
    for rel, edits in files.items():
        p = KO / rel
        lines = p.read_text(encoding="utf-8").split("\n")
        for n, s in edits.items():
            lines[n - 1] = s
        p.write_text("\n".join(lines), encoding="utf-8", newline="")
    print(len(plan) + len(MANUAL))


if __name__ == "__main__":
    main()

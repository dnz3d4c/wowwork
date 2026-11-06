"""테스터 설치 안내가 설치 프로그램의 선택 기능을 빠뜨리지 않는지 검사한다.

2026-11-06: 안내가 "평소처럼 설치합니다"라고만 해서 NVDA 브리지(구성 요소 페이지의
"WoW에서 NVDA를 음성으로 사용")를 설치하는 방법이 빠졌다. 첫 화면의 "지금 업데이트"는
권장 기본값으로 설치하므로 브리지가 들어가지 않는다. 안내를 원본 설명서에서 출발하지 않고
"한국어에서 달라진 점"만 적었기 때문이다.

옵션 목록은 손으로 적지 않고 ComponentsForm.cs 의 SetOptionText 호출에서 뽑는다. 원본에
옵션이 새로 생기면 이 검사가 저절로 실패해서 안내를 고치게 만든다.
"""

import re

from tools.installer_loc import LOC_CS, parse_table
from tools.locale_lib import REPO_ROOT

GUIDE = REPO_ROOT / "docs" / "tester-guide.md"
FORM = LOC_CS.parent / "ComponentsForm.cs"


def visible(label: str) -> str:
    """화면과 스크린리더가 말하는 글자. 단축키 표시 (&F)와 &를 뺀다."""
    return re.sub(r"\(&.\)", "", label).replace("&", "").strip()


def required_labels() -> dict[str, str]:
    ko = parse_table(LOC_CS.read_text(encoding="utf-8"), "Ko")
    keys = [
        f"opt.{k}.label"
        for k in re.findall(r'SetOptionText\([^,]+,[^,]+,\s*"(\w+)"\)', FORM.read_text(encoding="utf-8"))
    ]
    keys += ["update.customizeBtn", "managed.label"]
    return {k: visible(ko[k]) for k in keys}


def test_option_keys_are_found() -> None:
    labels = required_labels()
    assert "opt.sapi2sr.label" in labels
    assert len([k for k in labels if k.startswith("opt.")]) >= 5


def test_guide_names_every_installer_option() -> None:
    guide = GUIDE.read_text(encoding="utf-8")
    missing = {k: v for k, v in required_labels().items() if v not in guide}
    assert not missing, f"테스터 안내에 없는 설치 프로그램 문구: {missing}"


def test_guide_quotes_match_installer_text() -> None:
    """안내가 따옴표로 인용한 화면 문구는 설치 프로그램 Ko 표에 실제로 있어야 한다.

    2026-11-06 최종 검수에서 status.koreanFailed 문구가 바뀌었는데 안내는 옛 문구를 인용하고 있었다.
    """
    ko_text = " ".join(visible(v) for v in parse_table(LOC_CS.read_text(encoding="utf-8"), "Ko").values())
    quotes = re.findall(r'"([^"]+)"', GUIDE.read_text(encoding="utf-8"))
    stale = [q for q in quotes if q not in ko_text]
    assert not stale, f"설치 프로그램에 없는 인용 문구: {stale}"

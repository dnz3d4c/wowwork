"""koKR 값이 바뀌었을 때 한국어 설명서의 화면 문구 인용을 따라 바꾸는 도구.

2026-11-06: 바뀐 문구 54개를 설명서에 맞추면서 `world/combat.md`의 "제어됨" 3곳을
잘못 바꿨다. 바뀐 키는 targeting.lua "Controlled"였는데, 그 파일이 인용한 것은 값이 같은
다른 키 ui.lua "controlled"였다. 영어 설명서가 어느 키의 영어를 인용하는지 보고 판단한다.
"""

from tools.manual_sync import Change, sync_text


def test_short_value_replaced_only_when_quoted_and_en_quotes_key() -> None:
    ch = [Change(en="Disabled", old="비활성화", new="사용 안 함")]
    en = 'It reads "Disabled" when off.'
    ko = '꺼져 있으면 "비활성화"라고 읽습니다. 기능을 비활성화하려면'
    out, log = sync_text(ch, en, ko, others={})
    # 인용 뒤 "라고"는 받침과 무관하다. 본문 속 "비활성화하려면"은 인용이 아니라서 그대로다.
    assert out == '꺼져 있으면 "사용 안 함"라고 읽습니다. 기능을 비활성화하려면'
    assert len(log) == 1


def test_same_old_value_used_by_other_key_is_not_touched() -> None:
    """combat.md 사례: 원문이 다른 키("controlled")를 인용하면 바꾸지 않는다."""
    ch = [Change(en="Controlled", old="제어됨", new="군중 제어 중")]
    en = 'the count is followed by "controlled".'
    ko = '숫자 뒤에 "제어됨"이 붙습니다.'
    out, log = sync_text(ch, en, ko, others={"제어됨": ["controlled"]})
    assert out == ko
    assert log == []


def test_ambiguous_when_both_keys_quoted() -> None:
    ch = [Change(en="Controlled", old="제어됨", new="군중 제어 중")]
    en = 'It says "Controlled" here and "controlled" there.'
    ko = '여기서는 "제어됨", 저기서는 "제어됨".'
    out, log = sync_text(ch, en, ko, others={"제어됨": ["controlled"]})
    assert out == ko
    assert log and "판단 필요" in log[0]


def test_long_value_replaced_anywhere_when_en_present() -> None:
    old, new = "경매장 열리지 않음 상태", "경매장이 열려 있지 않은 상태"
    ch = [Change(en="Auction not open", old=old, new=new)]
    out, _ = sync_text(ch, "WowVision says Auction not open.", f"WowVision이 {old}라고 말합니다.", others={})
    assert new in out


def test_nothing_when_en_does_not_mention_key() -> None:
    ch = [Change(en="Disabled", old="비활성화", new="사용 안 함")]
    out, log = sync_text(ch, "No quote here.", '"비활성화"', others={})
    assert out == '"비활성화"' and log == []


def test_long_value_matches_en_case_insensitively() -> None:
    """quick-start.md 사례: 원문이 화면 이름을 문장 속 소문자로 쓴다("free bag slots")."""
    ch = [Change(en="Free Bag Slots", old="비어 있는 가방 칸", new="빈 가방 칸")]
    out, _ = sync_text(ch, "money, free bag slots, durability", "돈, 비어 있는 가방 칸, 내구도", others={})
    assert out == "돈, 빈 가방 칸, 내구도"


def test_running_twice_changes_nothing_when_new_contains_old() -> None:
    """옛 값이 새 값 안에 들어 있으면("…경로" → "…경로 안내") 두 번 돌려도 "안내 안내"가 되면 안 된다."""
    ch = [
        Change(
            en="Route to Target",
            old="대상까지 경로까지 이어지는 길",
            new="대상까지 경로까지 이어지는 길 안내",
        )
    ]
    en = "Route to Target"
    once, _ = sync_text(ch, en, "키: 대상까지 경로까지 이어지는 길.", others={})
    twice, log = sync_text(ch, en, once, others={})
    assert once == twice == "키: 대상까지 경로까지 이어지는 길 안내."
    assert log == []

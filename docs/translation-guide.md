# WowVision 한국어 번역 지침

WowVision 원문(`../wowvision-ko/vision-locale/enUS/*.lua`)을 같은 저장소의 `koKR/*.lua`로 번역할 때 따르는 규칙입니다. 번역 파일은 비공개 복제 저장소 `dnz3d4c/vision-locale`에 커밋하고, 이 저장소(wowwork)는 도구와 기록만 둡니다.

## 파일 형식

- 파일 이름은 enUS와 같습니다. 첫 두 줄은 반드시 다음과 같습니다.

```lua
local L = LibStub("AceLocale-3.0"):NewLocale("WowVision", "koKR")
if not L then return end
```

- enUS의 키를 하나도 빠짐없이, 같은 순서로 옮깁니다. `--` 주석 줄과 빈 줄도 원문 위치에 그대로 둡니다.
- 값은 항상 한국어 문자열입니다. `true`를 쓰지 않습니다. enUS가 `L["EditBox"] = "Edit"`처럼 값을 따로 가진 경우에는 키가 아니라 그 값을 번역합니다.
- 큰따옴표와 백슬래시는 Lua 규칙대로 이스케이프합니다.
- 검증: `uv run pytest -q`가 키 누락, 원문에 없는 키, 빈 값, 서식 지정자 불일치, Lua 문법 오류를 잡습니다.
- 같은 키는 파일이 달라도 번역이 하나입니다. AceLocale은 키 하나에 값 하나만 가지므로, 다른 파일에 이미 있는 키는 그 번역을 따릅니다. 예: `Direct`는 음성 방식(`speech.lua`)과 길 안내 창(`navigation.lua`)이 함께 사용하므로 둘 다 "직접"입니다.

## upstream 업데이트 절차

1. 원본 변경을 병합합니다: `git -C ../wowvision-ko/vision-locale pull upstream main`. 앱 코드 확인용으로 `git -C ../wowvision-ko/WowVision pull upstream main`도 실행합니다.
2. `uv run python -m tools.sync_locale`을 실행합니다. 번역이 없는 키가 있으면 파일을 쓰지 않고 `cache/missing.tsv`를 만듭니다.
3. `cache/missing.tsv`의 `ko` 열을 채운 뒤 `uv run python -m tools.sync_locale cache/missing.tsv`를 실행합니다. 줄 순서와 주석은 enUS를 따르고, 원문에서 사라진 키는 빠지며, `modules.xml`은 enUS 것을 복사합니다. 키는 그대로인데 영어 값이 바뀐 키도 `old_en` 열과 함께 이 목록에 올라옵니다. 비교 기준은 마지막 동기화 때의 영어 값(`state/enUS.tsv`)입니다.
4. `uv run python -m tools.game_terms`로 용어 목록을 업데이트하고 `uv run pytest -q`로 검증합니다.

## 서식 지정자

- `%s`, `%d` 같은 지정자는 개수와 종류를 원문과 똑같이 유지합니다.
- 한국어 어순 때문에 순서를 바꿔야 하면 `%2$s`처럼 위치 지정을 사용합니다(WoW의 `format`이 지원합니다).
- 숫자 사이의 `of`("1 of 5")는 영어 `of`를 그대로 둡니다. 코드가 이어 붙이는 `L["of"]`(2026-11-03)뿐 아니라 서식 문자열 안의 `of`(`Page %d of %d` → `페이지 %d of %d`)도 같습니다(2026-11-05 사용자 결정).
- 지정자 바로 뒤에 받침에 따라 달라지는 조사(을/를, 이/가, 은/는, 와/과, 으로/로)를 붙이지 않습니다. 문장 구조를 바꿔 피합니다. 예: `Whisper %s` → `%s에게 귓속말` (에게는 받침과 무관). 피할 수 없는 경우는 보고 목록에 올립니다.

## 용어

1. **인게임 용어가 최우선입니다.** `cache/game_terms.tsv`에는 원문 문자열과 정확히 일치하는 게임 GlobalStrings의 공식 한국어가 있습니다(출처: wago.tools, 리테일 클라이언트). 일치 항목은 이 번역을 사용합니다. 후보가 `|`로 여러 개이면 문맥에 맞는 것을 고릅니다.
2. 정확히 일치하지 않는 문구도 그 안의 게임 용어(창 이름, 직업, 자원, 아이템 품질, 경매 용어 등)는 공식 한국어를 사용합니다. 필요하면 `cache/gs_enUS.csv`와 `cache/gs_koKR.csv`를 `BaseTag`로 대조해서 찾습니다.
   **문맥이 우선입니다(2026-11-03 사용자 결정).** 같은 문맥(같은 창, 같은 기능)의 공식 번역이면 그대로 따릅니다. 영어 문자열만 같고 다른 문맥에서 온 일치 항목이면 문맥에 맞게 번역합니다. 예: Comment는 공식 "하실 말씀"이 아니라 "의견", Merchant는 "상품 목록"이 아니라 "상인"으로 옮깁니다.
   행동 단축바 계열은 모두 "단축바"로 통일합니다(태세 단축바, 게임패드 단축바).
3. 뜻이 애매하면 원본 코드에서 키가 어떻게 쓰이는지 확인합니다: `../wowvision-ko/WowVision` 아래에서 `L["키"]`를 검색합니다.
4. 고유 이름은 그대로 둡니다: WowVision, WowNav, WoW Forever, Battle.net, BattleTag.
5. 키보드 키 이름(Shift, Ctrl, Alt, Enter, Tab, Space 등)은 영어 그대로 둡니다.

## 문체

- 음성 알림과 상태 문구는 **짧은 명사형**으로 씁니다. 예: `combat started` → `전투 시작`, `combat ended` → `전투 종료`.
- 설정 이름과 메뉴 항목도 명사형입니다. 예: `Count Elite Enemies Only` → `정예 적만 세기`.
- 안내 문장(설명, 도움말)과 사용자에게 할 일을 지시하는 문장은 합니다체로 씁니다.
- 상태 알림은 원문이 마침표로 끝나는 완결 문장이어도 합니다체로 늘리지 않고 간결하게 씁니다. 원인과 결과는 "~해서 종료"처럼 잇습니다(2026-11-05 사용자 결정). 예: `Route ended outside the network's zones.` → "네트워크 지역 밖이라 경로 종료."
- 영어 복합어의 하이픈은 옮기지 않습니다. `Auto-move` → "자동 이동"(2026-11-05 사용자 결정).
- 컨트롤 종류 이름은 한국어로 옮깁니다. 예: Button → 버튼, Checkbox → 체크 상자, Dropdown → 드롭다운, Edit → 편집, Slider → 슬라이더.
- 원문의 대소문자 구분(`Combat`과 `combat`)은 한국어에서 의미가 없으므로 같은 번역을 사용해도 됩니다.
- 원문에 없는 기호를 추가하거나 원문 기호를 없애지 않습니다. 스크린리더 발음을 이유로 문구를 가공하지 않습니다.

## 보고 목록

번역하면서 아래에 해당하는 항목은 따로 모아 사용자 확인을 받습니다.

- 인게임 용어 후보가 여럿이라 고르기 애매한 것
- 조사 문제로 자연스러운 번역이 불가능한 것
- 원문 뜻을 확신하지 못한 것

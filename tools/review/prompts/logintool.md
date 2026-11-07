# 대상: WoW Login Tool 문자열

이번 입력은 WowVision 애드온 문자열이 아니라 WoW Login Tool(AutoHotkey v2 프로그램, `wowvision-ko/Sku-WoW-Addon-TBC/logintool/`)의 문구다. 툴은 게임 밖에서 로그인·캐릭터 선택·캐릭터 생성 화면을 다루고, 이 문구들을 툴의 음성(SAPI, 보통 SAPI2SR을 거쳐 스크린리더)으로 말한다. 위 공통 규칙 중 Lua·AceLocale에 관한 것은 그대로 적용하지 않고, 아래 규칙이 우선한다.

- 형식: `koKR.txt::<키>` 항목은 `data/localization/koKR.txt`의 `키==값` 줄이고 값만 번역이다. 키는 영어 그대로 둔다(코드가 키로 찾는다). `en` 필드는 `enEN.txt`의 영어 값이다. `forever.ahk::<영어>` 항목은 `v2/includes/forever.ahk` 안에서 툴이 조립해 말하는 낱말(색상 이름, 이름 확인 결과, 컨트롤 이름 등)이다.
- 입력에는 `de`, `fr`, `es`, `ru` 번역이 함께 있다. 뜻을 확인하는 참고 자료로만 쓴다.
- 서식 지정자는 없다. 대신 코드가 문자열을 이어 붙인다. 예: `Say(T("login mode for") " " T(gametype) ", " regionName ", " langName)`. `code` 필드와 코드 파일(`v2/includes/*.ahk`)을 보고 이어 붙인 결과가 한국어로 자연스러운지, 뒤에 붙는 말과 조사가 맞는지 확인한다. 색상 이름은 `FvColourName`이 톤·명도·색을 이어 붙인다.
- 종족, 직업, 성별, 시작 지역 이름은 `data/data.ini`의 영어 키(`human`, `night_elf`, `death_knight` 등)를 이 파일로 번역해서 말한다. 게임 공식 한국어(`game_term`, `cache/gs_koKR.csv`)와 같아야 한다.
- 게임 버전(게임 종류) 이름은 영어로 쓴다: Classic Era, Burning Crusade(Anniversary), Cataclysm Classic, Retail, WoW Forever. 설치 프로그램과 한국어 설명서가 영어 이름을 쓰기 때문이다(`docs/decisions.tsv` 2026-11-07 설명서 게임 버전 이름).
- 고유 이름은 그대로: Sku, Sku installer, WoW Login Tool, AutoHotkey, NVDA, SAPI, SAPI2SR, Battle.net, Discord, WowVision.
- 키보드 키 이름은 영어 그대로(Alt, Control, Shift, Enter, Escape, F1 등). 원문이 "Alt F1"처럼 쓰면 그 모양을 따른다.
- 화면에 표시되는 게임 버튼·창 이름을 가리키는 말은 게임 공식 한국어를 따른다(예: Enter World = 접속하기, Create Character = 캐릭터 생성).
- 문체는 번역 지침과 같다: 상태 알림(모드 이름, "기다려 주세요" 같은 짧은 알림)은 짧게, 사용자에게 할 일을 지시하는 문장은 합니다체.
- 숫자 사이의 of("1 of 5")는 영어 of를 그대로 둔다(`docs/decisions.tsv` 2026-11-03).

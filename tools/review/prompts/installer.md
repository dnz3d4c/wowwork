# 대상: 설치 프로그램(wowvision-installer) 문자열

이번 입력은 게임 애드온 문자열이 아니라 WowVision 설치 프로그램(C# WinForms, `wowvision-ko/wowvision-installer/WowVisionInstaller/`)의 화면 문구다. 위 공통 규칙 중 Lua·AceLocale·게임 용어에 관한 것은 그대로 적용하지 않고, 아래 규칙이 우선한다.

- 입력에는 `de`(독일어), `fr`(프랑스어) 번역이 함께 있다. 뜻을 확인하는 참고 자료로만 쓴다.
- 자리표시자는 C# `{0}`, `{1}` 형식이다. 개수와 번호가 원문과 같아야 한다. 순서는 바꿔도 된다(번호가 위치를 정한다). 자리표시자 바로 뒤에 받침에 따라 달라지는 조사를 붙이지 않는다.
- 단축키 `&`: 한국어판 Windows 관례대로 영어 글자를 괄호에 둔다. 예: `&Next >` → `다음(&N) >`. 영어 원문과 같은 글자를 쓴다. 단축키가 없는 원문에 `&`를 더하지 않는다.
- 접근성 원칙(원본의 집 규칙): 컨트롤의 접근 가능한 이름(`...Acc` 키)은 그 옆에 표시되는 글(`...Btn`, `...label`, `...desc`)보다 정보가 적으면 안 된다. 짝이 되는 키를 함께 비교한다.
- 시스템 대화 상자의 버튼(Retry, Cancel 등)은 한국어판 Windows 표기(다시 시도, 취소)로 가리킨다.
- 고유 이름은 그대로: WowVision, World of Warcraft, WoW Forever, Anniversary, Classic Era, Battle.net, NVDA, SAPI, SAPI2SR, WoW Login Tool, AutoHotkey, BugGrabber, GitHub, WTF(폴더 이름), Interface\AddOns(경로).
- 낱말: installer = 설치 프로그램, Browse = 찾아보기, download = 내려받기, desktop shortcut = 바탕 화면 바로 가기, Start menu = 시작 메뉴, beta = 베타, stable release = 안정판.
- 문체: 제목·버튼·상태 줄은 짧게, 설명과 안내 문장은 합니다체.

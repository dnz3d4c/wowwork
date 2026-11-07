# upstream 보고 목록

원본(wow-vision/WowVision, wow-vision/wowvision-installer)에 알릴 것을 모은다. 한국어판에서는 고칠 수 없거나, 고치면 원문 충실 결정(`docs/decisions.tsv` 2026-11-05)을 어기는 것들이다.

## 상태

- 아직 보내지 않았다(2026-11-06). 1번 목록은 번역 에이전트가 코드를 읽고 적은 것이고 사람이 다시 확인하지 않았다. 보내기 전에 각 코드 위치를 직접 열어 확인한다.
- 원자료: `reviews/2026-11-05-manual-regression/upstream-raw.json`(20건, 중복 포함), `reviews/2026-11-06-final-ui/result.json`(코드 문자열).

## 1. 설명서와 실제 동작이 다른 곳

| 설명서(en) | 차이 | 코드 위치 |
|------------|------|-----------|
| basics/alerts.md | "you or your group"과 전투 중이면 울린다고 하지만, 파티에서는 party1~5와 그 소환수만 검사한다(나와 내 소환수 제외). 혼자일 때는 player와 소환수, 공격대에서는 raid1~40과 그 소환수 | WowVision core/targeting/module.lua:75-103 |
| basics/interface.md | 희귀 등급 이상이면 모두 "DELETE" 확인을 받는다고 하지만 계승 아이템은 빠진다 | WowVision core/ui modules/cursor.lua:61 |
| basics/keybindings.md | 어깨·트리거·오른쪽 스틱 누르기가 같은 보조 키라고 하지만, 양쪽 어깨를 함께 누르면 바로 가기 층이 되고 오른쪽 스틱 누르기는 방향 패드와만 조합된다 | WowVision core/ui/input/padLogic.lua:15-35, core/graph/keyCapture.lua:136-142 |
| basics/keybindings.md | 같은 충돌 안내가 적용된다고 하지만, 컨트롤러에는 필수 동작의 마지막 입력 보호가 없다 | WowVision core/ui modules/graphBindings.lua:61-79 |
| getting-started/installer.md | 취소하면 현재 단계를 마친 뒤 멈춘다고 하지만, 진행 중인 내려받기는 바로 중단하고 압축 풀기·복사만 끝까지 마친다 | wowvision-installer ProgressForm.cs:141-146 |
| getting-started/installer.md | 게임 종료가 필요한 경우로 처음 설치와 게임 설정만 들지만, 추가 애드온 설치·업데이트 때도 요구한다 | wowvision-installer InstallRunner.cs:439-455 |
| getting-started/installer.md | 업데이트 뒤 /reload만 안내하지만, TOC를 다시 쓴 실행은 게임 재시작을 안내한다 | wowvision-installer InstallRunner.cs:556-561 |
| getting-started/quick-start.md | 스캐너 항목에서 Enter를 누르면 바로 안내가 시작된다고 하지만, 지도 데이터나 경로 엔진이 있으면 길 안내 창이 열리고 Enter를 한 번 더 눌러야 한다 | WowVision core/navigation/maps/module.lua:574-582 |
| reference/commands.md | 요약 표는 /wv padlog를 Retail과 WoW: Forever용이라 하지만 모든 버전에 등록된다(같은 문서 본문도 그렇게 적음) | WowVision core/ui modules/module.lua:162 |
| reference/commands.md | 이름 없이 실행하면 두 명령 모두 "Syntax: /enableaddon <name>"을 출력한다고 하지만 /disableaddon은 "Syntax: /disableaddon <name>"을 출력한다 | WowVision core/WowVision.lua:1139 |
| reference/glossary.md | 상하 각도 고정이 수영과 비행 모두에 걸린다고 하지만 리테일 계열은 비행 중 고정하지 않는다 | WowVision core/navigation/pitchLock.lua:55, retail/pitchLock.lua:3 |
| windows/action-bars.md | 상황별 메뉴의 끌기는 실제 가방 아이템으로 취급한다고 하지만 끌기 키와 같은 함수를 쓴다 | WowVision core/windows/bars/bars.lua:150-164 |
| windows/loot-trade-mail.md | 개수를 두 개 이상일 때만 읽는다고 하지만 1개여도 " x1"을 붙인다 | WowVision core/windows/trade.lua:19-20 |

## 2. 번역할 수 없는 코드 문자열

`L[]` 밖에 영어가 직접 들어 있어서 어떤 언어에서도 영어로 읽힌다.

| 문자열 | 위치 |
|--------|------|
| `" in "` (경매장 스캔 진행 안내) | WowVision tbc/auction/ScanSession.lua:147 |
| `" min "`, `" sec"` (경매장 스캔 남은 시간) | WowVision tbc/auction/module.lua:80-93 |

## 3. 여러 기능이 같은 키를 써서 한국어로 맞게 옮길 수 없는 문자열 (2026-11-07 설명서 다듬기)

같은 영어 키를 서로 다른 문맥에서 함께 써서, 한 문맥의 게임 공식 이름을 따르면 다른 문맥이 틀린다. 키를 문맥별로 나눠야 한다. 두 회사 판정자가 코드의 쓰임을 확인했다(`reviews/2026-11-07-kokr-candidates`). 보내기 전에 위치를 다시 확인한다.

| 키 (koKR 현재 값) | 문맥 A와 공식 한국어 | 문맥 B와 공식 한국어 |
|-------------------|----------------------|----------------------|
| quests.lua `Trainers` (상급자) | 미니맵 추적 Profession Trainers: 기술 전문가 (MINIMAP_TRACKING_TRAINER_PROFESSION) | 퀘스트 스캐너 TRAINER 역할(직업 상급자 포함): 상급자 (TUTORIAL_TITLE14) |
| ui.lua `Repair` (수리) | 미니맵 추적 Repair: 장비 수리 (MINIMAP_TRACKING_REPAIR) | 상인 창 수리 묶음: 수리 (CONTEXT_ACTION_LABEL_REPAIR) |
| ui.lua `Available` (사용 가능) | 경매장 결과 수량: 구매 가능 수량 | 특성 선택 가능 상태: 사용 가능 (AVAILABLE) |

## 4. 코드가 이어 붙여 한국어 띄어쓰기를 맞출 수 없는 문자열

| 결과 | 위치 |
|------|------|
| "12 개 출현 지점": 숫자, 공백, `L["spawns"]` 순서로 붙여 단위 "개"가 띄어진다 | WowVision core/quests/scanner.lua:81, 125 |

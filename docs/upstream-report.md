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
| reference/commands.md (V1.0.1) | /wv targetinfo가 마지막에 "실제로 들리는 그대로의 알림"을 보여 주고 말로 읽는다고 하지만, 대상 알림 설정이 꺼져 있으면(기본값) 알림을 만들지 않고 말하지도 않는다 | WowVision targetNames.lua:832-835, 1006, names.lua:109-112 (2026-11-08 설명서 평가 판정자 확인) |
| reference/commands.md (V1.0.1) | 게임이 숨기는 항목은 <secret>으로 표시된다고 하지만, 숨겨진 참·거짓 값과 숫자는 건너뛰고 읽을 값이 없으면 `-`로 표시한다 | WowVision targetNames.lua:11-15, 848-855 (2026-11-08 설명서 평가 판정자 확인) |
| reference/commands.md | 이름 없이 실행하면 두 명령 모두 "Syntax: /enableaddon <name>"을 출력한다고 하지만 /disableaddon은 "Syntax: /disableaddon <name>"을 출력한다 | WowVision core/WowVision.lua:1139 |
| reference/glossary.md | 상하 각도 고정이 수영과 비행 모두에 걸린다고 하지만 리테일 계열은 비행 중 고정하지 않는다 | WowVision core/navigation/pitchLock.lua:55, retail/pitchLock.lua:3 |
| windows/action-bars.md | 상황별 메뉴의 끌기는 실제 가방 아이템으로 취급한다고 하지만 끌기 키와 같은 함수를 쓴다 | WowVision core/windows/bars/bars.lua:150-164 |
| windows/loot-trade-mail.md | 개수를 두 개 이상일 때만 읽는다고 하지만 1개여도 " x1"을 붙인다 | WowVision core/windows/trade.lua:19-20 |
| reference/keybindings.md (V1.0.2) | 모든 창 닫기(Shift+Escape)가 모든 창을 닫는다고 하지만, 응답을 기다리는 팝업과 전투 중 보호된 게임 창은 남는다(릴리스 노트에는 적혀 있음) | WowVision core/ui/WindowManager.lua:168-189 |
| reference/keybindings.md (V1.0.2) | 같은 이름의 미방문 지점 경로 안내가 걸어서 가장 가까운 곳을 고른다고 하지만, 직선거리로 가까운 후보 8곳 가운데서만 고른다 | WowVision core/navigation/visited.lua:96-116 |
| reference/keybindings.md (V1.0.2) | 주사위 툴팁이 툴팁 전체를 읽는다고 하지만, 아이템 링크나 툴팁 내용을 얻지 못하면 이름만 읽는다 | WowVision core/windows/loot.lua:20-43 |
| windows/auction-house.md (V1.0.2) | Retail 전체 스캔이 모든 아이템의 가격을 기억한다고 하지만, 즉시 구입가가 없는 경매는 빼고 기록한다 | WowVision retail/auction/prices.lua:26-32 |
| windows/auction-house.md (V1.0.2) | Retail "Vendor Buy"는 상인에게서 아이템을 본 뒤 나온다고 하지만, 수량 제한이 없고 추가 비용이 없는 아이템만 기록한다 | WowVision retail/auction/module.lua:160-168 |
| world/quests.md (V1.0.2) | 주변 퀘스트 소리는 장소가 앞쪽에 있을 때만 들린다고 하지만, 거리와 정면에서 벗어난 각도를 합쳐 판단해 가까우면 옆쪽(10야드에서 100도)도 들린다 | WowVision core/quests/nearbyEngine.lua:32-46, nearbyEngineTests.lua:68-74 |
| world/quests.md (V1.0.2) | 축제 퀘스트는 축제 기간에만 포함된다고 하지만, 축제 뒤에도 완료할 수 있는 퀘스트는 완료 가능 장소로 계속 남는다 | WowVision core/quests/nearbySounds.lua:215 |
| information/buffers.md (V1.0.2) | 버퍼 설정 화면이 사용함, 버퍼, 항목 방향 반전 세 가지를 이 순서로 보여 준다고 하지만(244줄), 같은 문서 설정 표에 새로 생긴 Always Start at Top과 Sounds When Opening and Closing도 그 화면에 있다 | WowVision core/buffers/module.lua:20-38 |
| getting-started/managing.md (V1.0.2) | 표(14줄)는 WowVisionPriceDB를 TBC, Retail, WoW: Forever용이라 하고 본문(18줄)은 "on TBC"라고만 해서 문서 안에서 어긋난다. 코드는 표와 같다 | WowVision WowVision_Standard.toc:8, WowVision_Camelot.toc:8 |

## 2. 번역할 수 없는 코드 문자열

`L[]` 밖에 영어가 직접 들어 있어서 어떤 언어에서도 영어로 읽힌다.

남은 것 없음. 경매장 스캔 안내의 `" in "`, `" min "`, `" sec"`는 wow-vision/vision-locale#66, wow-vision/WowVision#109로 서식 문자열 키가 되어 2026-11-08 병합됐고, koKR 값을 넣었다(2026-11-09).

## 3. 여러 기능이 같은 키를 써서 한국어로 맞게 옮길 수 없는 문자열 (2026-11-07 설명서 다듬기)

같은 영어 키를 서로 다른 문맥에서 함께 써서, 한 문맥의 게임 공식 이름을 따르면 다른 문맥이 틀린다. 키를 문맥별로 나눠야 한다. 두 회사 판정자가 코드의 쓰임을 확인했다(`reviews/2026-11-07-kokr-candidates`). 보내기 전에 위치를 다시 확인한다.

| 키 (koKR 현재 값) | 문맥 A와 공식 한국어 | 문맥 B와 공식 한국어 |
|-------------------|----------------------|----------------------|
| quests.lua `Trainers` (상급자) | 미니맵 추적 Profession Trainers: 기술 전문가 (MINIMAP_TRACKING_TRAINER_PROFESSION) | 퀘스트 스캐너 TRAINER 역할(직업 상급자 포함): 상급자 (TUTORIAL_TITLE14) |
| ui.lua `Repair` (수리) | 미니맵 추적 Repair: 장비 수리 (MINIMAP_TRACKING_REPAIR) | 상인 창 수리 묶음: 수리 (CONTEXT_ACTION_LABEL_REPAIR) |

## 4. 코드가 이어 붙여 한국어 띄어쓰기를 맞출 수 없는 문자열

| 결과 | 위치 |
|------|------|
| "12 개 출현 지점": 숫자, 공백, `L["spawns"]` 순서로 붙여 단위 "개"가 띄어진다 | WowVision core/quests/scanner.lua:120, 165 (원본 main 5cbf76a) |

## 5. 다른 언어를 전제하거나 뜻이 모호한 설명서 문장 (2026-11-09 설명서 평가)

한국어판은 원문대로 옮겼다(2026-11-09 사용자 결정: 원문 그대로 두고 원본에 보고). 평가자가 지적했고 코드로 확인한 내용이다(`reviews/2026-11-09-manual-main`, `reviews/2026-11-09-manual-main-regression`).

| 설명서(en) | 문제 | 코드 위치 |
|------------|------|-----------|
| world/wownav.md:75 | 괄호 안 직함도 번역되므로 "aubergiste", "cuisinier"로 검색할 수 있다고 한다. 프랑스어 클라이언트의 예시라서 다른 언어 사용자에게는 그대로 맞지 않는다. "게임 언어로 된 직함" 같은 일반 표현이 낫다 | WowVision camelot/wownav/text.lua:224-234, 300-304 |
| world/wownav.md:61 | Ctrl+Shift+N과 대상까지의 경로는 "where you stand if that is clear"에서 시작한다고 한다. 실제 조건은 서 있는 곳의 층을 가릴 수 있는지다(모호하면 "ambiguous") | WowVision camelot/wownav/module.lua:183-194 |
| world/navigation.md:233 | "Ctrl+S before the start of a leg"는 구간 시작에서 한 번 더 뒤로 가는 동작인데, 구간 밖에서 누르라는 뜻으로도 읽힌다 | WowVision core/navigation/visited.lua:284-298 |

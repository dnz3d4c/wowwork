# 설명서 회귀 확인 3회차에 남은 중대 지적

회귀 3회차: 20개 중 10개 통과. 절차상 순환 2회를 마쳐서 사용자 판단으로 넘긴다.

## getting-started/installer.md

1. (claude, terminology, major)
   - 현재: 게임의 음성 번호가 바뀔 수 있으니, 설치 후 말하기 음성을 확인하십시오.
   - 제안: 게임의 음성 번호가 바뀔 수 있으니, 설치 후 음성 종류 설정을 확인하십시오.
   - 문제: 원문 "check your speech voice afterward"는 WowVision의 Speech Voice 설정을 가리키는데, 번역의 "말하기 음성"은 실제 설정 이름과 다르다. 독자가 존재하지 않는 "말하기 음성" 설정을 찾게 된다.
   - 근거: vision-locale/koKR/speech.lua:5 L["Speech Voice"] = "음성 종류"; en/basics/speech.md 설정 표 'Speech Voice' ↔ ko/basics/speech.md:16 '음성 종류'. 설명서 다른 파일에 '말하기 음성' 표기는 없음(Grep 결과 installer.md:48 한 곳).

2. (gpt, terminology, major)
   - 현재: 게임의 음성 번호가 바뀔 수 있으니, 설치 후 말하기 음성을 확인하십시오.
   - 제안: 게임의 음성 번호가 바뀔 수 있으니, 설치 후 음성 종류를 확인하십시오.
   - 문제: WowVision의 실제 설정 이름인 ‘음성 종류’ 대신 ‘말하기 음성’을 써서, 독자가 존재하지 않는 설정을 찾게 됩니다.
   - 근거: 원문은 “check your speech voice afterward”입니다. wowvision-ko/vision-locale/koKR/speech.lua:5에서 `Speech Voice`는 `음성 종류`이고, wowvision-ko/WowVision/docs/src/user/ko/basics/speech.md:16과 :33도 같은 표기를 씁니다. `말하기 음성`은 이 파일에만 있습니다.

3. (gpt, terminology, major)
   - 현재: 직접 압축을 푼 베타나 그 밖의 테스트 빌드는 모두 다시 설치 항목을 고를 때까지 손대지 않습니다.
   - 제안: 직접 압축을 푼 베타나 그 밖의 테스트 빌드는 "모두 다시 설치(복구)" 항목을 체크할 때까지 손대지 않습니다.
   - 문제: 화면 항목을 가리키면서 실제 이름의 ‘(복구)’를 누락했습니다. 같은 파일 앞부분에서는 전체 이름을 사용하므로 표기도 일관되지 않습니다.
   - 근거: 원문의 `Reinstall everything`은 구성 요소 페이지의 확인란을 가리킵니다. 실제 한국어 화면 문구는 wowvision-ko/wowvision-installer/WowVisionInstaller/Loc.cs:933의 `모두 다시 설치(복구)`이며, 번역문 앞부분도 `모두 다시 설치(복구)(체크 안 됨)`이라고 씁니다. manual-translate.md의 용어 규칙은 화면 문구를 실제 한국어 값과 글자 그대로 맞추도록 합니다.

## getting-started/introduction.md

4. (gpt, terminology, major)
   - 현재: 길 안내 창(F10)은 경유지 연결망을 따라 경로를 짜고 소리 비컨으로 목적지까지 이끕니다.
   - 제안: 길 안내 창(F10)은 경유지 네트워크를 따라 경로를 짜고 소리 비컨으로 목적지까지 이끕니다.
   - 문제: 확정 용어인 "네트워크"를 "연결망"으로 다르게 옮겼습니다. 다른 설명서의 같은 개념과도 표기가 일치하지 않습니다.
   - 근거: 원문은 "a network of waypoints"입니다. wowwork/docs/glossary.tsv에서 network는 "네트워크"로 확정되어 있습니다. wowvision-ko/WowVision/docs/src/user/ko/world/scanner.md:93도 같은 개념을 "경유지 네트워크"로 씁니다.

## getting-started/sku.md

5. (claude, terminology, major)
   - 현재: 퀘스트 제공자 창(퀘스트 수락과 완료 보고).
   - 제안: 퀘스트 NPC 창(퀘스트 수락과 완료 보고).
   - 문제: Quest giver 창을 '퀘스트 제공자 창'으로 옮겨, 같은 창을 '퀘스트 NPC 창'이라 부르는 다른 설명서 파일과 애드온 화면 문구와 어긋난다. 같은 창이 페이지마다 다른 이름으로 들린다.
   - 근거: 원문 'Quest giver window'. vision-locale/koKR/quests.lua:45 L["Quest Giver"] = "퀘스트 NPC", quests.lua:22 L["Quest Givers"] = "퀘스트 NPC". 다른 파일 표기: windows/overview.md:56 '퀘스트 NPC 창', reference/versions.md:31 '퀘스트 NPC 창', world/index.md:13 '퀘스트 NPC 창과 Questie', getting-started/introduction.md:10 '퀘스트 NPC 창'.

6. (gpt, terminology, major)
   - 현재: - 대화와 그 밖의 NPC 대화창.
- 상인.
- 우체통.
- 팝업(게임의 확인 대화상자).
   - 제안: - 대화와 그 밖의 NPC 대화창.
- 상인.
- 우편함.
- 팝업(게임의 확인 대화상자).
   - 문제: 창 목록에서 물리적인 우편 시설을 뜻하는 "우체통"을 사용했습니다. Sku가 맡는 대상은 우체통 오브젝트가 아니라 우편 창이므로 독자가 동작 범위를 잘못 이해할 수 있습니다.
   - 근거: 원문은 창 목록에서 "Mailbox"를 열거합니다. wowvision-ko/WowVision/docs/src/user/ko/windows/loot-trade-mail.md:71과 :150은 같은 창을 "우편함"으로 표기하고, :73은 물리적인 대상인 "우체통"과 열리는 "우편 창"을 구분합니다. 실제 창 이름도 wowvision-ko/vision-locale/koKR/windows.lua:97에서 "Mail"을 "우편"으로 번역합니다.

7. (gpt, terminology, major)
   - 현재: - 상급자.
- 전투 준비 확인과 던전 입장 준비 팝업.
- 역할 투표(역할 확인 팝업).
   - 제안: - 상급자.
- 전투 준비 확인과 던전 준비 팝업.
- 역할 투표(역할 확인 팝업).
   - 문제: 같은 게임 팝업을 다른 설명서와 다른 이름으로 표기했습니다. 스크린리더로 실제 팝업 제목을 들은 사용자가 이 항목과 같은 창인지 바로 식별하기 어렵습니다.
   - 근거: 원문은 "the dungeon ready popup"입니다. wowvision-ko/WowVision/docs/src/user/ko/windows/group-finder.md:158의 제목과 :160의 게임 화면 문구는 모두 "던전 준비 팝업"이며, :19에서도 Sku가 맡는 대상을 "던전 준비"로 표기합니다. 동작 대상은 wowvision-ko/WowVision/core/windows/ready.lua:61-68의 LFGDungeonReadyDialog입니다.

## information/buffers.md

8. (gpt, terminology, major)
   - 현재: 그룹을 저장하는 곳을 바꾸려면 그룹 목록에서 그 그룹으로 가서 Shift+F10(컨텍스트 메뉴)을 누릅니다.
   - 제안: 그룹을 저장하는 곳을 바꾸려면 그룹 목록에서 그 그룹으로 가서 Shift+F10(상황별 메뉴)을 누릅니다.
   - 문제: 실제 화면 용어인 ‘상황별 메뉴’를 ‘컨텍스트 메뉴’로 다르게 옮겼다.
   - 근거: wowvision-ko/vision-locale/koKR/ui.lua:58과 bindings.lua:24에서 Context Menu는 ‘상황별 메뉴’다. 다른 설명서도 wowvision-ko/WowVision/docs/src/user/ko/basics/interface.md:33, basics/menu-and-settings.md:163, information/monitors.md:63에서 ‘상황별 메뉴’로 통일했다.

## information/monitors.md

9. (gpt, context, major)
   - 현재: 오라, 재사용 대기, 주문 재사용 대기 규칙에서는 이 캐릭터로 시전했거나 오라로 확인한 주문이 목록에 나옵니다.
   - 제안: 오라 및 재사용 대기 규칙에서는 이 캐릭터로 시전했거나 오라로 확인한 주문이 목록에 나옵니다.
   - 문제: 주문 재사용 대기 규칙의 빠른 선택 목록 출처를 잘못 설명한다. 이 규칙은 캐릭터가 시전하거나 오라로 확인한 주문이 아니라 재사용 대기시간 관리자의 핵심 능력과 보조 능력 항목을 사용한다.
   - 근거: wowvision-ko/WowVision/retail/monitors/SpellCooldownMonitor.lua:145-150은 빠른 선택이 재사용 대기시간 관리자의 Essential 및 Utility 항목이라고 명시하고, 같은 파일 262-276에서 cooldownSpells와 procSpells를 해당 선택 화면에 연결한다. 바로 다음 번역 문장도 재사용 대기시간 관리자 항목을 보여 준다고 설명해 문단 안에서 서로 모순된다.

## reference/glossary.md

10. (claude, terminology, major)
   - 현재: 단축키 동작 — 다음 버퍼 항목처럼 키에 지정할 수 있는 동작입니다.
   - 제안: 바인딩(단축키 동작) — 다음 버퍼 항목처럼 키에 지정할 수 있는 동작입니다.
   - 문제: 용어집 표제어로 Binding을 '단축키 동작'으로 옮겼지만, 같은 개념을 정의하는 키 바인딩 목록 페이지는 '바인딩'을 쓴다. 독자가 다른 페이지에서 '바인딩'을 듣고 용어집을 찾아도 해당 표제어가 없다. 같은 파일의 '지정 안 됨' 정의(단축키 동작은 있지만)도 키 바인딩 목록의 같은 정의(바인딩은 있지만)와 어긋난다.
   - 근거: 원문 'Binding — An action that can be put on a key'. wowvision-ko/WowVision/docs/src/user/ko/reference/keybindings.md:6 ""지정 안 됨"은 바인딩은 있지만...", :105 'Alt Gr은 바인딩이 아닙니다', :158·:162·:184 '바인딩'. ko 설명서 전체에서 '단축키 동작'은 glossary.md에만 나온다(Grep 2건, 모두 이 파일). decisions.tsv·glossary.tsv에 binding 결정 없음.

## windows/action-bars.md

11. (gpt, terminology, major)
   - 현재: 리테일이 위의 네 개 외에 추가한 단축바(행동 단축바 5, 6, 7), 추가 행동 버튼, 지역 능력 버튼, 운송 수단 단축바나 지배 단축바는 읽지 않습니다.
   - 제안: 리테일이 위의 네 개 외에 추가한 단축바(행동 단축바 5, 6, 7), 추가 행동 버튼, 지역 능력 버튼, 운송 수단 단축바나 행동 단축바 조정은 읽지 않습니다.
   - 문제: 게임 공식 용어인 “행동 단축바 조정”을 “지배 단축바”로 옮겨 게임 화면의 이름과 다르다.
   - 근거: 원문은 “the vehicle or possess bars”라고 한다. wowwork/cache/gs_enUS.csv:20656의 HUD_EDIT_MODE_POSSESS_ACTION_BAR_LABEL은 “Possess Bar”이고, 같은 BaseTag의 wowwork/cache/gs_koKR.csv:20666은 “행동 단축바 조정”이다. manual-translate.md 용어 규칙 2는 용어표에 없는 게임 용어에 게임 공식 한국어를 쓰도록 정한다.

12. (gpt, context, major)
   - 현재: 각 칸은 일반 칸처럼 읽고, 이어서 그 칸을 발동하는 컨트롤러 버튼을 말합니다.

- "얼음 화살, A"
- "비어 있음, X"
   - 제안: 각 칸은 일반 칸처럼 읽고, 이어서 그 칸을 발동하는 컨트롤러 버튼을 말합니다.

- "얼음 화살, A 버튼"
- "비어 있음, X 버튼"
   - 문제: 예시의 낭독 문구에서 “버튼”이 빠져 실제 한국어판이 말하는 문구와 다르다.
   - 근거: WowVision/camelot/gamepadBars.lua:57-60은 각 칸에 WowVision.pad.inputText의 결과를 붙인다. WowVision/core/ui/input/pad.lua:474-477은 PAD1과 PAD3 등에 “A button”, “X button” 로케일 키를 사용하고, vision-locale/koKR/controller.lua:6-9의 실제 값은 “A 버튼”, “X 버튼”이다. 다른 한국어 설명서 WowVision/docs/src/user/ko/controller.md:136도 실제 낭독 이름을 “A 버튼, B 버튼, X 버튼, Y 버튼”으로 적는다.

## windows/character.md

13. (claude, context, major)
   - 현재: 3. 구성을 선택하면 장착, 저장, 세트 편집, 삭제가 정지점 하나씩 나옵니다. 장착을 누르면 선택한 구성을 착용합니다. 저장을 누르면 지금 입은 장비를 그 구성에 저장합니다. 세트 편집을 누르면 이름과 아이콘 창이 열립니다.
   - 제안: 3. 구성을 선택하면 장비, 저장, 이름/아이콘 변경, 삭제가 정지점 하나씩 나옵니다. 장비 버튼을 누르면 선택한 구성을 착용합니다. 저장을 누르면 지금 입은 장비를 그 구성에 저장합니다. 이름/아이콘 변경을 누르면 이름과 아이콘 창이 열립니다.
   - 문제: Equip 버튼과 Edit Set 버튼은 애드온 번역이 아니라 게임 전역 문자열로 읽힌다. 한국어 클라이언트에서 실제로 들리는 이름은 '장비'와 '이름/아이콘 변경'인데 설명서는 '장착'과 '세트 편집'으로 적어, 사용자가 들리지 않는 이름을 찾게 된다.
   - 근거: WowVision/camelot/character.lua:547 Equip 정지점은 nodes.proxyButton({ target = pane.EquipSet })로 label 없이 게임 버튼 글자(EQUIPSET_EQUIP)를 읽음. character.lua:559 Edit 정지점 label = EQUIPMENT_SET_EDIT or L["Edit Set"]로 전역 문자열이 우선, 애드온 locale(세트 편집)은 전역이 없을 때만 씀. wowwork/cache/gs_koKR.csv: 20051 EQUIPSET_EQUIP=장비, 21880 EQUIPMENT_SET_EDIT=이름/아이콘 변경. terms의 'Edit Set=세트 편집'은 애드온 fallback 값이다. 단 WoW: Forever 클라이언트가 이 전역 문자열을 갖는지는 게임 안에서 확인 필요.

14. (claude, context, major)
   - 현재: 새 구성과 세트 편집은 구성 창을 독립된 창으로 엽니다.
   - 제안: 새 구성과 이름/아이콘 변경은 구성 창을 독립된 창으로 엽니다.
   - 문제: 위 지적과 같은 버튼(EQUIPMENT_SET_EDIT)을 '세트 편집'으로 적었다. 같은 단락 묶음에서 한 곳만 고치면 이름이 엇갈리므로 함께 고쳐야 한다.
   - 근거: character.lua:559 label = EQUIPMENT_SET_EDIT or L["Edit Set"]; wowwork/cache/gs_koKR.csv 21880 EQUIPMENT_SET_EDIT=이름/아이콘 변경. 새 구성은 gs_koKR.csv 21879 PAPERDOLL_NEWEQUIPMENTSET=새 구성으로 맞음.

15. (claude, context, major)
   - 현재: 4. 장착이 들릴 때까지 Tab을 누르고 Enter를 누릅니다.
   - 제안: 4. 장비가 들릴 때까지 Tab을 누르고 Enter를 누릅니다.
   - 문제: 예시 절차의 마지막 단계에서 기다릴 버튼 이름을 '장착'으로 적었다. 실제로는 게임 버튼 글자 '장비'가 들리므로 사용자가 들릴 말을 기다리다 지나칠 수 있다.
   - 근거: character.lua:547 proxyButton({ target = pane.EquipSet })는 게임 버튼 글자를 읽음; wowwork/cache/gs_koKR.csv 20051 EQUIPSET_EQUIP=장비. 애드온 locale의 L["Equip"]=장착(vision-locale/koKR/windows.lua:265)은 이 버튼에 쓰이지 않는다.

16. (gpt, context, major)
   - 현재: - 불타는 성전에서는 모두 접기 / 모두 펼치기 버튼이 먼저 나옵니다. 버튼 이름은 누르면 일어날 일을 나타냅니다.
- 머리글은 "펼쳐짐" 또는 "접힘"으로 읽히고 Enter로 접습니다.
   - 제안: - 불타는 성전에서는 모두 접기 / 모두 펼치기 버튼이 먼저 나옵니다. 버튼 이름은 누르면 일어날 일을 나타냅니다.
- 머리글은 "펼쳐짐" 또는 "접힘"으로 읽히고 Enter를 누르면 접거나 펼칩니다.
   - 문제: Enter가 펼쳐진 머리글을 접기만 하는 것처럼 설명해, 이미 접힌 숙련 범주를 같은 키로 다시 펼칠 수 있다는 동작이 누락됐다.
   - 근거: 원문은 "Headers read \"Expanded\" or \"Collapsed\" and fold with Enter."이다. 실제로 TBC는 머리글의 펼침 상태를 양쪽 모두 읽고 머리글 버튼에 클릭 동작을 연결하며(wowvision-ko/WowVision/tbc/character/Skills.lua:68, wowvision-ko/WowVision/tbc/character/Skills.lua:91), WoW: Forever도 접기 전환 버튼을 사용한다(wowvision-ko/WowVision/camelot/character.lua:93, wowvision-ko/WowVision/camelot/character.lua:783).

17. (gpt, context, major)
   - 현재: 화폐 목록이 담긴 정지점 하나입니다. 머리글은 "펼쳐짐" 또는 "접힘"으로 읽히고 Enter로 접습니다. 화폐는 이름과 보유량을 읽습니다.
   - 제안: 화폐 목록이 담긴 정지점 하나입니다. 머리글은 "펼쳐짐" 또는 "접힘"으로 읽히고 Enter를 누르면 접거나 펼칩니다. 화폐는 이름과 보유량을 읽습니다.
   - 문제: 화폐 머리글도 Enter로 접고 펼치는 전환 동작인데 접는 동작만 설명해, 접힌 범주를 다시 여는 방법을 빠뜨렸다.
   - 근거: 원문은 "Headers read \"Expanded\" or \"Collapsed\" and fold with Enter."이다. 판다리아의 안개 구현은 머리글의 펼침 상태를 읽고 같은 행에 클릭 동작을 연결하며(wowvision-ko/WowVision/mists/character.lua:313, wowvision-ko/WowVision/mists/character.lua:323), WoW: Forever 구현도 접기 전환 버튼을 대상으로 삼는다(wowvision-ko/WowVision/camelot/character.lua:863, wowvision-ko/WowVision/camelot/character.lua:873).

## windows/loot-trade-mail.md

18. (claude, accuracy, major)
   - 현재: 예를 들어 입찰을 선택하면 그 아이템이 당신에게 귀속된다는 확인입니다.
   - 제안: 예를 들어 "이 아이템은 내 캐릭터에 귀속됩니다" 같은 확인입니다.
   - 문제: 원문에 없는 조건 "입찰을 선택하면"이 추가됐다. 원문은 확인 문구의 예만 들 뿐 어떤 선택에서 뜨는지 한정하지 않는다. 이 조건 때문에 독자는 차비를 고르면 확인 창이 뜨지 않는다고 오해할 수 있다. 원문의 따옴표 인용도 사라졌고, "당신에게"는 파일 나머지의 "내" 표기와 어긋난다.
   - 근거: 원문 3단계: "For some items the game asks you to confirm, for example "This item will bind to you"." 조건(if you choose Need) 없음. 같은 파일의 다른 곳은 "내 대상 메뉴", "내 거래 칸"처럼 "내"를 쓴다.

19. (claude, terminology, major)
   - 현재: 편지 다음에는 게임이 보여 주는 버튼마다 멈추는 곳이 하나씩 있습니다.
   - 제안: 편지 다음에는 게임이 보여 주는 버튼마다 정지점이 하나씩 있습니다.
   - 문제: 원문의 stop(탭 정지점)을 이 파일만 "멈추는 곳"으로 옮겼다. 설명서의 용어집과 인터페이스 페이지, 다른 창 페이지는 모두 "정지점"(탭 정지점)을 쓰므로, 독자가 이 페이지의 "멈추는 곳"을 용어집에서 배운 개념과 연결하지 못한다. 이 파일 안의 6곳("멈추는 곳은 차례대로 다음과 같습니다." 2곳, "멈추는 곳은 다음과 같습니다.", "다음 멈추는 곳으로", "상자마다 멈추는 곳이 따로", 이 문장)을 모두 "정지점"으로 맞춰야 한다.
   - 근거: ko/reference/glossary.md:58 "탭 정지점 — 목록, 버튼 줄, 검색 상자처럼 Tab과 Shift+Tab으로 건너뛰어 가는 창의 구역"; ko/basics/interface.md:86 "### 탭 정지점"; ko/windows/system.md:26 "정지점은 다음 순서입니다."; windows 폴더의 정지점 사용 횟수: bags-and-bank 12, character 24, spells-and-talents 19, professions 14, system 9, npcs 8, action-bars 2. "멈추는 곳"은 loot-trade-mail.md에만 있다(auction-house.md는 "정지 위치"로 역시 어긋남).

20. (gpt, terminology, major)
   - 현재: 5. 돈 보내기: 확인란.
6. 대금 청구: 확인란. 아이템을 첨부하기 전까지는 비활성 상태입니다.
   - 제안: 5. 돈 보내기: 체크 상자.
6. 대금 청구: 체크 상자. 아이템을 첨부하기 전까지는 비활성 상태입니다.
   - 문제: 실제로 낭독되는 컨트롤 종류인 "체크 상자"를 "확인란"으로 다르게 적었습니다.
   - 근거: wowvision-ko/WowVision/classic/mail.lua:169-175는 두 항목을 checkButtonNode로 만들고, wowvision-ko/WowVision/core/graph/ControlTypes.lua:40은 toggle 컨트롤을 L["Checkbox"]로 등록합니다. 실제 한국어 값은 wowvision-ko/vision-locale/koKR/ui.lua:33의 "체크 상자"입니다. 다른 설명서도 wowvision-ko/WowVision/docs/src/user/ko/basics/interface.md:53과 windows/auction-house.md:168에서 "체크 상자"를 사용합니다.

## windows/professions.md

21. (gpt, context, major)
   - 현재: 8. 제작, 모두 제작, 그리고 표시될 때는 길드 내 제작자 보기. 비활성화된 제작 버튼은 게임이 알려주는 이유(무엇이 부족한지)도 읽습니다.
   - 제안: 8. 제작, 모두 제작, 그리고 표시될 때는 제작자 보기. 비활성화된 제작 버튼은 게임이 알려주는 이유(무엇이 부족한지)도 읽습니다.
   - 문제: 실제로 읽히는 버튼 문구와 설명서의 표기가 다릅니다. 스크린리더 사용자가 설명서에서 안내한 이름으로 버튼을 찾기 어렵습니다.
   - 근거: wowwork/cache/gs_koKR.csv:9195의 GUILD_TRADE_SKILL_VIEW_CRAFTERS 값은 "제작자 보기"입니다. wowvision-ko/WowVision/camelot/crafting.lua:467-470은 ViewGuildCraftersButton을 별도 번역 없이 게임 버튼 자체의 문구로 읽습니다.

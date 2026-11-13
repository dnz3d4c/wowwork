# WowVision 한국어 설명서 감수 보고

- 대상: `WowVision/docs/src/user/ko` 51개 파일 8506줄 전부. 영어 `en`과 파일 단위로 대조했다. interface.md와 전수 grep 집계는 직접, 나머지는 범위 7개로 나눠 끝까지 읽은 결과를 5부에 그대로 붙였다.
- 어떤 저장소 파일도 수정하지 않았다.
- 줄 번호는 한국어 파일 기준이다(영어는 대개 한 줄 앞).
- 낱말 결정표(`fluent-korean.md` 구 단위 2번 표)는 정답으로 전제하지 않고 설명서 문맥에서 따로 판정했다. 결과는 3부에 있다.

## 0. 한눈에

| 부류 | 개별 사례(대략) | 반복 표현 |
|---|---|---|
| (a) 지시어 대상이 귀로 안 잡힘 | 약 40 | "그곳에서는"(게임 버전), "그것을 고릅니다" |
| (b) 영어 관용구·은유 직역 | 약 160 | 키를 가져가다·돌려주다·물러나다 계열 약 45곳, 도착하다(초점) 14곳, 지켜보다 19곳, 치다 20줄, 울리다 23줄, 그리다 6곳, 모르다·알다 약 10곳, 조용하다, 데려가다 |
| (c) 목적어·주어 생략 | 약 80 | "확정합니다"(목적어 없음) 6곳, 주어 없는 "놓입니다" 약 12곳 |
| (d) 동사·낱말 선택 | 약 80 | 쓰다(use) 약 365곳, 오가다 17줄, 뒤로 가다 9곳, switch를 "변경"으로 옮긴 곳 약 15곳, 뜨다·띄우다 8줄 |
| (e1) 파일 사이 용어 갈림 | 약 25쌍 | 확인란 15줄, 상황 메뉴 8줄, 포커스 3줄, 조합 키 5줄, 정지 지점 7줄, 로드 16줄, 키 이름 번역(위/아래, 오른쪽 화살표) |
| (e2) 조사 오류 | 16곳 | "[알림](…)를/와" (경보→알림 치환 잔재) |
| (e3) 따옴표 없는 화면 문구·설정 이름이 문장에 녹음 | 약 30 | "비컨 중지는 취소할 때 말합니다", "없음은 대체가 없습니다" |
| (e4) 무생물 주어 + 읽다·말하다 | 약 55곳 | "각 칸은 ~을 읽습니다", 제목 "칸이 읽는 내용" |
| (e5) 사용자 결정 위반·미번역 | 4 | "리테일" 1곳, "12 min 30 sec" 2곳, "경로 계획기·선택기" 7줄 |
| 로케일 값 문제 | 18 | 4부 |

건수는 범위별 보고를 합친 값이라 ±10% 정도 오차가 있다. grep으로 센 것(줄 수를 적은 것)은 정확하다.

---

## 1. 사용자가 지적한 예시 8개

### 1) interface.md:4 "그 창을 읽고 … 창 안을 이동할 수 있게 합니다"

- 원문: When a game window opens, such as your bags, a merchant or the character pane, WowVision reads it and lets you move through it with the keyboard, much like a desktop application.
- 수정안: 가방, 상인, 캐릭터 창 같은 게임 창이 열리면 WowVision이 열린 창의 내용을 읽어 주고, 데스크톱 프로그램을 사용할 때처럼 키보드로 창 안의 항목 사이를 이동할 수 있게 해 줍니다.
- 이유: 선행어 "게임 창" 앞에 예시 세 개가 끼어 있어서 "그 창"이 가방인지 상인 창인지 귀로 다시 찾아야 한다. it을 "그"로 받지 말고 "열린 창"으로 풀어 말한다. "창을 읽다"도 목적어가 비어 있다. 읽는 것은 창의 내용이다. move through it은 "창 안을 이동"이 아니라 창 안의 항목 사이를 이동하는 것이다.

### 2) interface.md:8, 10, 17 "키를 가져가는 때", "이동 키를 가져갑니다"

- 원문: When WowVision takes your keys / WowVision only takes the navigation keys while a window is open. / … waits until you let go of the keys it needs before it takes them.
- 실제 동작: 창이 열려 있는 동안 WowVision이 화살표 키, Tab, Enter 등에 임시로 자기 기능을 걸어서(override binding) 게임의 원래 기능(걷기, 점프) 대신 창 탐색에 사용한다. 전투가 시작되면 임시 지정을 풀어 게임의 원래 기능으로 되돌린다(troubleshooting.md:57).
- 수정안
  - 제목: WowVision이 키 입력을 대신 처리하는 경우
  - 10줄: WowVision은 창이 열려 있는 동안에만 탐색 키 입력을 게임 대신 처리합니다. 열린 창이 없으면 화살표 키, Tab, Enter 등은 게임에서 원래 하던 기능(걷기, 돌기, 점프 등)을 합니다.
  - 17줄: … WowVision은 필요한 키에서 손을 뗄 때까지 기다렸다가 그 키의 입력을 처리하기 시작합니다.
- 이유: take는 "가져가다"가 아니라 "입력을 넘겨받아 처리하다"이다. 같은 문단 14줄이 이미 "Escape는 게임이 처리하며", "Escape를 WowVision이 처리합니다"라고 써서 "처리하다"가 이 설명서 안에서 이미 통하는 말이다.
- 덧붙임: 이 절의 navigation keys를 "이동 키"로 옮겼는데, 17줄의 movement key(캐릭터를 움직이는 키)도 "이동 키"다. 한 절 안에서 뜻이 다른 두 가지가 같은 말이 됐다. combat.md처럼 navigation keys는 "탐색 키", movement keys는 "이동 키"로 구분해야 10줄과 17줄이 통한다.

### 3) interface.md:13, 34 "창 사이를 오갑니다"

- 원문: Ctrl+Tab and Ctrl+Shift+Tab switch between them.
- 수정안: 창이 둘 이상 열려 있으면 Ctrl+Tab과 Ctrl+Shift+Tab으로 창을 전환합니다. 34줄: 열린 창을 전환합니다.
- 이유: 번역 지침이 switch는 "전환하다"로 정했고, 윈도 사용자에게 Ctrl+Tab은 "창 전환"으로 굳어 있다. "오가다"는 사람이 왕래하는 말이라 설명서 동사로 쓰이지 않는다.

### 4) interface.md:14 "한 단계 뒤로 가고, 첫 단계에 있으면 화면을 닫습니다"

- 원문: it goes back one level, or closes the screen when you are on the first level.
- 수정안: 이전 단계로 돌아가고, 첫 단계에서는 화면을 닫습니다.
- 이유: level은 메뉴의 깊이다. "뒤로"는 공간 방향으로 들려 캐릭터가 뒤로 가는 것과 섞인다. 낱말표의 "한 단계 이전으로"는 "뒤로"만 "이전으로"로 바꾼 꼴이라 "한 단계 이전으로 가고"가 여전히 어색하다. 한국어 어순은 "이전 단계로 돌아가다"다(3부 낱말표 수정 후보 2).

### 5) interface.md:76 "WowVision은 그 컨트롤을 지켜봅니다"

- 원문: While a control has focus, WowVision watches it. If its text, its checked state or its enabled state changes by itself, … the new value is spoken without you pressing anything.
- 수정안: WowVision은 초점이 있는 컨트롤의 상태가 달라지는지 계속 확인합니다. 텍스트, 체크 상태, 사용 가능 상태가 저절로 달라지면(…) 아무 키도 누르지 않아도 새 값을 읽습니다.
- 이유: "컨트롤에 초점이 있는 동안 … 그 컨트롤"은 같은 낱말을 지시어로 다시 받아 군말이 됐다. "초점이 있는 컨트롤"로 한 번에 말하면 지시어가 없어진다. watch는 프로그램이 값의 변화를 확인하는 동작이다. "지켜보다"는 사람이 눈으로 보는 말이라 스크린리더 사용자에게 특히 어색하다.

### 6) interface.md:125 "현재 선택지에 도착하며"

- 원문: Enter opens a short list of the choices. You land on the current one, which reads, for example, "…".
- 수정안: Enter를 누르면 선택지가 담긴 짧은 목록이 열립니다. 초점은 현재 선택된 항목에 놓이며, 예를 들어 "Microsoft Zira Desktop, 버튼, 선택됨"이라고 읽습니다.
- 이유: land on은 "초점이 그 항목에 놓인다"는 뜻이다. 설명서 다른 곳에 이미 맞는 번역이 있다(keybindings.md:12 "초점이 ~에 놓이고", social.md:61, professions). "현재 선택지"도 "현재 선택된 항목"이 귀에 분명하다.

### 7) interface.md:158 "Enter는 확정하고, Escape는 취소하며"

- 원문: Enter accepts, Escape cancels, and Tab accepts and moves on to the next control.
- 수정안: Enter를 누르면 입력한 내용이 적용되고, Escape를 누르면 입력이 취소되며, Tab을 누르면 입력한 내용이 적용된 뒤 다음 컨트롤로 넘어갑니다.
- 이유: accept의 목적어(입력한 내용)가 영어에서는 문맥으로 채워지지만 한국어 "확정하다"는 타동사라 목적어 없이는 뜻이 빈다. 키가 주어인 문장("Enter는 확정하고")은 "Enter를 누르면"으로 풀어야 누가 무엇을 하는지 들린다. 같은 뜻을 keybindings.md(reference):189가 "입력을 확정합니다"로 목적어를 넣어 옮겼다. "확정" 대신 "적용"을 고른 까닭은 설정 값 입력에서 Enter의 결과가 "값이 적용됨"이기 때문이다. "입력을 확정합니다"로 통일해도 뜻은 통한다(확신도 중간, 둘 중 하나로 통일).

### 8) controller.md "게임패드로도 WowVision을 쓸 수 있습니다"

- 수정안: 게임패드로도 WowVision을 사용할 수 있습니다.
- 이유: 기능·도구·키에 대한 use는 "사용하다"가 한국 소프트웨어 설명서의 표준이고, "쓰다"는 write와 소리가 같아 귀로 들을 때 한 박자 늦는다. 다만 전부 바꾸면 안 되는 예외가 있다(3부 낱말표 수정 후보 1).

---

## 2. 설명서 전체에 적용할 방침 (용어집 후보)

확신도 높은 것부터 적었다. 위치 목록이 긴 것은 5부의 해당 범위에 있다.

### 방침 1. 키 입력을 주고받는 은유: "처리하다"로 통일 (b, 높음, 약 45곳)

| 원문 | 지금 | 방침 |
|---|---|---|
| take (over) keys | 가져가다, 넘겨받다, 차지하다, 잡다, 받다 | (키 입력을) 대신 처리하다 |
| give / hand back, release | 돌려주다, 놓다 | 게임의 원래 기능으로 되돌리다 |
| take them again | 다시 가져가다, 다시 가져오다, 되찾다 | 다시 처리하다 |
| step aside, stay out of the way | 물러나다, 물러나 있다 | (키 처리를 / 작동을) 멈추다 |
| go to the game | 게임으로 가다 | 게임에 전달되다 |

- 대표: interface.md:219 "전투 중에는 게임이 키를 보호하므로 WowVision이 완전히 물러납니다. … 전투가 끝나면 바로 WowVision이 키를 다시 가져가고, 창과 초점은 떠났을 때 그대로입니다." → "전투 중에는 게임이 키를 보호하므로 WowVision은 키 처리를 모두 멈춥니다. … 전투가 끝나면 바로 WowVision이 키 입력을 다시 처리하고, 창과 초점은 전투 전 상태 그대로입니다."
- 위치(grep 전수): 가져가다 9줄(interface 8, 10, 17, 219, 247 / glossary 84 / chat 220 / combat 12, 172), 돌려주다 11줄(interface 193 / sku-login 190 / troubleshooting 57, 121 / commands 207 / glossary 84 / reference keybindings 13 / action-bars 15, 156 / overview 42 / combat 12), 물러나다 8줄(interface 219 / menu-and-settings 19 / combat 10 / targeting 223, 227, 236 / wownav 125, 198). 넘겨받다·차지하다·놓다·맡다 변종은 5부 각 범위의 "키 은유" 항목.
- 예외: wownav.md:125, 198 "관문에서 물러나기"는 비컨이 실제로 한 지점 뒤로 가는 koKR 설정 이름이라 그대로 둔다. targeting의 soft targeting steps aside는 "소프트 대상 지정이 작동하지 않는다"로 옮긴다.
- 본보기로 삼을 기존 문장: quick-start.md:41, troubleshooting.md:74, glossary.md:68, reference/keybindings.md:10, chat.md:209("키보드 입력을 받기 시작할 때").

### 방침 2. land on / arrive on / open on: "초점이 ~에 놓이다 / ~(으)로 이동하다" (b·c, 높음, 약 30곳)

- "도착하다"는 캐릭터가 실제 장소에 닿을 때와 데이터·메시지가 올 때만 쓴다(도착 80줄 중 66줄은 정상).
- 초점 뜻 14곳: interface.md 12, 48, 82, 88(2곳), 125, 131, 158, 160, 187, 213 / tooltips.md:24 / chat.md:121 / collections.md:52.
- 변환 규칙: "when you land on a control" → "컨트롤로 이동하면", "you land on X" → "초점이 X에 놓입니다", "where you have landed" → "초점이 놓인 위치", "arrive by Tab" → "Tab으로 이동해 오면".
- 주어 없는 "~에 놓입니다" 약 12곳(menu-and-settings 99, 116 / action-bars 22 / character 30, 90 / spells-and-talents 32, 47, 79, 118 등)은 "초점이"를 넣는다.
- "최신 메시지에서 열립니다"(chat 77), "등록 탭으로 열립니다"(group-finder 54, 142)는 "열리면 초점이 ~에 놓입니다".

### 방침 3. 창·화면 사이 이동 동사: switch는 "전환하다", move between/through는 "이동하다" (d, 높음)

- "오가다" 17줄 전부 교체. switch between → 전환하다(interface 13, 34 / auction-house 26 / loot-trade-mail 73), move·jump between, move through → "~ 사이를 이동하다"(나머지).
- navigation.md:239 step through the chain은 "연속 안내를 한 구간씩 넘깁니다"처럼 단순 치환이 안 된다(5부 world 1).
- 반대 방향 오류: switch를 "변경하다"로 옮긴 곳 약 15곳(chat 83, 237 / social 32, 102 / auction-house 51 / group-finder 28, 29 / spells 137, 170 / npcs 40 / character 32 등)은 "전환하다·이동하다"로 되돌린다. 2026-11-09 "바꾸다→변경하다" 일괄 치환의 잔재다.
- walk the list를 옮긴 "훑다, 돌아다니다, 따라가다"(character 4, 70, 74 / professions 4, 61 / spells 120, 170)도 "이동하다".

### 방침 4. go back one level: "이전 단계로 돌아가다" / 폴더는 "상위 폴더로" (d, 높음, 9곳)

- interface 14 / menu-and-settings 13, 14, 121(한 폴더 뒤로 → 상위 폴더로) / buffers 248, monitors 55(한 화면 뒤로 → 이전 화면으로 돌아갑니다) / reference keybindings 31 / controller 56 / monitors 328(뒤로 가서 → 이전 화면으로 돌아가서) / loot-trade-mail 134(Shift+Tab은 뒤로 갑니다 → 이전 정지점으로 갑니다).
- 그대로 두는 "뒤로": 게임 버튼 이름 "뒤로"(auction-house, group-finder, quests), koKR 문구 "경유지 하나 뒤로", 시간의 "그 뒤로는".
- auction-house.md:346 "초점이 뒤로에 놓입니다"는 "초점이 뒤로 버튼에 놓입니다"로 버튼임을 밝힌다.

### 방침 5. watch: UI는 "확인하다", 모니터 기능은 "감시하다" (b, 중간, 19곳)

- 컨트롤 변화: interface 76, 245 → "달라지는지 확인하다".
- 모니터: introduction 16 / information index 7 / monitors 4, 10, 112, 151 / glossary 40 / buffers 331 / movement 21 / wownav 115. koKR에 "파티 감시"가 있어 "감시하다"가 로케일과 맞는다. "대신 지켜보다가 알려 줍니다"는 뜻은 통하므로 확신도 중간이다. 통일만 해도 된다.

### 방침 6. 목적어를 비우지 않는다: accept "입력을 확정하다", 키가 주어인 문장은 필요할 때만 푼다 (c, 높음 6곳)

- "확정" 목적어 없음: interface 158 / menu-and-settings 100, 130 / first-login 13 / sku-login 74. 모두 "입력한 내용을", "선택을"을 넣는다.
- 키가 주어인 문장("Backspace는 채널 메뉴를 엽니다")은 본문에 약 100줄 있다. 목적어가 있고 뜻이 통하는 것은 그대로 둔다. 목적어가 빠졌거나 "Home과 End가 아무 일도 하지 않습니다"(interface 172 → 작동하지 않습니다)처럼 어색한 것만 고친다. 전부 "~를 누르면"으로 바꾸는 것은 과잉 수정이다.

### 방침 7. 지시어: 선행어와 사이에 낱말이 끼면 명사를 다시 말한다 (a, 높음)

- "그 창", "그 컨트롤", "그것을 고릅니다"(interface 125, menu-and-settings 99 → 해당 선택지를 선택합니다), "그곳에서는"(there가 게임 버전: quests 33, 84 / scanner 154 / getting-started 2곳 → 버전 이름을 다시 말한다).
- 바로 앞 낱말을 받는 "그 칸의 아이템", "그 항목"은 뜻이 통하므로 그대로 둔다.

### 방침 8. 그 밖의 반복 직역 (b, 중간)

| 원문 | 지금 | 방침 | 위치 |
|---|---|---|---|
| count as | ~로 치다 | ~로 간주하다 / 인식하다 / 포함하다 | 20줄(interface 88, controller 121, monitors 174·260, glossary 12, navigation 5곳, wownav 5곳 등) |
| fire (alert) | 울리다 | (알림이) 나오다 / 재생되다 | 23줄(alerts 7, monitors 9 등). 소리 알림의 "울리다"는 유지 가능, 음성 알림에 쓴 곳만 |
| the game draws | 그리다 | 표시하다 | action-bars 57 / bags 22, 109, 129, 134 / collections 132 |
| fills | 채우다 | 표시하다 / 표시되다 | professions 50 / collections 131 / spells 84 |
| data knows / unknown to | 모르는, 아는, 알려진 | 데이터에 있는 / 없는, 등록된 | navigation·wownav 9곳, scanner 79, 88, 119, minimap 61, combat 143 |
| silent, stays quiet | 조용하다, 조용히 있다 | 아무것도 읽지 않다 / 알리지 않다 | movement 41, 70, 75, 100 / npcs 141 등 |
| without asking | 묻지 않고 | 확인 없이 | interface 233 / keybindings 65 / menu-and-settings 148 / controller 129 / wownav 92 |
| hands you text | 건네줍니다 | 제공합니다 | interface 166 |
| notice, pick up | 알아차리다, 잡아내다 | 감지하다 | overview 10 / social 6 / chat 60, 66 |
| take / walk you to | 데려가다 | 안내하다 | navigation·wownav 4곳 |
| popup | 뜨다, 띄우다 | 열리다, 표시하다 | 8줄(npcs 30, loot 107, character 82, professions 70, chat 42·73, auction-house 90, group-finder 182) |
| share | 함께 쓰다 | 공유하다 | information 5곳 |
| pull | 당기다 | 전투를 시작하다(게임 은어 "풀링"은 사용자 판단) | combat 63, 100, 110 |

### 방침 9. 용어 통일 (e1, 높음: 설명서만 고치면 됨)

| 통일할 말 | 갈린 말과 위치 | 근거 |
|---|---|---|
| 체크 상자 | 확인란 15줄(alerts, tooltips, installation, sku-login, group-health, quests, scanner), 체크박스 1줄(collections 178) | koKR Checkbox 값, 번역 지침 |
| 상황별 메뉴 | 상황 메뉴 8줄(social 5, group-finder 3) | koKR Context Menu 값 |
| 초점 | 포커스 3줄(navigation 94, 309, 320) | 나머지 전부 |
| 보조 키 | 조합 키 5줄(speech 55, controller 17, 28, reference keybindings 37, 38) | 다수 |
| 탭 정지점 | 정지 지점 7줄(group-finder), 탭 위치 | 다수 |
| 불러오다 | 로드 16줄(sku, sku-login 중심) | 다수. "불러와지다" 이중 피동 5곳은 "불러온" |
| 탐색 키 / 이동 키 | interface.md는 둘 다 "이동 키" | combat.md의 구분 |
| 단축키 화면 | 단축키 창 | 사용자 판단(둘 중 하나) |
| 키 이름은 영어 | navigation 37, 83, 311 "위/아래", sku-login "오른쪽 화살표, 숫자 키패드 7" | 번역 지침 "키 이름은 번역하지 않음" |
| 컨트롤 | 조작 요소(system 51, 53, 61) | 다수 |
| 경로 계획 도구, 선택 목록 | 경로 계획기, 선택기 7줄 | 낱말표 "-기 행위자 이름 금지", koKR에 없음 |
| Retail | 리테일 1곳(menu-and-settings 87) | decisions 2026-11-07 |
| 참고하십시오 | 보십시오(bags-and-bank 6곳 등) | 다수 |

### 방침 10. 조사 오류 16곳 (e2, 높음, 기계적으로 고칠 수 있음)

"[알림](…)를", "[알림](…)와": menu-and-settings 48, 107 / speech 58, 76 / quick-start 61 / troubleshooting 44 / group-health 106 / monitors 53 / glossary 8, 42, 108 / chat 226 / system 168 / minimap 127, 173 / quests 128. "경보"를 "알림"으로 바꿀 때 조사가 따라가지 않았다. "을", "과"로 고친다.

### 방침 11. 사용자 결정이 필요한 대량 방침 (고치기 전에 확인)

1. 따옴표 없는 화면 문구·설정 이름이 문장에 녹는 곳(e3, 약 30곳). 예: navigation.md:107 "비컨 중지는 취소할 때 말합니다", 150 "여기서는 돌아서기 사용 불가가 들립니다", monitors "없음은 대체가 없습니다", buffers "내가 시전을 해당만으로 두면". 원문에 따옴표가 없어서 기호를 더할 수 없다. 후보: "~(이)라는 안내가 들립니다", 이름 뒤에 "설정·상태·필터"를 붙임. 뒤의 것은 원문에 없는 낱말을 더한다.
2. 무생물 주어 + 읽다(e4, 약 55곳과 제목 5개). "각 칸은 아이템 이름을 읽습니다", 제목 "칸이 읽는 내용". 후보: "칸마다 ~을 읽습니다", "칸에서 들리는 내용". 제목을 바꾸면 앵커와 링크도 바뀐다.
3. alerts.md 표 6개 약 40칸의 머리글과 칸 문형 불일치(5부 basics).
4. minimap.md에서 Scanner(F9 창)와 the scanner(미니맵 스캐너)가 모두 "스캐너"(약 20곳).
5. choose를 옮긴 "고르다"는 일관되고 뜻이 통해 수정 대상에서 뺐다. "선택하다"로 바꿀지는 사용자 판정.
6. 피동 "읽힙니다"(group-finder 29, auction-house 19)와 능동 "읽습니다" 통일 여부.

---

## 3. 낱말표 수정 후보 (fluent-korean.md 구 단위 2번 표를 독립 판정한 결과)

표를 설명서 실물에 대어 본 결과다. 항목 14개 중 그대로 맞는 것 8개, 범위나 형태를 고쳐야 하는 것 5개, 설명서에서 확인할 수 없는 것 1개다.

### 후보 1. 쓰다 → 사용하다: 방향은 맞고, 제외 범위를 표에 적어야 한다

- 판정: 기능·키·도구·설정에 대한 use는 "사용하다"가 맞다. 설명서에 "쓰다" 계열이 약 380곳 있고 그중 약 365곳이 이 뜻이다(씁니다 77, 쓰는 66, 쓸 수 있 50, 쓰십시오 25, 쓰기 23, 쓸 수 없 18, 쓰면 18 등. 파일별로는 buffers 30, navigation 25, sku-login 25, monitors 22 순).
- 일괄 치환하면 틀리는 곳(실물 확인):
  - write 뜻: installer.md:19 "게임 폴더에 파일을 쓰기 때문에", menu-and-settings.md:192 "디스크에 씁니다"(→ 저장합니다), navigation.md:169 "대화창에는 아무것도 쓰지 않습니다"(→ 표시하지 않습니다), reference/keybindings.md:107과 group-finder.md:46 "글을 쓰는", chat.md:132 "메시지를 쓴 플레이어", chat.md:154 "채널에 쓰기", buffers.md:212 "직접 쓴 글자".
  - spend 뜻: "포인트를 쓰다" 8곳(spells-and-talents 4, 11, 114, 116, 165, 184 / collections 186, 204). "포인트를 사용하다"도 틀리지는 않지만 게임 말로는 "투자하다·찍다"에 가깝다. 사용자 판단.
  - share 뜻: "함께 쓰다" 5곳은 "공유하다"다.
  - 굳은 말: 쓸모 6곳.
  - 피동 "쓰이다" 12곳은 "사용되다".
  - 제목 "WowVision과 Sku 함께 쓰기"는 링크 글자로 10곳에 반복되고 앵커(`#wow-forever에서-도구-쓰기` 등)에도 들어 있다. 제목을 바꾸면 앵커와 링크를 함께 바꿔야 한다.
- 표에 적을 말: "쓰다(기능·키·도구를 use) → 사용하다. 제외: 글·파일을 쓰다(write), 포인트·돈을 쓰다(spend), 쓸모·신경 쓰다 같은 굳은 말."

### 후보 2. 한 단계 뒤로 → 한 단계 이전으로: 오른쪽이 어색하다

- 판정: 왼쪽을 쓰지 않는 것은 맞다. 오른쪽 "한 단계 이전으로"는 "뒤로"만 갈아 끼운 꼴이라 "한 단계 이전으로 갑니다"가 여전히 번역체다. 설명서에 "이전으로"는 0건이라 아직 적용된 곳도 없다.
- 제안: "한 단계 뒤로 가다 → 이전 단계로 돌아가다". 대상이 폴더·메뉴 계층이면 "상위 폴더로·상위 메뉴로", 화면이면 "이전 화면으로".
- 범위 제한도 필요하다: 버튼 이름 "뒤로", 공간의 뒤(경유지 하나 뒤로), 시간의 "그 뒤로는"은 대상이 아니다.

### 후보 3. 바꾸다 → 변경하다: 자동사 "바뀌다"까지 넓힌 것이 과하다

- 판정: 사용자가 설정을 고치는 change는 "변경하다"가 맞다(165줄). 문제는 "변경되다" 82줄 가운데 누가 고친 것이 아니라 상태가 저절로 달라진 경우다. 예: group-health.md:92 "생명력이 변경되었을 때", movement.md:81 "위치가 거의 변경되지 않으면", controller.md:121 "대상이 변경되지 않습니다", information/index.md:7 "그것이 변경되면 알려 줍니다", auction-house.md:60 "버튼으로 변경됩니다"(turn into). "변경"은 누군가 고친다는 뜻이 강해서 생명력·위치·상태에는 "달라지다·변하다"가 자연스럽다.
- 또 switch·turn into·become까지 "변경"이 된 곳이 약 15곳 남아 있다(방침 3).
- 표에 적을 말: "바꾸다(설정·값을 고치다) → 변경하다. 저절로 일어나는 상태 변화(바뀌다)는 달라지다·변하다. switch는 전환하다, turn into는 ~(으)로 전환되다."

### 후보 4. 나뉘다 → 구분하다: 품사가 안 맞고 필요성이 낮다

- 판정: 왼쪽은 자동사, 오른쪽은 타동사라 그대로 갈아 끼울 수 없다. 설명서에 "나뉘다" 8줄이 남아 있는데(interface 92 "큰 창은 탭 정지점으로 나뉩니다", collections 124 "왼쪽 어깨와 오른쪽 어깨로 나뉩니다", bags 159 "페이지로 나뉘어") 모두 귀로 잘 통한다. "is divided into"의 "나뉘다"는 실제로 널리 쓰는 말이라 표의 기준("그 말을 쓰는 사람이 있는가")으로도 바꿀 이유가 약하다.
- 제안: 항목을 빼거나, "구분의 뜻일 때만 구분되다, 여러 부분으로 갈라지는 뜻은 나뉘다 유지"로 좁힌다.

### 후보 5. 뜨다 / 떠 있다 → 실행되다: 창·팝업에는 안 맞는다

- 판정: 프로그램에는 맞다. 설명서에 남은 8줄은 전부 창·팝업이다("팝업이 뜹니다", "떠 있는 창"). 여기에 "실행되다"를 넣으면 틀린다. 번역 지침도 이미 "창이 뜨다 → 열리다"로 따로 적었다.
- 표에 적을 말: "뜨다(프로그램이) → 실행되다, (창·팝업이) → 열리다·표시되다."

### 후보 6. 들어가다(포함) → 포함되다: 맞다. 경계만 적는다

- 포함 뜻 약 18곳은 고칠 대상이 맞다(5부 world 1, world 2). 다만 "칸에 들어 있는 아이템", "커서가 상자에 들어갑니다"처럼 실제로 안에 있는 뜻은 그대로 둔다. interface.md:187 "이름 어딘가에 그 글자들이 들어 있는"은 "포함된"이 맞다.

### 그대로 맞는 것

갱신 → 업데이트(36줄 적용됨. 오라 갱신과 버튼 이름은 예외로 이미 적혀 있다. koKR "개 아이템 갱신"은 4부), 배정 → 할당, 링크를 켜다, 설치기, 글 파일, 거절 → 취소(범위가 좁게 적혀 있다), 줄이 생김.

### 설명서로는 판정할 수 없는 것

방위 → 방향: 설명서와 koKR에 "방위"가 0건이라 실물로 볼 수 없다. 나침반 기능에서 북·북동 같은 말을 가리킬 때는 "방위"가 더 정확한 낱말이므로, 표를 유지한다면 "캐릭터가 향한 쪽, 대상이 있는 쪽"으로 범위를 좁혀 두는 편이 안전하다(추정, 근거는 낱말 뜻뿐이다).

---

## 3-1. interface.md 사례 목록 (직접 읽은 범위)

형식: 줄 | 부류 | 확신도 | 현재 | 원문 | 수정안

- 4 | a·c | 높음 | 예시 1
- 8, 10, 17 | b | 높음 | 예시 2
- 10, 17 | e1 | 높음 | "이동 키"가 navigation keys와 movement key 둘 다 | — | 탐색 키 / 이동 키로 구분
- 12 | b | 높음 | 창이 열리면 WowVision은 하던 말을 멈추고 지금 도착한 곳을 읽습니다 | stops any speech and reads where you have landed | 창이 열리면 WowVision은 읽던 것을 멈추고 초점이 놓인 위치를 읽습니다
- 13, 34 | d | 높음 | 예시 3
- 14 | d | 높음 | 예시 4
- 15, 36, 59, 113, 115, 193, 214, 247 등 13곳 | d | 높음 | 씁니다, 쓸 수 없습니다 | use | 사용합니다, 사용할 수 없습니다
- 21 | d | 중간 | 다른 키로 옮길 수는 있지만 완전히 없앨 수는 없습니다 | they can be moved to another key, but never removed completely | 다른 키로 변경할 수는 있지만 단축키를 완전히 삭제할 수는 없습니다
- 48 | b | 높음 | 컨트롤에 도착하면 | When you land on a control | 컨트롤로 이동하면
- 76 | a·b | 높음 | 예시 5
- 82 | b | 높음 | 이동한 행의 첫 컨트롤에 도착합니다 | you land on the first control of that row | 초점이 이동한 행의 첫 컨트롤에 놓입니다
- 88 | b | 높음 | 무언가 들어 있는 다음 칸에 도착합니다 … 마지막 칸에 도착하고 | You land on the next slot that has something in it | 비어 있지 않은 다음 칸으로 이동합니다 … 마지막 칸으로 이동하고
- 88 | b | 중간 | 두 번 누르기로 치지 않습니다 | does not count as a double press | 두 번 누르기로 인식하지 않습니다
- 92 | a | 중간 | Tab과 Shift+Tab으로 그 사이를 건너뛰고 | Tab and Shift+Tab jump between them | Tab과 Shift+Tab으로 탭 정지점 사이를 이동하고
- 92 | b | 중간 | 떠났던 항목으로 돌아갑니다 | return to the item you left | 마지막으로 있던 항목으로 돌아갑니다
- 125 | b·c | 높음 | 예시 6
- 125 | a | 높음 | 선택지에서 Enter를 누르면 그것을 고릅니다 | press Enter on a choice to pick it | 원하는 선택지에서 Enter를 누르면 그 선택지가 선택됩니다
- 131 | b | 높음 | 그 구역에서 처음 도착한 항목과 함께 한 번 읽습니다 | read once, together with the first entry you land on in that section | 그 구역에서 처음 이동한 항목을 읽을 때 함께 한 번 읽습니다
- 138 | b | 중간 | 게임이 그 항목에 툴팁을 줄 때만 해당합니다 | when the game gives it one | 게임이 그 항목에 툴팁을 제공할 때만 읽습니다
- 158 | c | 높음 | 예시 7
- 158, 160 | b | 높음 | Tab으로 도착하거나 | When you arrive by Tab | Tab으로 이동해 오거나
- 166 | b | 높음 | 일부 동작은 복사할 텍스트를 건네줍니다 | Some actions hand you a text to copy | 일부 동작은 복사할 텍스트를 제공합니다
- 172 | d | 중간 | Home과 End가 아무 일도 하지 않습니다 | Home and End do nothing | Home과 End가 작동하지 않습니다
- 187 | b | 높음 | 필터와 입력한 글자를 읽어 주는 줄에 도착하고 | You land on a line that says Filter and what you typed | 초점이 "필터"와 입력한 글자를 읽어 주는 줄에 놓이고 (따옴표는 원문에 없으므로 빼도 된다)
- 193 | b | 높음 | 전투에 들어가거나 목록을 닫을 때도 키를 게임에 돌려줍니다 | The keys are also released | … 글자 키를 게임의 원래 기능으로 되돌립니다
- 213 | b | 높음 | 도착한 창의 전체 경로 | the window you land on | 이동한 창의 전체 경로
- 214 | b | 중간 | 지금 쓰는 창의 초점을 빼앗지 않지만 | do not take focus away from the one you are using | 사용 중인 창에서 초점을 옮기지 않지만
- 219 | b | 높음 | 방침 1의 대표 문장
- 233 | b | 중간 | Delete를 누르면 묻지 않고 그냥 지웁니다 | without asking | Delete를 누르면 확인 없이 바로 지웁니다
- 245 | b | 높음 | 무엇을 지켜보는지 설명합니다 | what WowVision is watching | 어떤 변화를 확인하고 있는지 설명합니다
- 247 | b | 높음 | 가져가거나, 기다리거나, 돌려줄 때마다 | takes, waits for and releases | 키 입력을 처리하기 시작하거나, 기다리거나, 게임에 되돌릴 때마다

그대로 둔 것: 44 "읽을 말이 밀리지 않습니다", 63 "컨테이너가 겹겹이 들어 있는 구조", 127 "첫 항목에 초점을 둡니다", 229 "마우스로 할 때처럼 거부됩니다", 234 "소지품은 안전합니다". 뜻이 통한다.

---

## 4. 로케일 값 문제 (설명서만 고칠 수 없는 곳, 18건)

koKR 값을 고치면 설명서 인용은 `tools.sync_locale`이 따라간다. 확신도 높음부터.

| # | koKR 키 = 값 | 설명서 위치 | 문제 | 후보 | 확신도 |
|---|---|---|---|---|---|
| 1 | windows.lua:168 `Search Match` = "일치하는 항목 검색" | collections 192, spells-and-talents 100, 179 | 상태 표시인데 명령으로 들린다 | "검색 일치" | 높음 |
| 2 | ui.lua:216 `Controls` = "조작" | social 30, 51, 66 등 9곳, loot-trade-mail | "Tab으로 조작에 가서"가 구역 이름으로 안 들린다 | "컨트롤", "조작 버튼" | 중간 |
| 3 | `turn in` = "완료", `Complete` = "완료" | scanner 73, 77, 82, minimap 68, 152 | 퀘스트 상태와 완료 보고 대상 NPC가 같은 말 | turn in → "완료 보고" | 중간 |
| 4 | auction.lua:51 `items updated` = "개 아이템 갱신" | auction-house 211, 322 | 낱말표(갱신 → 업데이트)와 어긋남 | "개 아이템 업데이트" | 중간 |
| 5 | groupHealth.lua:19 `Repeat Below (percent)` = "이 값 미만일 때 반복 (퍼센트)" | group-health 41, 57, 96 | 이름 안의 "이 값"이 문장에 들어가면 지시어로 들린다 | "반복 기준 생명력 (퍼센트)" | 중간 |
| 6 | windows.lua:281 `Alert Editor` = "알림 편집기", 게임 공식은 "신규 경보", "경보 편집" | monitors 188 | 한 문장에서 같은 것이 알림과 경보 | 사용자 판단(alert=알림 결정의 예외 여부) | 중간 |
| 7 | Announce Errors = "오류 알림" + alert "알림" | combat 156 | "오류 알림 알림" | Announce 계열 이름(사용자 결정 사항) | 중간 |
| 8 | `Day Mean` = "일간 평균", 하이픈 | auction-house 220, 231 "7-일간 평균" | 코드가 하이픈을 넣는 것으로 추정(미확인: `L["Day Mean"]` 사용처) | 코드면 upstream-report | 중간 |
| 9 | ui.lua:221, 222 `New` = "새" / "신규", 종류 이름 "Aura" | monitors 49, 322, 335 | "신규 Aura"가 실제 화면과 같은지 미확인(게임에서 모니터 종류 목록 확인) | 영어가 실제로 나오면 upstream-report | 중간 |
| 10 | monitors.lua:59 `Missing` = "없음" | monitors 여러 곳 | 주어로 쓰면 "없음은 대체가 없습니다" | 로케일 유지, 설명서에서 "없음 상태" | 낮음 |
| 11 | buffers.lua:26~28 Any/Only/Not = "전체", "해당만", "제외" | buffers 122, 135, 328, 373 | "해당만으로 두면" | 로케일 유지, 설명서에서 풀기 | 낮음 |
| 12 | buffers.lua:22, 29 "내 오라만", "내가 시전" | buffers 135 | 조사가 붙으면 이름으로 안 들림 | 위와 같음 | 낮음 |
| 13 | navigation.lua:102 "Alt Gr로 거리 알림" | reference keybindings 107 | 이름의 "로"가 문장 조사와 겹침 | 설명서 어순으로 완화 | 낮음 |
| 14 | navigation.lua:267 `Riding to the noted dock %s` = "기록한 %s까지 타고 가는 중" | wownav 139, 164 | noted는 "기억해 둔" | "기억해 둔 %s까지 …" | 낮음 |
| 15 | auction.lua:61 `Vendor price per item` = "개당 상인에게 파는 가격" | auction-house 326 | "개당"이 "상인"을 꾸미는 것처럼 들림 | "상인에게 파는 개당 가격" | 낮음 |
| 16 | `Link %s in Chat` = "대화창에 %s 링크 걸기" | chat 155, interface 42, 201은 "링크 넣기" | 설명서와 화면 문구가 갈림 | 설명서를 "링크 걸기"로 맞춤 | 낮음 |
| 17 | ui.lua:69 `Available` = "사용 가능" | auction-house 260, 271, 345 | 기결정(decisions 2026-11-09, 원본 PR 대기) | 병합 뒤 따라 고침 | 기결정 |
| 18 | Enabled / Disabled | targeting 191 | SettingDisabled 병합 뒤 실제 발화와 대조할 곳 | 지금은 유지 | 참고 |

그 밖에 설명서 쪽에서 로케일과 어긋난 곳(설명서만 고치면 됨): 확인란 → 체크 상자, 상황 메뉴 → 상황별 메뉴, quests.md의 "출처" → koKR "원본"(data source), auction-house 318, 319의 "12 min 30 sec"(koKR "%s분 %s초").

미확인: installer.md의 버튼 이름은 설치 프로그램 Loc.cs 값이라 대조하지 않았다. social.md의 "갱신", "쪽지 설정", auction-house의 "새로고침"은 게임 자체 버튼 이름으로 보이며 `cache/gs_koKR.csv` 대조가 필요하다.

---

## 5. 범위별 사례 목록 (원자료)

아래는 범위 7개를 영어와 대조해 끝까지 읽은 결과를 그대로 붙인 것이다. 사례 형식은 `파일:줄 | 부류 | 확신도 | 현재 | 원문 | 수정안 | 이유`이고, 부류 기호 (e)의 번호는 범위마다 따로 붙어 있다. 범위별 "로케일 값 문제" 절은 위 4부에 합쳤다.


---

### getting-started 감수 결과 (포크)

범위: ko/getting-started/ 10개 파일(introduction, installation, installer, manual-installation, first-login, quick-start, managing, sku, sku-login, troubleshooting)을 en과 한 쌍씩 끝까지 대조했다. 줄 번호는 ko 파일 기준.

부류: (a) 지시어 (b) 관용구·은유 직역 (c) 목적어·주어 생략 (d) 동사 선택 (e1) 파일 사이 용어 불일치 (e2) 귀로 들을 때 다른 말로 들림(동음·수식 구조) (e3) 조사 오류

형식: `파일:줄 | 부류 | 확신도 | 현재 | 원문 | 수정안 | 이유`

#### 1. 개별 사례

##### introduction.md
- introduction.md:16 | c+b | 중간 | "대신 지켜봅니다." | It watches things for you. | "상태 변화를 대신 감시합니다." | 문단 첫 문장인데 목적어가 없어 무엇을 지켜보는지 비어 있다. 바로 뒤에 "모니터"가 나오므로 "감시"가 기능 이름과도 이어진다.
- introduction.md:18, 40 / quick-start.md:6, 49 | e1 | 높음 | "세상 속에서 길을 안내합니다", "캐릭터가 세상에 들어간 뒤", "게임 세계 안에", "세상에 귀 기울이기" | the world | "월드"로 통일(예: "월드에서 길을 안내합니다", "캐릭터가 월드에 들어간 뒤", "5단계: 월드의 소리 듣기") | 같은 the world가 installation·first-login·sku-login에서는 "월드"(월드에 들어간 뒤), introduction 47줄 링크도 "월드에서"다. 세상·게임 세계·월드 세 가지로 갈려 있다.

##### installation.md
- installation.md:4 | e2 | 높음 | "이 페이지에서는 둘 중 하나를 고르도록 돕고, 어느 방법으로 설치하든 그다음에 할 일인 WowVision과 함께 쓰는 애드온, 그리고 애드온을 켜는 방법을 다룹니다." | This page helps you choose one, and covers what comes after either: the addons WowVision works with, and switching the addon on. | "이 페이지에서는 두 방법 중 하나를 고를 수 있게 안내합니다. 그리고 어느 방법으로 설치하든 그 뒤에 알아야 할 두 가지를 설명합니다. WowVision과 함께 사용하는 애드온, 그리고 애드온을 켜는 방법입니다." | "그다음에 할 일인 WowVision과 함께 쓰는 애드온"이 귀로는 "할 일인 WowVision"으로 붙어 들린다. 원문의 콜론 구조를 문장 나누기로 살린다.
- installation.md:35 | d+e1 | 중간 | "이제는 게임의 애드온 목록에 있는 구버전 애드온 불러오기 확인란을 켜도 불러오게 되지 않습니다." | the Load out of date AddOns check box ... no longer changes that | "이제는 게임의 애드온 목록에 있는 구버전 애드온 불러오기 체크 상자를 체크해도 게임이 그 애드온을 불러오지 않습니다." | "불러오게 되지 않습니다"는 주어·목적어가 다 빠진 피동. check box는 translation-guide에서 "체크 상자"로 정해져 있는데 여기와 sku-login.md:114만 "확인란"이다.
- installation.md:37 | c | 높음 | "설치 프로그램으로 설치한 경우: 실행할 때마다 WowVision의 TOC를 게임의 패치에 맞춥니다." | With the installer: it matches WowVision's TOC to your game's patch on every run. | "설치 프로그램으로 설치한 경우: 설치 프로그램은 실행될 때마다 WowVision의 TOC를 게임의 패치에 맞춥니다." | 무엇을 실행하는지, 누가 맞추는지 주어가 없다. 사용자가 직접 맞춰야 하는 것으로 들린다.
- installation.md:38 | c | 중간 | "보통 패치가 나오고 얼마 지나지 않아 업데이트됩니다." | It is normally updated soon after a patch. | "WowVision은 보통 패치가 나온 뒤 곧 업데이트됩니다." | 주어(WowVision)가 빠져 무엇이 업데이트되는지 앞 문장에서 찾아야 한다.

##### installer.md
- installer.md:8, 81 / sku-login.md:85 | d | 중간 | "게임의 \"사용자 제작 스크립트를 허용하시겠습니까?\" 질문을 끕니다", "질문 없음", "내레이터 질문을 끄고" | turns off the game's "run this script?" question | "... 질문이 나오지 않게 합니다" / 81줄 "... 질문이 나오지 않게 하는 설정" / "내레이터 질문이 나오지 않게 하고" | 질문은 켜고 끄는 대상이 아니다. "질문을 끄다"는 turn off 직역. (따옴표 안 문구 자체는 게임 문구 인용이므로 그대로 둔다.)
- installer.md:32 | b | 낮음 | "게임 버전, 폴더, 구성 요소를 직접 고르는 긴 방법입니다." | the longer way | "... 직접 고르는, 단계가 더 많은 방법입니다." | "긴 방법"은 뜻은 통하나 어색.
- installer.md:45 | c | 중간 | "어떤 게임 버전용 빌드가 없는 애드온은 그 사실을 알리고 그 게임 버전에서는 건너뜁니다." | an addon that does not exist for one of your game versions says so and is skipped there | "어떤 게임 버전용 빌드가 없는 애드온은 설치 프로그램이 그렇다고 알리고, 그 게임 버전에서는 설치하지 않고 건너뜁니다." | 애드온이 알리고 애드온이 건너뛰는 것처럼 들린다. "그 사실", "그 게임 버전" 지시어가 연달아 온다.
- installer.md:49 | a | 중간 | "이것은 Sku Login Tool입니다." | It is the Sku Login Tool | "Sku Login Tool과 같은 프로그램입니다." | 앞 문장이 길어 "이것"이 WoW Login Tool을 가리키는지 바로 안 잡힌다. 두 이름이 같은 프로그램이라는 뜻을 드러낸다.
- installer.md:58 | b | 중간 | "반쯤 기록된 채로 남는 것은 없습니다." | nothing is left half written | "쓰다 만 파일은 남지 않습니다." | half written 직역. 무엇이 반쯤 기록되는지(파일)가 없다.
- installer.md:7 | d | 낮음 | "게임이 패치된 뒤에도 WowVision이 그대로 불러와집니다." | so a game patch does not stop WowVision from loading | "게임이 패치된 뒤에도 게임이 WowVision을 정상적으로 불러옵니다." | "불러와지다" 이중 피동(같은 꼴: quick-start.md:12, manual-installation.md:61, 95, troubleshooting.md:10 제목과 그 앵커). 제목·앵커는 링크가 걸려 있어 함께 바꿔야 하므로 방침으로만 올린다.

##### manual-installation.md
- manual-installation.md:12 | b | 중간 | "zip 이름은 버전을 따릅니다(예: WowVision-V1.0.0.zip)." | The zip is named after the version | "zip 이름에는 버전 번호가 포함됩니다(예: WowVision-V1.0.0.zip)." | named after 직역. "이름이 버전을 따른다"는 뜻이 안 잡힌다.
- manual-installation.md:24 | b | 낮음 | "다른 지도 데이터 애드온도 그 옆에 설치할 수 있습니다." | can be installed beside them | "... 함께 설치할 수 있습니다." | "그 옆에"는 공간 은유 직역. (57줄 "게임 버전 폴더들 옆에"는 실제 폴더 위치라 유지.)

##### first-login.md
- first-login.md:6 / sku-login.md:4 | b | 중간 | "이 화면들에 접근할 수 있게 만들 수 있는 것은 게임 자체뿐입니다." | only the game itself could make them accessible | "이 화면들의 접근성은 게임만이 제공할 수 있습니다." | "~수 있게 만들 수 있는 것"이 겹쳐 귀로 따라가기 어렵다. accessible은 "접근 가능"이 아니라 접근성 지원의 뜻.
- first-login.md:8 | b | 중간 | "이 화면들에 음성 메뉴를 붙여 줍니다." | gives these screens a spoken menu | "이 화면들에 음성 메뉴를 제공합니다." | "붙여 주다"는 은유. installer.md:49는 같은 내용을 "소리 메뉴를 제공하는"으로 썼다.
- first-login.md:13 / sku-login.md:75 | c | 높음 | "Right로 들어가고, Up과 Down으로 고른 다음 Enter로 확정합니다." / "오른쪽 화살표로 들어가고, 위아래 화살표로 고르고, Enter를 눌러 확정합니다." | Right goes in, Up and Down choose, Enter confirms | "Right로 항목에 들어가고, Up과 Down으로 값을 고른 다음 Enter로 선택을 확정합니다." | 사용자 예시 7과 같은 문제. 어디에 들어가고 무엇을 확정하는지 목적어가 없다.
- first-login.md:32, 54 / sku-login.md:85 | b | 낮음 | "사용자가 고른 값을 건드리지 않습니다", "단축키, 카메라, 소프트 대상, 소리 크기는 건드리지 않습니다", "도구는 설정을 건드리지 않고" | leaves alone / are not touched | "변경하지 않습니다" | "건드리다"는 구어 은유. 뜻은 통하므로 우선순위 낮음.
- first-login.md:45 | e2+d | 높음 | "또 기존 캐릭터가 새 줄을 추가하는 업데이트 후 처음 로그인하면, 일반 버퍼에 새 줄 몇 개(빈 가방 칸, 내구도, 우편, 귀환석, 게임 시계)가 생깁니다." | The General buffer also gains a few new lines (...) the first time an existing character logs in after an update that adds them. | "또 버퍼 줄을 새로 추가하는 업데이트를 설치한 뒤 기존 캐릭터로 처음 로그인하면, 일반 버퍼에 새 줄 몇 개(빈 가방 칸, 내구도, 우편, 귀환석, 게임 시계)가 추가됩니다." | 귀로는 "기존 캐릭터가 새 줄을 추가하는"으로 묶여 들린다. "줄이 생김 → 추가됨"은 사용자 낱말 결정표 항목.
- first-login.md:62 | c | 중간 | "/wv speech를 포함해 입력할 수 있는 모든 것." | everything you can type, including /wv speech | "/wv speech를 포함해 입력할 수 있는 모든 명령." | "모든 것"이 무엇인지 비어 있다.

##### quick-start.md
- quick-start.md:56 | b | 중간 | "떨어질 때 올라가는 음, 벽에 부딪힐 때 쿵 소리" | rising tones when you fall | "떨어질 때 점점 높아지는 음, 벽에 부딪힐 때 쿵 소리" | "떨어질 때 올라가는"이 방향 모순처럼 들린다. rising은 음높이. (introduction.md:38은 "떨어질 때의 신호음"으로 문제없음.)
- quick-start.md:61 / troubleshooting.md:44 | e3 | 높음 | "[알림](../basics/alerts.md)를 보십시오." / "... 를 참고하십시오." | See [Alerts] | "[알림](../basics/alerts.md)을 ..." | 받침 있는 "알림" 뒤 조사 오류. getting-started의 링크 뒤 조사 전체를 grep으로 확인했고 이 2건뿐이다.

##### managing.md
- managing.md:8 | d | 중간 | "게임은 플레이 중에는 이 파일을 기록하지 않고, 로그아웃하거나 /reload를 입력할 때 기록합니다." | The game writes them when you log out or type /reload, not while you play. | "게임은 플레이 중에는 이 파일을 저장하지 않고, 로그아웃하거나 /reload를 입력할 때 저장합니다." | "파일을 기록하다"는 write 직역. troubleshooting.md:92, 160은 같은 내용을 "저장"으로 썼다.
- managing.md:22 | d+e1 | 중간 | "기본적으로 대부분의 설정은 모든 캐릭터가 함께 씁니다." | shared by all your characters | "기본적으로 대부분의 설정은 모든 캐릭터가 공유합니다." | 같은 문단 뒤쪽과 troubleshooting.md:95는 "공유"다.

##### sku.md
- sku.md:4 / sku-login.md:275 | b | 중간 | "두 애드온은 같은 창을 두고 다투지 않습니다." / "둘이 키를 두고 다투지 않도록" | They do not fight over the same windows | "두 애드온은 같은 창에서 충돌하지 않습니다." / "두 애드온의 키가 충돌하지 않도록" | fight over 의인화. 소프트웨어 설명서에서는 "충돌".
- sku.md:4 | b | 낮음 | "WowVision과 Sku는 나란히 설치할 수 있고" | side by side | "함께 설치할 수 있고" | 공간 은유. 뜻은 통한다.
- sku.md:8 / troubleshooting.md:88 | b | 중간 | "이 기능들의 WowVision 설정과 단축키는 그대로 남아 있다가 Sku를 끄면 바로 돌아옵니다." | come back as soon as Sku is off | "... 그대로 남아 있다가 Sku를 끄면 바로 다시 적용됩니다." | 설정이 "돌아온다"는 come back 직역. 지워졌다가 복구되는 것처럼 들리는데 실제로는 지워지지 않는다.

##### troubleshooting.md
- troubleshooting.md:21 | b | 중간 | "... 오래된 사본은 게임을 혼란스럽게 할 수 있습니다." | can confuse the game | "... 오래된 사본이 있으면 게임이 애드온을 제대로 불러오지 못할 수 있습니다." | confuse the game 의인화.
- troubleshooting.md:30 | c | 중간 | "첫 번째 목소리, 보통 속도, 최대 음량을 고릅니다." | That chooses the first voice, the normal rate and full volume. | "이 명령은 첫 번째 목소리, 보통 속도, 최대 음량으로 설정합니다." | 주어(That=명령)가 빠져 사용자가 또 골라야 하는 단계로 들린다. 41줄 "/wv speech 1 9 100은 ... 고릅니다"는 주어가 있어 통한다.
- troubleshooting.md:33 | c | 높음 | "직접 끊었습니까?" | Did you cut it yourself? | "음성을 직접 끊지 않았습니까?" | 목적어가 없어 무엇을 끊었는지 알 수 없다.
- troubleshooting.md:35 | d | 중간 | "음성이 한참 뒤에 막히거나 멈춥니까? ... 음성이 막히면 그 설정을 변경합니다." | Speech stalls or stops after a while? ... If speech stalls, switch that setting. | "음성이 얼마 지나면 끊기거나 멈춥니까? ... 음성이 끊기면 그 설정을 다른 값으로 전환합니다." | 음성이 "막히다"는 어색. switch는 규칙상 전환(변경은 change일 때만).
- troubleshooting.md:60 | b+c | 높음 | "WowVision은 자기가 쓰는 키가 모두 떼어질 때까지 기다렸다가 키를 넘겨받습니다. 키에서 손을 뗀 입력을 게임이 놓치지 않게 하려는 것입니다." | WowVision waits to take its keys until every key it uses is released, so that the game never misses a key release. | "WowVision은 자신이 사용하는 키에서 사용자가 모두 손을 뗄 때까지 기다린 다음에 그 키를 처리하기 시작합니다. 키에서 손을 뗀 것을 게임이 놓치지 않게 하기 위해서입니다." | "키가 떼어지다", "손을 뗀 입력"은 key release 직역이라 귀로 안 잡힌다. interface.md:17은 같은 내용을 "손을 뗄 때까지"로 썼다.
- troubleshooting.md:76 | b | 중간 | "... 그 키에서 손을 뗀 입력을 게임이 놓쳤다는 뜻입니다." | the game missed its release | "... 그 키에서 손을 뗀 것을 게임이 인식하지 못했다는 뜻입니다." | 위와 같음.
- troubleshooting.md:95 | c | 중간 | "다른 범위에 속해 있습니다." | They belong to another scope. | "설정이 다른 범위에 속해 있습니다." | 목록 항목 첫 문장인데 주어가 없다.
- troubleshooting.md:111 | b | 중간 | "특정 게임 메시지(...)만 조용히 하려면" | To silence only certain game messages | "특정 게임 메시지(...)만 읽지 않게 하려면" | silence 직역. 메시지를 "조용히 하다"는 맞지 않는다.
- troubleshooting.md:130 | d | 낮음 | "한 경유지 전으로 돌아갑니다." | Go back one waypoint | "이전 경유지로 돌아갑니다." | 바로 뒤 문장이 "이전 경유지로 옮깁니다"이고 koKR 키 이름도 "이전 경유지"다.
- troubleshooting.md:141 | b | 중간 | "무엇을 했는지, 무엇이 들릴 거라 예상했는지, 대신 무슨 일이 일어났는지." | what happened instead | "... 실제로는 무슨 일이 일어났는지." | instead를 "대신"으로 옮기면 누구 대신인지로 들린다.
- troubleshooting.md:151 | b | 높음 | "문제를 보여 주기 직전에 /wv padlog, 그 뒤 /reload" | /wv padlog just before you show the problem | "문제를 재현하기 직전에 /wv padlog, 그 뒤 /reload" | show the problem 직역. 누구에게 보여 주는지 없고, 버그 신고 문맥에서는 "재현".

##### sku-login.md
- sku-login.md:4, 25, 148 | a | 중간 | "이 도구가 그곳에서도 도움이 됩니다", "그곳에서는 도구가 화면을 읽어 주지 않습니다", "그곳에서 플레이하기 전에" | there | "WoW: Forever에서도 이 도구가 도움이 됩니다", "WoW: Forever에서는 도구가 ...", "그 서버에서 플레이하기 전에" | 게임 버전과 서버를 "그곳"으로 받아 장소처럼 들린다. 가리키는 이름을 다시 말하는 편이 귀에 바로 잡힌다.
- sku-login.md:52 | c | 중간 | "WoW: Forever, 불타는 성전 기념 서버, Classic Era용으로 도구를 설치하고, 필요한 AutoHotkey를 함께 설치하고, ... 바로 가기를 만듭니다." | It installs the tool for ... | "설치 프로그램은 WoW: Forever, ... 바로 가기를 만듭니다." | 긴 문장에 주어가 없어 사용자가 할 일의 나열로 들린다.
- sku-login.md:85~86, 257 | c | 중간 | "내 음성 대신 게임의 기본 음성이 들리면", "게임이 내 음성으로 말하게 합니다" | instead of yours / with your voice | "내가 고른 음성 대신 ...", "게임이 내가 고른 음성으로 말하게 합니다" | "내 음성"은 사용자의 목소리로 들린다. 도구에서 고른 음성이라는 뜻.
- sku-login.md:85 | b | 중간 | "도구는 설정을 건드리지 않고 그에 대해 아무 말도 하지 않습니다." | leaves the settings alone and says nothing about it | "도구는 설정을 변경하지 않고 아무 안내도 하지 않습니다." | "그에 대해"는 about it 직역.
- sku-login.md:116, 193, 216, 224, 225 | b | 중간 | "화살표 키는 게임으로 가므로", "그 밖에는 게임으로 가므로", "이 키들이 게임으로 갑니다", 표의 "게임으로 감" | go to the game | "게임에 전달되므로", "게임에 전달됩니다", "게임에 전달됨" | 키가 "간다"는 go to 직역. 같은 파일 191줄은 이미 "게임에도 전달됩니다"로 썼다.
- sku-login.md:139 | c | 중간 | "영상이 끝나면 월드에 서 있게 되고 WowVision이 넘겨받습니다." | WowVision takes over | "영상이 끝나면 캐릭터가 월드에 서 있고, 그때부터 WowVision이 안내를 맡습니다." | 무엇을 넘겨받는지 없다. 같은 파일 265, 270줄은 "WowVision이 맡습니다"로 썼다.
- sku-login.md:141 | c | 높음 | "캐릭터가 많은 서버에서는 세는 데 몇 초가 걸릴 수 있습니다." | Counting a realm with many characters can take several seconds. | "캐릭터가 많은 서버에서는 캐릭터 수를 세는 데 몇 초가 걸릴 수 있습니다." | 목적어가 없어 "세는 데"가 무슨 말인지 귀로 안 잡힌다.
- sku-login.md:160 | d | 중간 | "오른쪽 화살표로 더 들어가고 왼쪽 화살표로 한 단계 돌아갑니다." | Use Right to go deeper and Left to step back. | "오른쪽 화살표로 다음 단계에 들어가고 왼쪽 화살표로 한 단계 이전으로 돌아갑니다." | 사용자 낱말 결정표 "한 단계 뒤로 → 한 단계 이전으로"와 같은 부류.
- sku-login.md:170 | e2 | 높음 | "도구는 규칙을 한 쪽씩 읽고" | reads the rules page by page | "도구는 규칙을 한 페이지씩 읽고" | 귀로는 "한쪽씩"(한 편씩)으로 들린다. 설명서 다른 곳은 모두 "페이지"다.
- sku-login.md:187 | b | 중간 | "도구가 이름을 붙일 수 없는 화면을 만나면" | If the tool meets a screen it cannot name | "도구가 알아보지 못하는 화면이 나오면" | meets, cannot name 직역. 같은 파일 284줄은 "도구가 모르는 화면"으로 썼다.
- sku-login.md:188 | b | 중간 | "목록 끝에서는 커서가 반대쪽 끝으로 돌아갑니다." | At the ends of the list the cursor goes around. | "목록 끝에서는 커서가 반대쪽 끝으로 넘어갑니다." | "돌아가다"는 원래 있던 곳으로 간다는 뜻으로 들린다.
- sku-login.md:190 | b | 높음 | "입력한 다음 Enter나 Escape를 누르면 키보드를 도구에 돌려줍니다." | to give the keyboard back to the tool | "입력한 다음 Enter나 Escape를 누르면 입력 모드가 끝나고 도구가 다시 키를 처리합니다." | 사용자 예시 2("키를 가져가다")와 같은 부류. 키보드를 "돌려준다"는 뜻이 안 통한다.
- sku-login.md:194 | d | 높음 | "Enter World 버튼을 누르면 도구가 Play mode로 변경됩니다." | switches the tool to Play mode | "... 도구가 Play mode로 전환됩니다." | 규칙: switch는 전환, 변경은 change일 때만. 같은 파일 95~96줄은 "전환"이다.
- sku-login.md:215 | b | 중간 | "Login mode에서, 그리고 처음 설정하는 동안 도구가 다음 키를 받습니다." | the tool takes these keys | "... 도구가 다음 키를 처리합니다." | "키를 가져가다" 부류. 부모의 방침에 맞춰 통일.
- sku-login.md:255 | e2 | 높음 | "### 도구가 게임에 쓰는 것" | What the tool writes to the game | "### 도구가 게임에 기록하는 것" | 제목만 들으면 "사용하는 것"으로 들린다(쓰다=write/use 동음). 바로 아래 본문은 "써 넣어"라 통한다. 이 제목으로 걸린 앵커 링크는 getting-started 안에 없다.
- sku-login.md:274 | d | 중간 | "WowVision은 Sku 애드온을 선택 애드온으로 나열하지만, 로그인 도구와는 연동하지 않습니다." | WowVision lists the Sku addon as an optional addon. It does not use the login tool. | "WowVision은 Sku 애드온을 선택 애드온으로 등록해 두었지만, 로그인 도구는 사용하지 않습니다." | lists 직역. installation.md:15는 같은 내용을 "선택 애드온으로 등록되어"로 썼다.
- sku-login.md:275 | d | 중간 | "BlindSlash가 로드되어 있으면 이 두 명령은 없습니다." | These two commands do not exist when BlindSlash is loaded. | "BlindSlash를 불러온 상태에서는 이 두 명령을 사용할 수 없습니다." | troubleshooting.md:85가 같은 내용을 이렇게 썼다.
- sku-login.md:295 | b | 낮음 | "로그를 챙기십시오." | Take the log. | "로그를 준비하십시오." | 구어 표현.

#### 2. 반복 표현 → 위치 목록 + 방침 제안

1. **"키를 가져가다" 부류(take / take over / hand back / give back / belong to)**: 이 폴더에서는 "가져가다"가 아니라 넘겨받다·돌려주다·가져오다·받다로 옮겨져 있다.
   - 위치: sku.md:8, 60(키를 넘겨받지 않습니다) / troubleshooting.md:57(게임에 돌려주고 ... 다시 가져옵니다), 60(키를 넘겨받습니다), 121(창 버튼을 게임에 돌려줍니다) / sku-login.md:190(키보드를 도구에 돌려줍니다), 215(키를 받습니다)
   - 이미 잘 옮긴 본보기: quick-start.md:41 "열린 창이 없을 때는 이 키들이 다시 게임 키가 되므로", troubleshooting.md:74 "화살표 키가 창 조작에 쓰입니다", troubleshooting.md:52 "이 키들은 게임에 설정된 대로 작동합니다".
   - 방침 제안: "WowVision이 키를 처리한다 / 키가 게임 기능으로 돌아간다(게임 키로 작동한다)"로 통일. sku.md의 "넘겨받지 않습니다"는 "처리하지 않습니다"로.
2. **"도착하다 / land on"**: getting-started에는 "도착" 직역이 없다. 좋은 본보기가 있다: sku-login.md:146 "끝나면 커서가 첫 서버에 놓입니다"(Then you are on the first realm). troubleshooting.md:125, 131의 "도착한 것으로 처리"는 경유지 도착이라 정상.
3. **"오가다", "한 단계 뒤로", "지켜보다"**: "오가다" 0건. "한 단계 뒤로" 0건(같은 부류 sku-login.md:160 "한 단계 돌아갑니다" 1건, 위 사례). "지켜보다"는 introduction.md:16(위 사례), sku-login.md:269 "화면을 지켜보기만 하고"(실제로 화면을 보는 도구라 유지).
4. **로드 / 불러오다(load) 불일치 (e1, 높음)**: sku.md 전체(4, 8, 10, 12 제목, 60줄)와 sku-login.md:265, 275, 276은 "로드", 나머지 파일(installation, installer, first-login, troubleshooting, quick-start)은 "불러오다". 같은 문장이 파일에 따라 "Sku가 로드되어 있으면"(sku.md) / "Sku를 불러온 상태에서는"(installation.md:19, troubleshooting.md:62, 80)로 갈린다. 방침 제안: "불러오다"로 통일(다수이고 "구버전 애드온 불러오기" 표기와 맞다). sku.md:12 제목은 앵커 링크 확인 필요.
5. **동작하다 / 작동하다(work) 불일치 (e1, 낮음~중간)**: sku.md, sku-login.md, manual-installation.md:22, installation.md:15는 "동작", 나머지는 "작동". 방침 제안: 하나로 통일(다수는 "작동").
6. **키 이름 표기 불일치 (e1, 높음)**: sku-login.md는 화살표 키를 "오른쪽 화살표, 왼쪽 화살표, 위아래 화살표, 숫자 키패드 7"로 옮겼고(75, 110~111, 133, 137~138, 159~160, 188~193, 203~205줄, 키 표 219~230줄), 같은 절차를 요약한 first-login.md:13~15는 "Right, Up과 Down"이다. translation-guide `## 용어` 5번은 키 이름을 영어 그대로 두라고 한다. 원문도 "Right", "Up and Down", "Numpad 7"이다. 방침 제안: sku-login.md를 Right / Left / Up / Down / Numpad 7로 맞춘다.
7. **"게임으로 가다"(go to the game)**: sku-login.md:116, 193, 216, 224, 225 → "게임에 전달되다"(위 사례).
8. **"월드 / 세상 / 게임 세계"(the world)**: 위 introduction 사례. "월드"로 통일.
9. **"확인란 / 체크 상자"(check box)**: installation.md:35, sku-login.md:114 → "체크 상자".
10. **"불러와지다" 이중 피동**: installer.md:7, quick-start.md:12(본문과 앵커), manual-installation.md:61, 95, troubleshooting.md:10(제목). 방침 제안: "게임이 WowVision을 불러오지 않음/못함"으로. 제목과 앵커가 걸려 있어 일괄로 처리해야 한다(first-login.md:61은 이미 "게임이 WowVision을 불러오지 못하거나"로 썼다).
11. **"돌아오다"(come back, 설정·데이터)**: sku.md:8, troubleshooting.md:88(다시 적용됩니다), troubleshooting.md:94 "그러면 돌아오는 경우가 많습니다"(→ "그러면 다시 나타나는 경우가 많습니다", 낮음).
12. **"고르다"(choose / pick)**: 이 폴더에서 버튼·항목 선택에 일관되게 "고르다"를 쓴다(installer.md 여러 곳, sku-login.md 여러 곳). 뜻은 잘 통하고 일관되므로 수정 대상으로 올리지 않는다. 다만 소프트웨어 설명서 관례는 "선택하다"라서, 사용자가 "쓰다→사용하다"와 같은 판정을 내릴지 물어볼 만한 후보다(방침 질문).

#### 3. 로케일 값 문제

getting-started에서 따옴표 안 화면 문구나 설정 이름 자체가 원인인 사례는 찾지 못했다. 확인한 것:
- first-login.md:37 "경유지 쪽으로 돌아서기" = koKR navigation.lua:88 `Turn to Waypoint` 값 그대로. 문제없음.
- troubleshooting.md:35 "음성 방식", "음성 종류", 103줄 "걷는 중 추적 아이콘 알림", 111줄 "오류별 필터", 133줄 "막힌 지점을 피하는 새 WowNav 경로", 135줄 "도착 거리 전환" = koKR 값 그대로.
- troubleshooting.md:61 "이 입력과 충돌하는 단축키 ... 바꾸시겠습니까?"는 화면 문구 인용이라 "바꾸다"를 그대로 둔 것이 맞다(낱말 표의 예외 조항).
- installer.md의 버튼·항목 이름(권장 구성으로 설치, 현재 설정으로 업데이트 등)은 설치 프로그램 Loc.cs 값이라 koKR lua로는 대조하지 않았다(미확인).

#### 4. 범위 밖 메모

- troubleshooting.md:95 "단축키와 몇 가지 다른 항목은 항상 캐릭터별입니다"와 managing.md:22 "단축키도 같은 방식으로 공유되며"는 내용이 서로 어긋나 보이는데, 원문(en)이 그렇게 되어 있다. 번역 문제가 아니라 원문 불일치이므로 upstream-report 후보.
- manual-installation.md:81은 원문(영어, 독일어, 프랑스어)에 "한국어"를 더했다. decisions.tsv 2026-11-05의 예외(지원 언어 목록)에 해당하므로 정상.

---

### 감수 결과: basics(interface.md 제외) + controller.md + credits.md

범위: ko/basics/index.md, speech.md, tooltips.md, menu-and-settings.md, alerts.md, keybindings.md, ko/controller.md, ko/credits.md. 전부 en 같은 경로 파일과 줄 단위로 대조해 끝까지 읽었다. credits.md와 index.md는 지적할 것이 없다(index.md의 "쓰는"은 부모 grep 집계 대상).

형식: `파일:줄 | 부류 | 확신도 | 현재 한국어 | 영어 원문 | 수정안 | 이유`

부류: (a) 지시어 대상 불명 (b) 영어 관용구·은유 직역 (c) 목적어·주어 생략 (d) 동사 선택이 설명서 관례와 다름 (e1) 같은 영어를 파일마다 다른 한국어로 옮김(용어 갈림) (e2) 사용자 결정·번역 지침 위반 (e3) 조사 오류 (e4) 표 머리글과 칸의 문형이 안 맞음

#### 1. 반복 표현 (위치 목록 + 방침 제안)

##### 1-1. steps aside / takes / stays with / goes back to: WowVision과 게임이 키를 "주고받는" 은유 (b)
interface.md의 "키를 가져가다"와 같은 뿌리다. 이 범위에서는 "물러나다, 맡다, 차지하다, 돌아가다, 가져오다, 남다"로 나타난다.

- menu-and-settings.md:19 | b | 높음 | 전투 중에는 WowVision이 물러나 있으므로 메뉴는 전투 전이나 전투 후에 여십시오. | In combat WowVision steps aside, so open the menu before a fight or after it | 전투 중에는 WowVision이 창 이동 키를 처리하지 않으므로 메뉴는 전투 전이나 전투 후에 여십시오. | "물러나 있다"는 무엇을 안 하는지가 안 들린다. interface.md `## 전투`의 수정안과 같은 말로 맞춘다.
- controller.md:32 | b | 높음 | WowVision 창이 열려 있는 동안에는 WowVision이 방향 패드와 앞면 버튼을 맡습니다. | WowVision takes the D-pad and the face buttons | WowVision 창이 열려 있는 동안에는 방향 패드와 앞면 버튼 입력을 WowVision이 처리합니다. | takes your keys와 같은 표현. 방침 하나로 통일.
- controller.md:39 | b | 중간 | Escape를 게임이 맡는 곳에서는 B가 대신 게임 자체의 Escape를 실행합니다. | Where Escape belongs to the game | Escape를 게임이 처리하는 창에서는 B가 대신 게임 자체의 Escape를 실행합니다. | "곳"이 창을 뜻하는 것이 안 잡힌다.
- controller.md:99 | b | 중간 | 게임의 휠에 그대로 남아 비장애인 플레이어가 쓸 때와 똑같이 작동합니다 | Stay with the game's wheel and work as they do for sighted players | 게임의 휠이 그대로 처리하므로 비장애인 플레이어가 사용할 때와 똑같이 작동합니다 | "버튼이 휠에 남는다"는 뜻이 안 통한다.
- controller.md:119 | b | 높음 | 전투가 시작되면 WowVision 창의 키와 마찬가지로 WowVision 창에서 쓰는 버튼과 바로 가기 층이 게임으로 돌아갑니다. 오른쪽 스틱 누르기와 그 조합(경유지 쪽으로 돌아서기, 버퍼)은 언제나 WowVision이 맡습니다. 전투가 끝나면 WowVision이 버튼을 다시 가져옵니다. | the window buttons and the shortcut layer go back to the game ... stay with WowVision all the time. When combat ends, WowVision takes its buttons again. | 전투가 시작되면 WowVision 창의 키와 마찬가지로 WowVision 창에서 사용하는 버튼과 바로 가기 층을 게임이 처리합니다. 오른쪽 스틱 누르기와 그 조합(경유지 쪽으로 돌아서기, 버퍼)은 언제나 WowVision이 처리합니다. 전투가 끝나면 WowVision이 버튼을 다시 처리합니다. | 세 문장이 모두 같은 은유.
- keybindings.md:115 | b | 높음 | WowVision은 두 애드온이 부딪치지 않도록 Sku도 쓰는 몇몇 키를 차지하지 않습니다. | WowVision does not take a few keys that Sku also uses, so the two do not fight | WowVision은 두 애드온의 키가 충돌하지 않도록 Sku도 사용하는 몇몇 키를 사용하지 않습니다. | fight → 충돌, take → 사용. 같은 문서 `## 충돌` 절이 이미 "충돌"을 쓴다.
- tooltips.md:123 | b | 높음 | 두 애드온이 키를 두고 다투지 않도록 WowVision은 ... 툴팁 키를 할당하지 않은 채로 둡니다. | so that the two addons do not fight over them | 두 애드온의 키가 충돌하지 않도록 ... | 같은 영어(fight)가 keybindings.md:115에서는 "부딪치다", 여기서는 "다투다"로 갈렸다. 범위 밖 참고: windows/character.md:22도 "같은 키를 두고 부…"로 시작한다.
- tooltips.md:117 | b | 중간 | 툴팁이 없으면 Space는 게임에 그대로 넘어가므로, 입력 중이 아닐 때는 캐릭터가 점프합니다. | Space is left alone for the game | 툴팁이 없으면 Space는 게임이 그대로 처리하므로 ... | 같은 계열.
- "Sku에 맡깁니다"(keybindings.md:115 두 곳, :125 "Escape를 게임에 맡기는 창")는 한국어로 자연스럽고 뜻이 통하므로 유지 권고.

방침 제안: take / own / belong to / stay with / go back to / step aside (키·버튼) → "A가 그 키(입력)를 처리한다 / 처리하지 않는다"로 통일. "가져가다, 맡다, 차지하다, 물러나다, 돌아가다, 남다"는 쓰지 않는다. fight (over keys) → "충돌하다".

##### 1-2. land on / you land in: "놓입니다"에 주어가 없음 (c)
같은 범위 안에 좋은 번역이 이미 있다: keybindings.md:12 "초점이 첫 단축키에 놓이고", :24 "초점이 놓인 버튼", :36 "초점은 그 동작의 첫 키에 놓이고". 주어를 뺀 곳만 고치면 된다.

- menu-and-settings.md:99 | c | 높음 | Enter를 누르면 선택지 목록이 열리고 현재 선택지에 놓입니다. | Enter opens the list of choices. You land on the current one. | Enter를 누르면 선택지 목록이 열리고 초점이 현재 선택지에 놓입니다. | 무엇이 놓이는지 없다.
- menu-and-settings.md:116 | c | 높음 | 소리에서 Enter를 누릅니다. 폴더 목록에 놓입니다. | You land in a list of folders. | 소리에서 Enter를 누릅니다. 초점이 폴더 목록에 놓입니다. | 같음.
- tooltips.md:24 | b | 낮음 | 컨트롤에 도착한 뒤 처음 누르는 Shift+Down은 | after you land on a control | 컨트롤로 이동한 뒤 처음 누르는 Shift+Down은 | 단순 치환. 줄 번호만 참고.
- 이미 "이동"으로 잘 옮긴 곳(수정 불필요): tooltips.md:4, alerts.md:49, alerts.md:157, menu-and-settings.md:118.

방침 제안: land on → 사용자가 가는 경우 "~로 이동하다", 프로그램이 데려다 놓는 경우 "초점이 ~에 놓이다". "도착하다"와 주어 없는 "놓이다"는 쓰지 않는다.

##### 1-3. without asking / with no question: "묻지 않고" (b)
위치: menu-and-settings.md:148, keybindings.md:65, controller.md:129 (범위 밖: interface.md:233, world/wownav.md:92)

- menu-and-settings.md:148 | b | 중간 | 맨 아래에는 묻지 않고 삭제하는 제거 버튼이 있습니다. | a Remove button that deletes it without asking | 맨 아래에는 확인 없이 바로 삭제하는 제거 버튼이 있습니다. | 누가 누구에게 묻는지가 빠져 있다. 소프트웨어 설명서 관례는 "확인 없이".
- keybindings.md:65 → "확인 없이 즉시 제거되고", controller.md:129 → "확인 없이 바로 지워집니다".

방침 제안: without asking / with no question → "확인 없이".

##### 1-4. goes back (one level / one folder / up): "뒤로" (d, 사용자 낱말 표)
- menu-and-settings.md:13, :14 "한 단계 뒤로 갑니다" → "한 단계 이전으로 돌아갑니다" (단순 치환, 사용자 낱말 표).
- menu-and-settings.md:121 | d | 높음 | Escape를 누르면 아무것도 고르지 않고 한 폴더 뒤로 갑니다. | Escape goes back one folder without choosing anything. | Escape를 누르면 아무것도 고르지 않고 상위 폴더로 돌아갑니다. | 폴더는 "이전"보다 "상위"가 정확하다. 단순 치환과 다르다.
- menu-and-settings.md:40 | d | 중간 | 각 화면은 목록이며, Escape를 누르면 위로 돌아갑니다. | Escape goes back up. | ... Escape를 누르면 상위 화면으로 돌아갑니다. | "위로"는 목록의 위쪽 항목으로도 들린다.
- controller.md:56 | d | 중간 | B를 누르면 뒤로 갑니다. | Press B to go back. | B를 누르면 이전 단계로 돌아갑니다. | 같은 계열.

##### 1-5. accept: "확정" 목적어 없음 (c)
- menu-and-settings.md:100 "입력한 뒤 Enter로 확정하거나 Escape로 취소합니다" → "Enter로 입력을 확정하거나"
- menu-and-settings.md:130 "Enter로 확정합니다" → "Enter로 입력을 확정합니다"
(interface.md:158 예시 7과 같은 방침을 적용.)

##### 1-6. modifier: "보조 키"와 "조합 키"로 갈림 (e1)
- 보조 키: interface.md:42, keybindings.md:44, :49, :50, :122, reference/keybindings.md:37, :38
- 조합 키: speech.md:55, controller.md:17(제목), controller.md:28
- 높음. koKR에 modifier 키 값은 없다(grep 0건). 다수인 "보조 키"로 통일 권고. controller.md:17 제목 "조합 키: 어깨 버튼과 트리거" → "보조 키: 어깨 버튼과 트리거"(제목이 바뀌므로 이 제목을 가리키는 앵커가 있는지 확인 필요, 이 범위에서는 발견하지 못했다). 용어집 후보.

##### 1-7. checkbox: "체크 상자"와 "확인란"으로 갈림 (e1, e2)
- 확인란(이 범위 8곳): tooltips.md:51, :55, :98, :111, alerts.md:34, :47, :102, :125. 설명서 전체로는 확인란 15줄, 체크 상자 67줄.
- 높음. translation-guide `## 문체`가 Checkbox → 체크 상자로 정했고 koKR `ui.lua:41 L["Checkbox"] = "체크 상자"`이므로 사용자가 실제로 듣는 말은 "체크 상자"다. "확인란" 전부 "체크 상자"로. tooltips.md:51 "Pawn 요약 확인란을 끕니다"(uncheck Pawn Summary) → "Pawn 요약 체크 상자의 체크를 해제합니다" 또는 "Pawn 요약 체크 상자를 끕니다".

##### 1-8. 링크 뒤 조사 "를" (e3)
"[알림](./alerts.md)를 보십시오" 꼴. 링크 글자가 "알림"이므로 "을"이어야 한다.
- 이 범위: speech.md:58, :76, menu-and-settings.md:48, :107
- 범위 밖(grep으로 확인): getting-started/quick-start.md:61, troubleshooting.md:44, information/group-health.md:106, information/monitors.md:53, reference/glossary.md:8, :42, world/minimap.md:127, world/quests.md:128
- 높음. 영문 제목 Alerts를 한국어 "알림"으로 바꾼 뒤 조사를 안 고친 흔적으로 보인다(2026-11-07 경보 → 알림 결정 때 "경보를"이 "알림를"로 남은 것으로 추정).

##### 1-9. target (동사): "대상으로 잡다" (d)
- alerts.md:99 "무언가를 대상으로 잡습니다" (You target something), alerts.md:103 "새로운 것을 대상으로 잡습니다" (you target something new)
- 중간. 수정안: "무언가를 대상으로 지정합니다". 같은 범위 controller.md:121이 이미 "게임에서 대상을 지정하려고"로 쓰고 있다. 설명서 전체 집계는 부모가 grep("대상으로 잡")으로 확인 권고.

##### 1-10. covers / left to: "맡다" (b, 낮은 우선순위)
- alerts.md:112 | b | 중간 | 알림 하나가 모든 귓속말 탭을 맡습니다. | One alert covers all whisper tabs. | 알림 하나가 모든 귓속말 탭에 적용됩니다.
- alerts.md:123 | b | 낮음 | 퀘스트 진행 메시지는 퀘스트 모듈의 퀘스트 진행 상황 알림들이 맡습니다. | are left to the quest progress alerts | ... 알림들이 처리합니다.

##### 1-11. counts as: "~로 치다" (d)
- controller.md:121 | d | 중간 | 그 어깨 버튼은 이미 쓴 것으로 칩니다. | counts as using that hold | 그 어깨 버튼은 이미 사용한 것으로 처리합니다. | 범위 밖 interface.md:88 "두 번 누르기로 치지 않습니다"도 같은 표현. 같은 범위 keybindings.md:49, :122는 "인정됩니다"로 옮겨 뜻이 통한다.

#### 2. 개별 사례

##### speech.md
- speech.md:36 | c | 중간 | Retail과 WoW: Forever는 글자에 손대지 않고 그대로 넘깁니다. | hand the text over untouched | Retail과 WoW: Forever에서는 텍스트를 가공하지 않고 그대로 음성으로 전달합니다. | 어디로 넘기는지 없고 "손대다"는 은유.
- speech.md:67 | c | 중간 | 게임 자체 설정이므로 게임의 /tts playline, /tts playactivity 명령과 음성 메뉴는 항상 일치합니다. | the game's ... commands and the Speech menu always agree | 게임 자체 설정이므로 게임의 /tts playline, /tts playactivity 명령으로 변경한 값과 음성 메뉴의 값은 항상 같습니다. | 명령과 메뉴가 "일치한다"는 무엇이 같은지 빠졌다.
- speech.md:80 | a | 중간 | 거기서 따로 고르기 전까지는 음성 종류를 그대로 따르며, 그 음성을 값으로 보여 줍니다. | Until you choose something there, it simply follows Speech Voice, and it shows that voice as its value. | 이 설정에서 음성을 따로 고르기 전까지는 음성 종류 설정을 그대로 따르며, 설정값에도 그 음성이 표시됩니다. | "거기서"와 "음성 종류"(설정 이름)가 귀로 구분되지 않는다. alerts.md:45가 같은 내용을 "음성 종류 설정을 따르며"로 더 잘 옮겼다.

##### tooltips.md
- tooltips.md:57 | b | 중간 | 아이템의 마지막 줄을 지나 Shift+Down을 누르면 비교로 들어가고 | Press Shift+Down past the item's last line to walk into the comparison | 아이템의 마지막 줄에서 Shift+Down을 더 누르면 비교 내용으로 넘어가고 | "줄을 지나 누른다", "비교로 들어간다"가 직역.
- tooltips.md:81 | d | 중간 | 보석과 마법부여는 셈에 넣지 않습니다. | do not count gems or enchantments | 보석과 마법부여는 계산에 포함하지 않습니다. | "셈에 넣다"는 설명서에서 쓰지 않는 말. 낱말 표의 포함되다 계열.
- tooltips.md:111 | b | 낮음 | 이 값은 경매장을 쓰는 동안 WowVision이 만드는 가격 데이터베이스에서 옵니다. | These come from the price database | 이 값은 ... 가격 데이터베이스에서 가져옵니다. | come from 직역.
- tooltips.md:63 | c | 낮음 | 양손 무기를 들고 있으면 두 손에 하나씩입니다. | both hands when you hold a two-handed weapon | 양손 무기를 들고 있으면 양손 각각에 구역이 하나씩 생깁니다. | 무엇이 하나씩인지 앞 절과 떨어져 있다. 원문 자체가 압축돼 있어 확신 낮음.

##### menu-and-settings.md
- menu-and-settings.md:87 | e2 | 높음 | 리테일과 WoW: Forever에서는 게임 플레이 효과음도 고를 수 있습니다. | Retail and WoW: Forever also offer Gameplay Sound Effects. | Retail과 WoW: Forever에서는 ... | decisions.tsv 2026-11-07 "게임 버전 이름은 영어(Retail). 리테일은 쓰지 않는다" 위반. 설명서 전체에서 "리테일"은 이 한 곳뿐(grep).
- menu-and-settings.md:118 | d | 중간 | WowVision에 딸려 오는 소리를 쓰려면 WowVision 폴더로 | the sounds that ship with WowVision | WowVision에 포함된 소리를 사용하려면 WowVision 폴더로 | "딸려 오다"는 입말. 같은 범위 speech.md:71은 같은 ship with를 "들어 있습니다"로 옮겼다.
- menu-and-settings.md:123 | a | 중간 | 비컨 소리(...) 중 하나를 고르며, 하나로 이동하면 비컨 견본이 재생됩니다. | moving onto one plays a sample beacon | ... 소리 항목으로 이동하면 비컨 견본이 재생됩니다. | "하나로 이동"이 무엇인지 안 잡힌다. alerts.md:49는 같은 문장을 "소리 항목으로 이동하면"으로 옮겼다. 견본/미리 듣기도 두 파일이 갈린다(sample: 여기 "견본", alerts.md:49 "미리 듣기").
- menu-and-settings.md:169 | c | 중간 | 전역을 고르면 설정을 계정 저장소에 둡니다. 계정의 값을 가져옵니다. | Choosing Global makes the setting follow the account. It takes the account's value. | 전역을 고르면 설정이 계정 저장소를 따릅니다. 이때 설정값은 계정에 저장된 값으로 변경됩니다. | 둘째 문장에 주어가 없어 누가 무엇을 가져오는지 안 들린다.
- menu-and-settings.md:161 | a | 낮음 | 나중에 로그인하는 캐릭터는 이미 있는 것을 그냥 씁니다. | characters that log in later simply use what is there | 나중에 로그인하는 캐릭터는 계정 저장소에 이미 있는 설정을 그대로 사용합니다. | "이미 있는 것"의 대상.
- menu-and-settings.md:192 | d | 중간 | 로그아웃하거나 UI를 재시작하거나 게임을 끝낼 때 WowVision 설정을 디스크에 씁니다. | The game writes WowVision's settings to disk | ... WowVision 설정을 디스크에 저장합니다. | "쓰다"가 사용의 뜻으로 수십 번 나오는 문서에서 write의 뜻으로 한 번 나온다. 부모의 쓰다 → 사용하다 일괄 치환에서 "디스크에 사용합니다"로 잘못 바뀔 위험이 있어 따로 적는다. 절 제목도 "설정이 저장되는 때"다.

##### alerts.md
- alerts.md:93 | a | 중간 | 나침반 방향 읽기는 거기서 말하지 않고 다른 나침반 알림은 계속 작동합니다. | Speak Compass Direction stays silent there while the other compass alerts keep working | 인스턴스 안에서는 나침반 방향 읽기가 작동하지 않고 다른 나침반 알림은 계속 작동합니다. | "거기서". 그리고 설정 이름 "나침반 방향 읽기"가 "말하지 않는다"의 주어라 어색하다.
- alerts.md:99 | b | 중간 | 목표 선택의 이름 화면에서 고른 항목(기본값은 이름, 레벨 등)을 읽으며, 대상 표시기로 시작하게 할 수도 있습니다. | optionally starting with its raid marker | ... 읽으며, 대상 표시기를 맨 앞에 읽게 할 수도 있습니다. | "표시기로 시작하다"는 직역.
- alerts.md:102 | a | 중간 | 그 소프트 대상의 각도와 거리도 여기에 있습니다. | It also holds the arc and range of that soft target | 그 소프트 대상의 각도와 거리 설정도 이 알림 화면에 있습니다. | "여기"가 표의 칸 안에서 무엇인지 안 잡힌다.
- alerts.md:125 | b | 높음 | 아직 만나지 않은 것을 포함해 게임이 아는 모든 메시지를 나열합니다. | including ones you have not met yet | 아직 본 적 없는 메시지를 포함해 ... | met 직역. 바로 위 표(alerts.md:123)가 "본 적 있는 메시지"로 썼다.
- alerts.md:131 | c | 중간 | 걷는 중 추적 아이콘 알림(켬)이 필요합니다. | Needs Announce Tracked Dots While Walking (on). | 걷는 중 추적 아이콘 알림 설정이 켜져 있어야 합니다. | 설정 이름이 문장에 그대로 녹아 "알림이 필요하다"로 들린다. alerts.md:74는 같은 Needs를 "켜져 있어야 합니다"로 옮겼다.
- alerts.md:135 | c | 중간 | 퀘스트의 모든 목표가 끝났습니다. 끝났는지는 퀘스트 목록에서 확인합니다. | Every objective of a quest is done, read from your quest log. | 퀘스트의 모든 목표가 끝났습니다. 완료 여부는 WowVision이 퀘스트 목록에서 읽어 옵니다. | 주어가 없어 사용자가 직접 확인하라는 지시로 들린다.
- alerts.md:45 | a | 낮음 | 하나를 고르기 전까지는 음성 종류 설정을 따르며 | Until you choose one | 음성을 고르기 전까지는 ... | "하나"의 대상.
- alerts.md:70 외 표 5개(:70, :78, :97, :109, :120, :129) | e4 | 중간 | 머리글 "울리는 때" 아래 칸이 "전투에 들어갑니다.", "떨어집니다." | When it fires / You enter combat. | 칸을 "전투에 들어갈 때", "떨어질 때"로 쓰거나 머리글을 "조건"으로 | 스크린리더는 칸마다 머리글을 붙여 "울리는 때, 전투에 들어갑니다"로 읽는다. 원문의 문장 형태를 따른 것이라 구조 검사(tools.manual check)와는 무관하지만, 서술 종결형이 조건으로 들리지 않는다. 약 40칸에 걸리므로 대량 방침으로 사용자 결정을 받을 사안.

##### keybindings.md
- keybindings.md:81 | c | 중간 | WowVision은 자체 동작끼리만 키를 확인합니다. 게임 자체 단축키는 확인하지 않으며 | WowVision only checks keys against its own actions. | WowVision은 키 충돌을 자체 동작끼리만 확인합니다. 게임 자체 단축키와 충돌하는지는 확인하지 않으며 | 무엇을 확인하는지(충돌 여부)가 빠졌다.
- keybindings.md:113 | b | 낮음 | (제목) Sku를 불러왔을 때 꺼지는 키 | Keys that stay off when Sku is loaded | 수정 보류 | 뜻은 통한다. 제목 앵커라 바꾸면 링크가 깨질 수 있다.

##### controller.md
- controller.md:19 | c | 높음 | 그래서 WowVision이 누르고 있는 버튼을 직접 읽어 그 키처럼 다룹니다. | so WowVision reads the held buttons itself and treats them like those keys | 그래서 사용자가 누르고 있는 버튼을 WowVision이 직접 읽어 Shift, Ctrl, Alt처럼 처리합니다. | "WowVision이 누르고 있는 버튼"으로 들린다(수식 범위 모호). "그 키"도 앞 문장으로 되돌아가야 한다.
- controller.md:75 | a | 중간 | 전투 중이 아닐 때 양쪽 어깨를 함께 누르고 있으면, 버튼들이 WowVision 창을 엽니다. 이 창들에 해당하는 게임 버튼은 화면에 무언가를 띄울 뿐이라 비장애인 플레이어에게만 쓸모가 있습니다. | Hold both shoulders together, out of combat, and the buttons open WowVision windows whose game buttons only show something to sighted players | 전투 중이 아닐 때 양쪽 어깨를 함께 누르고 있으면 아래 버튼들이 WowVision 창을 엽니다. 게임에서 이 버튼들은 비장애인 플레이어만 볼 수 있는 화면을 표시합니다. | "이 창들에 해당하는 게임 버튼"이 귀로 풀리지 않는다. "띄우다"는 낱말 표의 뜨다 계열. 원문 관계절이 꼬여 있어 수정안 확신은 중간.
- controller.md:102 | c | 중간 | 추적은 WowVision 스캐너를 열고, 대화는 WowVision 대화 창을 엽니다. | Tracking opens the WowVision scanner and chat opens the WowVision chat window. | 추적 칸은 WowVision 스캐너를 열고, 대화 칸은 WowVision 대화 창을 엽니다. | 다음 문장이 "나머지 칸"이라고 받는데 앞에서 칸이라는 말이 없다.
- controller.md:134 | c | 중간 | 전투 중에는 아예 열리지 않고 "전투 중에는 불가"라고 말합니다. | In combat it does not open at all | 전투 중에는 버튼 입력 대기가 아예 시작되지 않고 ... | 무엇이 열리지 않는지 없다. 창이 안 열린다는 뜻으로 들린다.
- controller.md:140 | c | 낮음 | 인터페이스가 켜져 있으면 "WowVision pad log started afresh"라고 답하고 | (원문 if the interface is off) | 게임패드 인터페이스가 켜져 있으면 ... | 이 설명서에서 "인터페이스"는 WowVision 메뉴 항목 이름이기도 하다.
- controller.md:26, :73 등 | e1 | 낮음 | 바로 가기 층 | shortcut layer | 판단 보류 | 용어집에 floor = 층이 있어 "층"이 건물 층으로 들릴 수 있다. koKR에 값 없음(실제 발화는 "양쪽 어깨"). 용어집 후보로만 올린다.

#### 3. 로케일 값 문제
이 범위에서 설명서만 고칠 수 없는 화면 문구 문제는 발견하지 못했다. 확인한 것: "사용함"(ui.lua:64), "체크 상자"(ui.lua:41), "Pawn 요약"(misc.lua:13), "양쪽 어깨"(controller.lua:23), "스캐너를 트리로 표시"(scanner.lua:8)는 설명서 인용과 일치한다. 1-7의 "확인란"은 반대로 설명서가 로케일 값과 어긋난 경우다(설명서를 고치면 된다).

#### 4. 건드리지 말 것(과잉 수정 경계)
- speech.md:56, interface.md 계열 "말이 밀리지 않습니다"(backlog): 자연스럽고 뜻이 통한다.
- menu-and-settings.md:36 "테스터를 위한 지름길": 통용되는 비유.
- keybindings.md의 "입력 받기"(capture), "주 키"(main key), "인정됩니다"(counts as): 잘 옮겼다.
- controller.md:71 "톡 눌러"(tap): 유지.
- alerts.md 예시 단계의 명사형 끝맺음("... 가서 Enter."): 원문 문형 그대로라 유지.

#### 5. 건수
- (a) 지시어: 7건
- (b) 관용구·은유 직역: 17건(반복 묶음 1-1 8건, 1-3 3건, 1-10 2건 포함)
- (c) 목적어·주어 생략: 15건(1-2 2건, 1-5 2건 포함)
- (d) 동사 선택: 10건(1-4 5건, 1-9 2건, 1-11 1건 포함)
- (e1) 용어 갈림: 3묶음(보조 키/조합 키 3곳, 체크 상자/확인란 8곳, 바로 가기 층)
- (e2) 결정 위반: 1건(리테일) + 확인란 8곳과 겹침
- (e3) 조사 오류: 이 범위 4곳, 범위 밖 8곳
- (e4) 표 머리글·칸 문형: 표 6개 약 40칸(방침 1건)

---

### part-world1: world/navigation.md, wownav.md, movement.md, index.md 감수

범위 4개 파일을 영어 원문과 줄 단위로 끝까지 대조했다. index.md는 지적 없음. 줄 번호는 한국어 파일 기준(영어는 대체로 한 줄 앞).
형식: `파일:줄 | 부류 | 확신도 | 현재 한국어 | 영어 원문 | 수정안 | 이유`

부류: (a) 지시어 (b) 관용구·은유 직역 (c) 목적어·주어 생략 (d) 동사 관례 (e1) 파일 간 용어 불일치 (e2) 키 이름 번역 (e3) 영어 낱말+기 행위자 이름(사용자 낱말 표 위반) (e4) 따옴표 없는 화면 문구가 문장 성분처럼 들림 (e5) 능격 동사 직역(사물 주어 + 타동사)

#### 1. 반복 표현과 방침 제안

##### 1-1. (e2) 키 이름 Up/Down이 "위/아래"로 번역됨 [높음]
- navigation.md:37 "목록 안에서는 위와 아래로 이동합니다" (move inside a list with Up and Down)
- navigation.md:83 표의 키 열 "위 / 아래" (Up / Down)
- navigation.md:311 "아래를 누르면 다음 경매인이 들립니다" (Press Down to hear the next one)
- 근거: translation-guide `## 용어` 5번(키 이름은 영어 그대로). 같은 범위의 wownav.md:92 "Up과 Down으로 이동하고", wownav.md:208 "Down을 누르면", basics/interface.md 표는 Up/Down이다. koKR bindings.lua의 "위"/"아래"는 단축키 이름(Binding name)이지 키 이름이 아니다.
- 수정안: 37 "목록 안에서는 Up과 Down으로 이동합니다" / 83 "Up / Down" / 311 "Down을 누르면 다음 경매인이 들립니다".

##### 1-2. (e1) "포커스"와 "초점" [높음]
- navigation.md:94, 309, 320만 "포커스". 설명서 전체에서 "포커스"는 이 파일 3곳뿐이고 나머지는 "초점"이다(grep 확인).
- 수정안: 94 "초점은 목적지에 놓입니다" / 309 "가장 가까운 진입 지점에 초점이 놓이고" / 320 "초점이 목적지에 놓인 채로".

##### 1-3. (e3) "경로 계획기", "선택기" [높음: 사용자 낱말 표 "영어 낱말에 -기를 붙여 행위자 이름을 만들지 않습니다"]
- 경로 계획기(router): navigation.md:181, 203, 251. 범위 밖: reference/versions.md:58 "WowNav 경로 계획기".
- 선택기(picker): navigation.md:122. 범위 밖: basics/menu-and-settings.md:104, 123 "소리 또는 비컨 선택기".
- koKR에는 두 낱말 모두 없다(설명서에서만 고치면 된다).
- 방침 제안: router → "경로 계산 기능"(또는 주어를 WowVision으로). picker → "선택 목록".
- 예: 181 "클래식 경로에서는 가장 가까운 경유지 다섯 개 중 가장 좋은 경로가 나오는 것을 WowVision이 고릅니다." / 122 "선택 목록에서 항목으로 이동하면 미리 듣기가 재생됩니다."(견본 → 미리 듣기는 확신도 낮음)

##### 1-4. (b) know 의인화: "데이터가 모르는", "네트워크가 모르는", "데이터가 아는" [중간~높음]
- navigation.md:62 "네트워크가 모르는 건물 안에 있을 때" (a building the network does not know)
- wownav.md:40 "데이터가 모르는 지도에서는" / 123 "데이터가 아는 영역 밖으로" / 130 "데이터가 높이를 모르면" / 226 "데이터가 모르는 울타리에 부딪힙니다"
- 방침 제안: data/network knows X → "데이터에(네트워크에) X가 있다/없다".
- 수정안: 62 "네트워크에 없는 건물 안에 있을 때" / 40 "데이터에 없는 지도에서는" / 123 "데이터에 있는 영역 밖으로 걸어 나갔습니다" / 130 "데이터에 높이 정보가 없으면" / 226 "데이터에 없는 울타리에 부딪힙니다".
- 제외(유지): wownav.md:4 "WowNav는 ... 걸을 수 있는 곳을 알고 있으며", 76 "Questie가 알고 있으면", 109 "WowNav가 알 때만". 프로그램이 주어라 뜻이 통한다.

##### 1-5. (b) known → "알려진" [중간]
- navigation.md:4 "알려진 길을 따라", 9 "알려진 길 네트워크", 251 "가장 가까운 알려진 장소", 322 "알려진 길이 아니므로"
- "알려진"은 "세상에 널리 알려진"으로 들린다. 원뜻은 WowVision 데이터에 있다는 것이다.
- 방침 제안: known path/place → "등록된 길/장소"(1-4의 "데이터에 있는"과 같은 뜻으로 묶음).
- 수정안: 9 "진입 지점은 등록된 길 네트워크에서 경로가 시작되는 곳입니다" / 251 "이름에 "bank"가 포함된 등록된 장소 중 가장 가까운 곳까지 경로를 짭니다".

##### 1-6. (b) take/walk you to → "데려가다, 데려다주다" [중간]
- wownav.md:4 "깊은굴 지하철까지 데려다줄 수 있습니다" (can take you to)
- movement.md:131 "시체까지 데려가기 시작할 수 있습니다" (can start walking you to your corpse)
- movement.md:142 "바깥에서 그곳까지 데려가지 않습니다" (is not walked to from outside)
- movement.md:164 "게임이 물을 통과해 NPC에게 데려간 뒤"
- 방침 제안: WowVision·WowNav가 주어이면 "안내하다", 게임이 캐릭터를 걷게 하는 경우는 "이동시키다".
- 수정안: wownav 4 "깊은굴 지하철까지 안내할 수 있습니다" / movement 131 "WowVision이 시체까지 길 안내를 시작할 수 있습니다" / 142 "시체가 인스턴스 안에 있으면 바깥에서 그곳까지는 안내하지 않습니다" / 164 "게임이 캐릭터를 물을 통과해 NPC에게 이동시킨 뒤 열리는 NPC 창".

##### 1-7. (b)(d) silent/quiet → "조용하다" [중간]
- movement.md:41 "그곳에서는 나침반이 조용하지만" (the compass is then silent)
- movement.md:70 "시작된 낙하는 조용하므로" (stays silent)
- movement.md:75 "착지할 때까지 조용합니다"
- movement.md:100 "벽 감지가 조용합니다" (stays quiet)
- movement.md:117 "끄면 조용히 따라갑니다" (silent following) — 이것은 뜻이 통하므로 유지.
- 방침 제안: 기능이 주어인 silent → "아무것도 알리지 않습니다 / 소리를 내지 않습니다". "낙하가 조용하다"처럼 사건이 주어인 문장은 반드시 고친다.
- 수정안: 41 "그곳에서는 나침반이 방향을 말하지 않지만" / 70 "점프를 누른 뒤 1초가 조금 안 되는 사이에 시작된 낙하는 알리지 않으므로" / 75 "... 시작된 낙하는 착지할 때까지 알리지 않습니다" / 100 "벽 감지가 소리를 내지 않습니다".

##### 1-8. (e4) 따옴표 없는 화면 문구가 문장 성분처럼 들림 [중간, 방침 결정 필요]
원문도 따옴표가 없어서 기호를 더할 수 없다(translation-guide: 원문에 없는 기호 추가 금지). 다만 한국어에서는 문구 뒤에 조사만 붙어 문구의 끝이 귀로 구분되지 않는다. 같은 파일 navigation.md:228이 이미 "…하십시오라는 안내가 들립니다"로 풀었으므로 그 방식으로 통일하자는 제안이다.
- 가장 심한 곳:
  - navigation.md:107 | 높음 | "비컨 중지는 취소할 때 말합니다." | Beacon stopped is spoken when you cancel. | "취소하면 비컨 중지라고 말합니다." | "비컨 중지는"이 주어로 들려서 비컨 중지가 무언가를 말하는 것처럼 들린다.
  - navigation.md:150 | 높음 | "…곳(Retail의 인스턴스)에서는 여기서는 돌아서기 사용 불가가 들립니다." | you hear Turning is not available here. | "…곳(Retail의 인스턴스)에서는 여기서는 돌아서기 사용 불가라는 안내가 들립니다." | "에서는 여기서는"이 겹쳐 화면 문구의 시작이 구분되지 않는다.
  - navigation.md:106 | 중간 | "경로 끝에 이르면 도착이라고 말하고" — 이미 "이라고"가 있어 통한다. 유지.
  - navigation.md:55 | 중간 | "곧바로 선택됨이 들리고" | You hear selected at once | "곧바로 선택됨이라고 들리고"
- 같은 형태 위치 목록(문구+이/가 들립니다): navigation.md:90(경로 없음이), 105(도착이), 149, 171(2곳), 177(경로 끝이나 경로 시작이, 활성 경유지 없음이), 181(다시 시작할 경로 없음이), 191(비컨 중지가, 활성 경유지 없음이), 201(대상의 위치를 알 수 없음이), 203, 212(방문함을 먼저 붙여), 235(경로 계산 중이), 239(경로 시작이). wownav.md:92 "여기서 경로 없음은 시작점에서 …"(문장 첫머리라 특히 구분이 안 됨, 중간).
- 방침 제안: 따옴표 없는 화면 문구 뒤에는 "(이)라고", "(이)라는 안내가"를 붙인다. 기호는 더하지 않는다.

##### 1-9. (e1) 같은 범위 안에서 갈린 용어 [중간]
- "경로 체계"(navigation.md:18, 27, 259, 332) 대 "경로 시스템"(wownav.md:4). 원문은 모두 route system. 한쪽으로 통일(용어집 후보).
- "대상까지 경로 안내"(navigation.md:181, 193, 195, 211, 335) 대 "대상까지의 경로"(wownav.md:12, 62). 원문은 모두 the route to your target. 단축키 이름(koKR)인 "대상까지 경로 안내"로 통일 제안.
- "버그 보고"(navigation.md:303, wownav.md:40) 대 "버그 신고"(basics/interface.md:240). 통일 필요(부모가 전수 확인).
- 상호 참조 문구: navigation.md는 "…를 보십시오", wownav.md·movement.md는 "…를 참고하십시오". 원문은 모두 See. 확신도 낮음, 통일하면 좋은 정도.
- WowVision이 키를 take/release: movement.md:173 "키를 잡고 놓는 시점", movement.md:178 "WowVision의 키에 일어나는 일". interface.md의 "가져가다/돌려주다"와 또 다른 표현이다. 부모가 정하는 take keys 방침에 이 두 곳을 포함해야 한다. 수정안 예: 173 "/wv keylog로 WowVision이 이동 키 처리를 시작하고 끝내는 시점을 기록할 수 있습니다" / 178 "[전투](combat.md): 전투 중 WowVision의 키가 어떻게 작동하는지."

##### 1-10. 포함 뜻의 "들어가다/들어 있다" (사용자 낱말 표: 들어가다 → 포함되다) [중간, 위치만]
- navigation.md:25(지도 데이터가 들어 있지 않습니다), 173(Ctrl+Alt가 들어가는 다른 단축키), 228(이름이 들어간 안내), 251("bank"가 들어간), 263·265(함께 들어 있는: bundled, 3곳)
- wownav.md:23(함께 들어 있으며), 35(경로에 들어가지 않습니다), 64(목록에 들어갑니다), 75(이름에 들어가는 장소 낱말)
- movement.md:8(표 머리 "들어 있는 것": What it holds, 유지 가능)

##### 1-11. 부모 집계용 줄 번호(단순 치환과 같은 경우)
- 지켜보다: movement.md:21(나침반 모듈은 캐릭터를 지켜보다가 → "캐릭터의 상태를 계속 확인하다가" 제안), wownav.md:115(진행 상황을 지켜보다가: 뜻이 통함, 유지 가능)
- 도착(land on) 계열: 이 범위에는 "도착하다" 직역이 없고 "놓이다"로 옮겼다. 아래 2절 navigation.md:46 참고.
- 오가다: navigation.md:239(2절에 상세)
- 가져가다, 한 단계 뒤로: 해당 없음.

#### 2. 개별 사례

##### navigation.md
1. navigation.md:10 | (b) | 높음 | "목적지를 검색하고 그 위에서 Enter를 누릅니다." | Search for a destination and press Enter on it. | "목적지를 검색하고 그 목적지에서 Enter를 누릅니다." | on it의 직역. 같은 파일 62, 66줄은 "목적지에서 Enter를 누르면"으로 쓴다.
2. navigation.md:35 | (a) | 높음 | "퀘스트 목록에 있을 때 F10을 누르면 그 퀘스트의 다음 대상을 가리킨 채로 창이 열립니다." | Pressing F10 while you are in the quest log opens the window aimed at that quest's next target | "퀘스트 목록에서 퀘스트에 초점을 둔 채 F10을 누르면, 해당 퀘스트의 다음 대상이 목적지로 지정된 상태로 창이 열립니다." | "그 퀘스트"의 선행어가 없다(어느 퀘스트인지는 세 문장 뒤에 나온다). "가리킨 채로"(aimed at)도 은유 직역.
3. navigation.md:35 | (c) | 중간 | "퀘스트는 목록에서 커서가 놓인 퀘스트이고, 그런 퀘스트가 없으면 세부 정보가 열려 있는 퀘스트입니다." | The quest is the one your cursor is on in the log, or else the one whose details are open. | "여기서 말하는 퀘스트는 퀘스트 목록에서 커서가 있는 퀘스트이고, 그런 퀘스트가 없으면 세부 정보가 열려 있는 퀘스트입니다." | 정관사 The quest의 지시 기능이 빠져 정의문으로 들리지 않는다.
4. navigation.md:94 | (b) | 중간 | "그 항목을 가리킨 채로 길 안내 창이 열립니다." | opens the navigation window already aimed at it | "그 항목이 목적지로 지정된 상태로 길 안내 창이 열립니다." | 2번과 같은 aimed at.
5. navigation.md:46 | (c) | 높음 | "창이 열리면 이미 선택된 진입 지점에 놓이므로, 바로 검색으로 넘어가도 되는 경우가 많습니다." | When the window opens, you land on the entry point that is already selected | "창이 열리면 이미 선택된 진입 지점에 초점이 놓이므로, …" | 무엇이 놓이는지 주어가 없다. land on 방침의 한 사례(309줄은 "포커스가 놓이고"로 주어가 있다).
6. navigation.md:52 | (e5) | 중간 | "각 항목은 이름과 거리, 지금 바라보는 쪽을 기준으로 한 방향을 읽습니다." | Each entry reads its name, its distance and the direction | "각 항목에서는 이름과 거리, 지금 바라보는 쪽을 기준으로 한 방향을 읽어 줍니다." | 항목이 무언가를 읽는 것처럼 들린다. 같은 형태: navigation.md:88 "각 목적지는 이름과 거리, 그다음 목록 안의 위치를 읽습니다" → "각 목적지에서는 …을 읽어 줍니다". wownav.md:70은 "목적지마다 … 읽습니다"로 이미 자연스럽다.
7. navigation.md:72 | (c) | 중간 | "여러 단어가 아니라 텍스트 조각 하나입니다." | It is one text fragment, not several words | "검색어는 여러 단어로 나누지 않고 텍스트 조각 하나로 취급합니다." | 주어 It(검색어)이 빠져 무엇이 조각인지 알 수 없다.
8. navigation.md:72 | (b) | 낮음 | "장소 텍스트의 어느 부분과도 일치합니다." | matches any part of a place's text | "장소 텍스트의 어느 부분에 있어도 찾습니다." | "어느 부분과도 일치"는 모든 부분과 같다는 뜻으로 들릴 수 있다.
9. navigation.md:90 | (a) | 중간 | "야드에는 진입 지점까지 걷는 길이 포함됩니다." | The yards include the walk to your entry point. | "이 거리에는 진입 지점까지 걷는 길이 포함됩니다." | "야드에는"이 무엇을 가리키는지(요약의 340야드) 귀로 잡히지 않는다.
10. navigation.md:105 | (b)(c) | 중간 | "비컨이 이제 이끄는 경유지도 셉니다." | The waypoint the beacon now leads to counts too. | "비컨이 지금 안내하는 경유지도 남은 수에 포함됩니다." | 무엇에 세는지가 빠졌다.
11. navigation.md:143 | (b) | 낮음 | "WowVision은 카메라를 돌린 뒤 새 방향을 캐릭터에 넘깁니다." | turns the camera and hands the new direction to your character | "WowVision은 카메라를 돌린 뒤 캐릭터가 그 방향을 따르게 합니다." | hands to의 직역. 뜻은 짐작되므로 낮음.
12. navigation.md:157 | (b) | 높음 | "거리가 짧으면 각 지점 위로 정확히 걸어가야 하고, 길면 조금 벗어나도 봐줍니다." | a large one forgives wandering | "거리가 짧으면 각 지점 위로 정확히 걸어가야 하고, 길면 조금 벗어나도 도착한 것으로 칩니다." | forgive의 의인화 직역이고 구어체다. "도착한 것으로 치다"는 같은 문단이 이미 쓰는 표현이다.
13. navigation.md:185 | (b) | 낮음 | "경로가 뒤집힙니다." | The route turns around | "경로가 반대 방향으로 전환됩니다." | 화면 문구 "경로 역방향 전환"과 맞춘다. 135줄 "진행 중인 경로를 뒤집어"도 같다.
14. navigation.md:239 | (d)(b) | 높음 | "Ctrl+W와 Ctrl+S는 경로를 오갈 때처럼 연속 안내를 오갑니다." | Ctrl+W and Ctrl+S step through the chain the way they step through a route. | "Ctrl+W와 Ctrl+S는 경로에서 경유지를 앞뒤로 넘길 때와 같은 방식으로 연속 안내의 출현 지점을 앞뒤로 넘깁니다." | "오가다"에 목적어(무엇 사이를)가 없어 뜻이 빈다. 단순 치환(전환하다)으로는 맞지 않는 경우.
15. navigation.md:226 | (b) | 낮음 | "두 키 모두 연속 안내를 다음 출현 지점으로 넘깁니다." | either key steps the chain on to its next spawn | 유지 가능. 14번을 "넘기다"로 맞추면 일관된다.
16. navigation.md:277 | (d) | 중간 | "설정은 … 모든 캐릭터가 함께 씁니다." | Settings are shared by all your characters | "설정은 … 모든 캐릭터가 공유합니다." | "쓰다" 단순 치환(사용하다)이 아니라 shared이므로 "공유하다".
17. navigation.md:295 | (b) | 중간 | "열린 창을 모두 닫아, 걷는 데 키를 자유롭게 쓸 수 있게 합니다." | so your keys are free for walking | "열린 창을 모두 닫아, 이동 키가 다시 캐릭터 이동에 사용되게 합니다." | keys are free의 직역. 부모의 take keys 방침과 묶을 것.
18. navigation.md:322 | (a) | 중간 | "클래식 경로에서는 요약이 그렇다고 말해 주고("마지막 25야드 직선")" | With classic routes the summary says so | "클래식 경로에서는 요약에서 이 사실을 알려 주고("마지막 25야드 직선")" | "그렇다고"가 가리키는 내용이 앞 문장 전체라 귀로 잡기 어렵다. 같은 says so: wownav.md:82 "경로를 네트워크 끝에서 마치고 그렇게 알려 줍니다" → "… 마치고 그 사실을 알려 줍니다".
19. navigation.md:334 | (c) | 중간 | "Enter로 길 안내 창에 넘깁니다." | with Enter handing over to the navigation window | "Enter를 누르면 그 항목을 목적지로 길 안내 창이 열립니다." | 무엇을 넘기는지 목적어가 없다.
20. navigation.md:303 | (a)(d) | 낮음 | "돌아서기가 잘못되면 버그 보고에 이것을 넣으십시오." | Include this in a bug report | "돌아서기가 잘못되면 버그 신고에 이 결과를 포함하십시오." | "이것", "넣다". 1-9의 보고/신고와 함께 처리.
21. navigation.md:153 | 유지 | "나중에 시점 전환 방식을 되돌리면 돌아서기가 엉뚱한 곳을 향합니다." | turns will land in the wrong places | land의 은유를 뜻으로 잘 풀었다. 방침 참고용 좋은 예.
22. navigation.md:213 | (d) | 낮음 | "기록은 … 실제 시간을 쓰며" | uses real time | "실제 시간을 기준으로 하며" | 단순 "사용하며"보다 뜻이 분명하다.

##### wownav.md
23. wownav.md:12 | (b) | 중간 | "모든 경로 요청이 WowNav로 갑니다." | Every route request goes to it | "모든 경로 요청을 WowNav가 처리합니다." | goes to의 직역. 192줄 "모든 경로 요청을 클래식 경로 대신 WowNav로 보냅니다"도 같다 → "… 대신 WowNav가 처리하게 합니다".
24. wownav.md:38 | (b) | 중간 | "데이터에서 물은 평평합니다." | Water is flat in the data. | "데이터는 물을 평평한 면으로만 다룹니다." | 귀로 들으면 뜻이 잡히지 않는다. 깊이 정보가 없다는 뜻을 원문 범위 안에서 풀었다.
25. wownav.md:40 | (a) | 중간 | "WowNav 데이터가 있는 곳에서 NPC나 물체에 스캐너의 Enter를 누르면, 그 대상이 그 지점 근처의 WowNav 장소 목록에 있을 경우 WowNav 자체 항목으로 높이까지 포함해 경로를 잡습니다." | the scanner's Enter on an NPC or object that WowNav's place list knows near that spot routes to WowNav's own entry of it, with its height | "… Enter를 누르면, 같은 위치 근처의 WowNav 장소 목록에 그 NPC나 물체가 있을 경우 WowNav에 등록된 항목의 위치와 높이로 경로를 잡습니다." | "그 대상이 그 지점"으로 지시어가 겹치고 "그 지점"의 선행어가 없다.
26. wownav.md:73 | (c) | 중간 | "지역이 아직 준비되지 않은 장소는 확인하지 않은 채 나오고, 고를 때 확인합니다." | A place whose zone has not been prepared yet is offered unchecked, and checked when you choose it. | "지역 데이터가 아직 준비되지 않은 장소는 이 확인을 거치지 않은 채 목록에 나오고, 그 장소를 고를 때 확인합니다." | 무엇을 확인하는지(앞 문장의 네트워크 지점 유무)가 빠졌다.
27. wownav.md:70 | (b) | 낮음 | "덧붙는 낱말은 장소의 분류에서 옵니다." | The extra words come from the categories of the place. | "덧붙는 낱말은 장소의 분류입니다." | come from 직역.
28. wownav.md:108 | (d) | 중간 | "Ctrl+W와 Ctrl+S는 경로 자체의 경유지를 하나씩 넘깁니다." | step along the route's own waypoints | 유지 가능. navigation.md:239를 "넘기다"로 맞추면 이 문장과 일관된다(14번).
29. wownav.md:110 | (b) | 중간 | "반대쪽 끝을 기다리는 이동 수단" | a transit that waits for its far end | "반대쪽 도착을 기다리고 있는 이동 수단 구간" | 이동 수단이 끝을 기다린다는 말이 통하지 않는다. 화면 문구 "차원문 구간 완료 대기 중"(139줄)과 같은 상태다.
30. wownav.md:140 | (b) | 중간 | "지금 있는 연결 구간을 계획에서 막고, 마지막으로 도착한 경유지에서 새 경로를 찾습니다." | The link you are on is blocked in the plan | "지금 있는 연결 구간을 경로 계산에서 제외하고, …" | "계획에서 막다"는 한국어로 통하지 않는다.
31. wownav.md:148 | (a) | 중간 | "WowNav는 이를 기록하고 어디로 무엇을 타고 가는지 알려 줍니다." | WowNav notes it and says where the ride goes and with what | "WowNav는 고른 승강장을 기억해 두고 어디로 무엇을 타고 가는지 알려 줍니다." | "이를"이 가리키는 것이 귀로 잡히지 않는다. 단 "기록한"은 로케일 값과 이어진다(3절).
32. wownav.md:156 | (d) | 낮음 | "바로 앞 지점까지 안내받고 다음과 같이 듣습니다." | you are guided to a point just before it and told | "바로 앞 지점까지 안내받고 다음 안내가 들립니다." | 설명서의 다른 곳은 모두 "…가 들립니다"이다.
33. wownav.md:196 | (b) | 낮음 | "장소가 네트워크에서 얼마나 떨어져 있어도 경로를 받을 수 있는지 정합니다" | How far from the network a place may lie and still get a route | "장소가 네트워크에서 얼마나 떨어져 있어도 경로를 잡을 수 있는지 정합니다" | 장소가 경로를 "받는다"는 직역. 같은 파일은 "경로를 잡다"를 쓴다.
34. wownav.md:92 | (e4) | 중간 | "여기서 경로 없음은 시작점에서 그 층에 갈 수 없다는 뜻입니다." | no path from here means that floor cannot be reached | "여기서 경로 없음이라는 말은 시작점에서 그 층에 갈 수 없다는 뜻입니다." | 문장 첫머리의 "여기서"가 화면 문구의 일부인지 부사인지 구분되지 않는다(1-8).

##### movement.md
35. movement.md:49 | (c) | 중간 | "실내에서 실외로, 또는 실외에서 실내로 옮겼다고 게임이 판단하면" | when the game decides that you changed from one to the other | "실내에서 실외로, 또는 실외에서 실내로 이동했다고 게임이 판단하면" | "옮기다"는 타동사라 목적어 없이 쓰면 뜻이 빈다.
36. movement.md:69 | (d) | 중간 | "값을 높이면 짧은 낙하는 울리지 않습니다" | A higher value hides short drops | "값을 높이면 짧은 낙하는 알리지 않습니다" | 낙하가 울리는 것이 아니다. (표 머리 "울리는 때"는 알림이 주어라 유지.)
37. movement.md:98 | (b) | 중간 | "게임이 대신 걸어 주는 이동도 다룹니다. 상호작용 단축키를 눌러 게임이 NPC에게 걸어가게 할 때나 마우스 이동을 쓸 때입니다." | It also covers walks that the game makes for you: when you press the interact key and the game walks you to an NPC, or you use click to move. | "게임이 캐릭터를 자동으로 이동시키는 경우에도 작동합니다. 상호작용 단축키를 눌러 게임이 캐릭터를 NPC에게 이동시킬 때나 마우스 이동을 사용할 때입니다." | "걸어 주는 이동"은 한국어로 어색하고, "게임이 NPC에게 걸어가게 할 때"는 누가 걷는지 빠졌다.
38. movement.md:125 | (b) | 높음 | "켜 두면 손이 닿지 않는 대상과 상호작용 단축키 등으로 상호작용할 때 캐릭터가 먼저 대상까지 걸어갑니다" | interacting with a target that is out of reach | "켜 두면 상호작용 범위 밖에 있는 대상과 상호작용 단축키 등으로 상호작용할 때 캐릭터가 먼저 대상까지 걸어갑니다" | out of reach 직역. 게임에서는 "범위 밖"이 관례다.
39. movement.md:141 | (c) | 중간 | "WowVision은 포기하기 전에 몇 초 동안(1초에 한 번씩 최대 8번) 다시 묻습니다." | WowVision asks again for a few seconds | "WowVision은 포기하기 전에 몇 초 동안(1초에 한 번씩 최대 8번) 게임에 시체 위치를 다시 확인합니다." | 누구에게 무엇을 묻는지 빠져서 사용자에게 묻는 것으로 들린다.
40. movement.md:162 | (c) | 중간 | "수영(또는 비행)을 시작하면 저절로 걸리고, 땅에 서거나 비행 경로를 타는 즉시 풀립니다." | It engages by itself … and lets go | "수영(또는 비행)을 시작하면 고정이 저절로 걸리고, 땅에 서거나 비행 경로를 타는 즉시 풀립니다." | 목록 항목의 첫 문장인데 주어가 없어 무엇이 걸리는지 알 수 없다.
41. movement.md:169 | (b) | 낮음 | "애드온은 게임에서 상하 각도 한계를 다시 읽을 수 없으므로" | The game does not let addons read the pitch limit back | "애드온은 게임에 설정된 상하 각도 한계 값을 읽어 올 수 없으므로" | read back의 "다시"가 직역이다.
42. movement.md:21 | (b) | 중간 | "나침반 모듈은 캐릭터를 지켜보다가 주변 환경에 변화가 생기면 말합니다." | The Compass module watches your character and speaks when … | "나침반 모듈은 캐릭터의 상태를 계속 확인하다가 주변 환경에 변화가 생기면 알려 줍니다." | watch 방침(부모 집계)에 따른다.

#### 3. 로케일 값 문제(설명서만 고칠 수 없음)
- wownav.md:139, 164 "기록한 승강장", "기록한 아우버다인행 배 선착장까지 타고 가는 중" | koKR navigation.lua:267 `L["Riding to the noted dock %s"] = "기록한 %s까지 타고 가는 중"` | 확신도 낮음 | noted를 "기록한"으로 옮겼는데 실제 뜻은 "기억해 둔 승강장"이다. 본문 31번을 "기억해 두다"로 고치면 화면 문구와 낱말이 갈리므로 koKR과 함께 판단해야 한다.
- 그 밖에 이 범위의 따옴표 인용 문구에서 설명서와 로케일이 어긋난 곳은 찾지 못했다. movement.md:152와 navigation.md:153의 대화창 메시지에 있는 "바꿀 수 있습니다"는 로케일 인용이므로 유지한다.

#### 4. 문제없다고 판단해 넘긴 것(과잉 수정 방지 메모)
- "영혼으로 전환"(movement.md:131, 135, 137): 게임 공식 DEATH_RELEASE = "영혼으로 전환"(gs_koKR.csv:10089). 유지.
- "대상으로 잡다", "경로를 짜다/잡다", "돌려세우다", "…한 것으로 치다": 뜻이 통하고 일관된다.
- navigation.md:169 "대화창에는 아무것도 쓰지 않습니다": 여기서 "쓰다"는 write다. "쓰다 → 사용하다" 일괄 치환에서 제외해야 한다.
- wownav.md:62 "서 있는 곳이 분명하면", navigation.md:239 "구간의 시작보다 앞에서": decisions.tsv 2026-11-09(원문 그대로)에 따라 손대지 않는다.
- navigation.md:224 "도착할 때마다 이 키를 다시 누르면"(Chain the key): 은유를 뜻으로 잘 풀었다.

---

### part-world2: world/targeting, quests, scanner, minimap, combat 감수

범위 5개 파일을 영어 원문과 한 줄씩 대조해 끝까지 읽었다. 줄 번호는 한국어 파일 기준이다.
형식: `파일:줄 | 부류 | 확신도 | 현재 한국어 | 영어 원문 | 수정안 | 이유`

부류: (a) 지시어 대상 불명 (b) 영어 관용구·은유 직역 (c) 주어·목적어 생략 (d) 동사·낱말 선택 (e1) 대소문자로 구분하던 용어가 한국어에서 합쳐짐 (e2) 일괄 치환 뒤 조사 불일치 (e3) 같은 영어 용어가 파일마다 다른 한국어 (e4) 사물이 "말한다/읽는다/안다"는 의인화 주어

#### 1. 반복 표현 (위치 목록 + 방침 제안)

##### 1-1. 물러나다 (step aside, stay out of the way) — (b) 높음
- combat.md:10, targeting.md:223, 227, 236
- 방침 제안: "물러나다"를 쓰지 않는다. WowVision 전체가 주어이면 "키 처리를 멈춥니다/창 탐색을 중단합니다", 기능이 주어이면 "작동하지 않습니다/작동을 멈춥니다". interface.md `## 전투`의 "완전히 물러납니다"와 같은 원문이므로 같이 정한다.
- combat.md:10 | b | 높음 | 그래서 WowVision은 전투가 시작되는 순간 물러납니다. | WowVision therefore steps aside the moment a fight begins | 그래서 WowVision은 전투가 시작되는 순간 창 탐색 기능을 멈춥니다. | "물러나다"는 무엇을 그만두는지 말해 주지 않는다. 바로 아래 목록이 멈추는 내용(키, 창 읽기)이다.
- targeting.md:223 | b | 높음 | 살아 있는 적을 대상으로 잡고 있는 동안에는 소프트 대상 지정이 물러나 있으므로 | soft targeting stays out of the way | ... 동안에는 소프트 대상 지정이 작동하지 않으므로 | 같은 표의 다음 행은 "꺼집니다", "작동합니다"로 써서 이 행만 은유다.
- targeting.md:227 | b | 높음 | ... 모드 모두 적을 직접 대상으로 잡았을 때만 물러납니다. | step aside only for enemies you target yourself | ... 잡았을 때만 소프트 대상 지정이 작동을 멈춥니다. | 주어가 "모드"라 "모드가 물러난다"로 들린다.
- targeting.md:236 | b | 높음 | 소프트 대상 지정이 물러나고 상호작용 단축키는 그 적에게 작용했을 것입니다. | soft targeting would step aside | 소프트 대상 지정이 작동하지 않고 ... | 위와 같음.

##### 1-2. 가져가다 / 되찾다 / 돌려주다 / 놓다 / 넘겨받다 (take, take back, hand back, release, take over) — (b) 높음
- combat.md:12, 17, 172, minimap.md:35
- 방침 제안: 키가 주어·목적어일 때 "WowVision이 키를 처리한다 / 게임이 다시 처리한다"로 통일한다(interface.md "키를 가져가는 때"와 같은 결정).
- combat.md:12 | b,c | 높음 | WowVision이 창 탐색에 가져가 쓰던 키(화살표 키, ..., 그리고 머물던 요소의 키)는 게임에 돌려줍니다. | The keys WowVision takes over to navigate its windows (..., and the keys of the element you were on) are handed back to the game. | WowVision이 창 탐색에 사용하던 키(화살표 키, ..., 그리고 초점이 있던 요소에서 사용하는 키)는 다시 게임이 처리합니다. | "가져가 쓰던", "머물던 요소"가 둘 다 은유다. 누가 머물렀는지도 빠져 있다.
- combat.md:17 | b,c | 높음 | WowVision은 필요한 키가 하나도 눌려 있지 않게 되는 즉시 키를 되찾고, 하던 곳에서 이어 갑니다. 열려 있던 창은 그대로 열려 있고, 전과 같은 요소에 있게 됩니다. | takes its keys back ..., and picks up where you were. ... you are on the same element as before. | ... 즉시 다시 키를 처리하기 시작하고, 전투 전 위치에서 이어집니다. 열려 있던 창은 그대로 열려 있고, 초점도 전과 같은 요소에 있습니다. | "하던 곳", "있게 됩니다"의 주어(초점)가 없다.
- combat.md:172 | b | 중간 | WowVision이 탐색 키를 가져가거나 놓을 때마다 출력하는 기록 기능을 켭니다. | takes and releases its navigation keys | WowVision이 탐색 키 처리를 시작하거나 끝낼 때마다 ... | 1-2 방침 적용.
- minimap.md:35 | b,c | 중간 | 스캔은 잠시 미니맵과 마우스 커서를 넘겨받으므로 몇 가지 조건을 갖춰야 합니다. 그렇지 않으면 스캔을 거부하거나 멈춥니다. | A scan temporarily takes over the minimap and the mouse cursor ... Otherwise the scan refuses or stops | 스캔하는 동안에는 미니맵과 마우스 커서를 스캔이 잠시 제어하므로 ... 그렇지 않으면 스캔이 시작되지 않거나 중간에 멈춥니다. | "스캔을 거부하거나"는 누가 거부하는지 없다.

##### 1-3. 오가다 (move between, jump ... and back, one level at a time) — (d) 높음
- quests.md:37, scanner.md:23, 30, 131
- 방침 제안: 초점 이동은 "이동합니다", 창 전환은 "전환합니다". 수정안은 모두 단순 치환이다("사이를 이동합니다", "한 단계씩 이동하는 방식/메뉴").

##### 1-4. 그곳에서는 (there) — (a) 중간
- quests.md:33, 84, scanner.md:154
- 방침 제안: 게임 버전을 받는 "there"는 버전 이름을 다시 말한다. 귀로는 "그곳"이 장소(게임 안 지역)로 들린다.
- quests.md:84 | a | 중간 | WowVision에는 Classic Era용 퀘스트 목록 창이 없으므로, 그곳에서는 게임 자체 퀘스트 목록을 읽지 않습니다. | so the game's own quest log is not read there | ... 없으므로, Classic Era에서는 게임 자체 퀘스트 목록을 읽지 않습니다. | 위 방침.
- quests.md:33 → "WoW: Forever에서는 게임 자체 퀘스트 데이터가 비어 있는 경우가 많기 때문입니다." / scanner.md:154 → "WoW: Forever에서는 게임 자체의 퀘스트 데이터에 빠진 것이 많아서".

##### 1-5. 들어가다 (포함의 뜻) — (d) 높음 (사용자 낱말 표: 들어가다 → 포함되다)
- minimap.md:16("미분류에 들어갑니다"), 52("스캐너(F9)에 들어가며", "항목이 들어가는 분류"), 172("퀘스트 목록에 어떻게 들어가는지"), combat.md:102("감속도 들어갈 수 있습니다"), 143("목록에 들어가므로"), scanner.md:119("경로에 대상의 높이와 층 정보가 들어가므로")
- 수정안: "포함됩니다/추가됩니다". 지역·그룹·상자에 실제로 들어가는 "들어가다"(quests.md:119, 159, scanner.md:19, 35 등)는 정상이라 제외했다.

##### 1-6. (~로) 치다 (count as) — (d) 중간
- minimap.md:109("사라진 것으로 칩니다"), combat.md:102("무엇을 군중 제어로 치는지는")
- 방침 제안: "간주합니다 / 군중 제어로 보는 것은". interface.md:88 "두 번 누르기로 치지 않습니다"도 같은 표현이다.

##### 1-7. 알다 / 모르다 (프로그램·데이터가 주어) — (e4) 중간
- scanner.md:79("데이터 원본이 그 퀘스트를 알 때만입니다. 모르는 퀘스트는"), 88("Questie가 모르는 퀘스트"), 119("WowNav가 모르는 대상"), minimap.md:61("퀘스트 데이터베이스가 같은 이름의 NPC를 이미 알고 있으면"), combat.md:143("게임이 아는 모든 메시지"), quests.md:10(표 머리 "아는 것")
- 방침 제안: "X에 정보가 있다/없다"로 쓴다. quests.md:188이 이미 "데이터 출처에 정보가 있는 퀘스트"로 옮겼으니 그 표현으로 맞춘다.
- minimap.md:61 | e4 | 중간 | 퀘스트 데이터베이스가 같은 이름의 NPC를 이미 알고 있으면 | If your quest database already knows an NPC of the same name | 퀘스트 데이터베이스에 같은 이름의 NPC가 이미 있으면 | 위 방침.
- combat.md:143 | e4,d | 높음 | 이것을 켜면 게임이 아는 모든 메시지가 목록에 들어가므로 미리 음소거할 수 있습니다. | the list also holds every message the game knows | 이것을 켜면 게임에 있는 모든 메시지가 목록에 포함되므로 ... | 1-5와 겹친다.

##### 1-8. 알아채다 (notice, recognise) — (d) 낮음
- minimap.md:18, 68, combat.md:33
- 방침 제안: "감지합니다/판단합니다". 뜻은 통하므로 다른 파일과 맞출 때만 고친다.

##### 1-9. 확인란 (checkbox) — (e3) 높음, 로케일 값과 어긋남
- quests.md:71(두 번), scanner.md:21, 35, 107
- koKR `L["Checkbox"] = "체크 상자"`이고 translation-guide도 "Checkbox → 체크 상자"다. targeting.md는 전부 "체크 상자"다. 화면에서 듣는 말은 "체크 상자"인데 설명서는 "확인란"이라 듣는 말과 읽는 말이 갈린다. → "체크 상자"로 통일.
- 범위 밖에도 있다(grep): basics/alerts.md, basics/tooltips.md, getting-started/installation.md, getting-started/sku-login.md, information/group-health.md.

##### 1-10. 선택 (choices를 명사 "선택"으로) — (d) 중간
- targeting.md:38("같은 선택을 씁니다"), 43, 44("전투 중일 때 쓰는 선택을 엽니다"), 209("선택: 게임 기본값, ..."), 218("선택 하나로 보여 줍니다"), 220(표 머리 "선택"), 229("선택: 게임 기본값, 끄기, 적, 친구")
- 같은 파일 211, 213행은 "선택지"다. → 고르는 값 목록은 "선택지", 38·43·44행은 "선택 항목"(예: "전투 중일 때 적용할 선택 항목을 엽니다", "소프트 대상 알림도 같은 선택 항목을 사용합니다").

##### 1-11. [알림](...)를 / [알림](...)와 — (e2) 높음
- quests.md:128, minimap.md:127("알림를"), minimap.md:173("알림와 [음성]")
- 경보 → 알림 일괄 치환(2026-11-07) 때 조사가 따라가지 않은 것으로 보인다(추정: 같은 파일 다른 곳은 "알림을"로 맞다). → "을", "과".
- 범위 밖에도 있다(grep): basics/menu-and-settings.md:48, 107, windows/chat.md:226. 전체에서 `알림\]\([^)]*\)[를와]`로 찾으면 된다.

##### 1-12. 스캐너 (Scanner와 the scanner가 같은 말이 됨) — (e1) 높음, minimap.md 전용
- 영어는 F9 창을 대문자 "Scanner", 미니맵 스캐너를 소문자 "the scanner"로 구분한다. 한국어는 둘 다 "스캐너"라 한 문단 안에서 가리키는 대상이 바뀐다.
- 미니맵 스캐너를 가리키는 "스캐너": minimap.md:6, 10, 12, 13, 16(첫 번째·세 번째), 18, 76, 80, 88
- F9 스캐너를 가리키는 "스캐너": minimap.md:4, 16(두 번째 "스캐너의 채집 분류"), 20, 46, 52, 74, 86, 141, 143, 170
- 방침 제안: 이 파일에서 소문자 the scanner는 "미니맵 스캐너"로 쓰고, "스캐너"는 F9 창에만 쓴다.
- minimap.md:16 | e1 | 높음 | 이런 점은 스캐너의 채집 분류에 미분류로 나열됩니다. 그런 추적 능력이 켜져 있는 동안에는 스캐너가 그런 점과 퀘스트 NPC를 구별하지도 못하므로 | They are listed as Unsorted, in the Gathering category of the Scanner. While such a tracking ability is on, the scanner also cannot tell ... | ... 스캐너의 채집 분류에 미분류로 나열됩니다. ... 동안에는 미니맵 스캐너가 그런 점과 퀘스트 NPC를 구별하지도 못하므로 | 연속한 두 문장의 "스캐너"가 서로 다른 것이다.
- minimap.md:76 | e1 | 높음 | 스캐너에 이름표가 필요하면 한 번 알려 줍니다 | If the scanner needs them it tells you once | 미니맵 스캐너에 이름표가 필요하면 ... | 바로 앞 문단(74행)의 "스캐너의 비컨"은 F9 스캐너다.

##### 1-13. 당기다 (pull) — (b) 중간
- combat.md:63("적을 잘못 당겼는지"), 100("적을 당길 때 흔한 예"), 110("몬스터 셋을 당깁니다")
- targeting.md:255는 같은 말 "before the pull"을 "전투를 시작하기 전에"로 옮겼다. 파일끼리 갈린다. 한국 WoW 사용자가 쓰는 말은 "풀링"이고 "당기다"는 직역이다. 방침 제안: "전투를 시작하다/적을 끌어오다" 중 하나로 정한다(예: 63행 "적을 너무 많이 끌어왔는지 빨리 알 수 있습니다", 110행 "몬스터 셋을 끌어옵니다"). 사용자 판단 필요(게임 은어 선택).

#### 2. 개별 사례

##### targeting.md
- targeting.md:17 | a | 중간 | 그 가상 주시 대상 칸에 저장한 유닛을 대상으로 잡습니다 | Targets the unit you stored in that virtual focus slot | 같은 번호의 가상 주시 대상 칸에 저장한 유닛을 대상으로 잡습니다 | 표 칸 안이라 "그"가 받을 앞말이 없다.
- targeting.md:25 | a | 중간 | 하드 대상이 새 유닛으로 변경될 때마다 WowVision이 그것을 읽습니다. | WowVision reads it out | ... 변경될 때마다 WowVision이 새 대상을 읽습니다. | "그것"이 유닛인지 변경 사실인지 불분명하다.
- targeting.md:129 | e4 | 중간 | 이제 전투 중에 대상으로 잡는 몬스터는 이름만 말합니다. | The next mob you target in combat says only its name. | 이제 전투 중에 몬스터를 대상으로 잡으면 이름만 들립니다. | 몬스터가 말하는 것으로 들린다.
- targeting.md:56 | e4 | 중간 | 유닛이 아닌 것(우편함, ...)은 항상 툴팁 글 전체를 읽습니다. | always speak their full tooltip text | 유닛이 아닌 것(우편함, ...)은 항상 툴팁 글 전체로 알립니다. | 우편함이 읽는 것으로 들린다. 199행 "유닛이 아닌 것은 툴팁 글이나 최소한 이름을 읽습니다"도 같다.
- targeting.md:227 | b | 중간 | 이 모드는 대상이 변경되거나 죽을 때마다 그에 맞춰 반영되며 | The mode follows every target change and also your target's death | 이 모드는 대상이 변경되거나 죽을 때마다 다시 적용되며 | "그에 맞춰 반영되며"는 무엇이 무엇에 반영되는지 없다.
- targeting.md:229 | d | 중간 | 게임이 실제 대상을 소프트 대상으로 변경하게 합니다. | lets the game turn your real target into the soft one | 게임이 소프트 대상을 실제 대상으로 삼게 합니다. | 설정 이름이 "소프트 대상을 하드 대상으로 지정"인데 본문은 방향이 반대로 들린다. turn into는 번역 지침상 "변경"이 아니다.
- targeting.md:235 | a | 중간 | 상호작용 소프트 대상이 변경될 때마다 WowVision이 그것을 말합니다. | WowVision says what the soft interact target is as it changes | ... 변경될 때마다 WowVision이 새 대상을 말합니다. | 25행과 같은 "그것".
- targeting.md:240 | a,c | 중간 | /wv soft는 현재 고정 모드와, ... | the current lock mode | /wv soft는 현재 하드 대상이 있을 때 소프트 대상 지정 모드와, ... | "고정 모드"라는 말은 이 페이지 어디에도 없다. reference/commands.md:139는 "소프트 대상 지정 모드"라고 쓴다. 원문도 모호하므로(lock mode) upstream-report 후보.
- targeting.md:259 | c | 중간 | 키를 누르면 저장된 이름을 대상으로 잡습니다. | Pressing it targets the stored name | 키를 누르면 저장된 이름의 유닛을 대상으로 잡습니다. | 이름을 대상으로 잡을 수는 없다.
- targeting.md:170, 173 | d | 낮음 | 풀려 있는 대상 | a target that is free | 군중 제어에 걸리지 않은 대상 | "풀려 있는"이 무엇에서 풀렸는지 한 번은 밝혀야 한다. 173행 첫 문장만 고쳐도 된다.

##### quests.md
- quests.md:16 | c | 중간 | Questie가 있으면 항상 작동합니다. | With Questie it always works. | Questie가 있으면 이 두 분류는 항상 작동합니다. | 주어가 없어 무엇이 작동하는지 안 들린다. 원문 it도 모호해서 decisions 2026-11-09(모호한 원문은 그대로 + 보고)에 걸릴 수 있다. 사용자 판단.
- quests.md:14 | b | 중간 | 게임이 자체 퀘스트 데이터를 주지 않는 빈틈을 채웁니다. | It fills the gaps where the game offers no quest data of its own. | 게임에 자체 퀘스트 데이터가 없는 부분을 보완합니다. | "빈틈을 채우다" 직역.
- quests.md:41 | b,c | 중간 | 퀘스트 목록이 퀘스트의 세부 정보로 열리면 그 자리에 그대로 머뭅니다. | If the quest log opens on a quest's details, you stay there. | 퀘스트 목록이 퀘스트 세부 정보가 표시된 상태로 열리면 초점은 세부 정보에 그대로 있습니다. | "세부 정보로 열리면", "그 자리"가 무엇인지, 누가 머무는지 없다.
- quests.md:64 | c | 중간 | 패널은 화면과 마찬가지로 목록 보기와 ... 중 하나를 보여 줍니다. | as it does on screen | 패널은 화면에 보이는 것과 마찬가지로 ... | "화면과 마찬가지로"는 패널과 화면을 비교하는 말로 들린다.
- quests.md:75 | c | 높음 | 세부 정보 보기가 열리면 퀘스트 제목에 놓입니다. | The details view opens on the quest's title. | 세부 정보 보기가 열리면 초점이 퀘스트 제목에 놓입니다. | 무엇이 놓이는지 없다.
- quests.md:80 | c | 높음 | 뒤로 버튼에서 Enter를 누르면 목록으로 돌아가며, 열었던 퀘스트에 놓입니다. | to return to the list, on the quest you opened | ... 목록으로 돌아가며, 초점은 열었던 퀘스트에 놓입니다. | 위와 같음.
- quests.md:47 | e4 | 낮음 | 선택된 퀘스트는 "선택됨"이라고 합니다. 지역 머리글은 "접힘" 또는 "펼쳐짐"이라고 합니다. | The selected quest says "selected". | 선택된 퀘스트에는 "선택됨"이 붙습니다. 지역 머리글에는 "접힘" 또는 "펼쳐짐"이 붙습니다. | 앞 문장이 "해당할 때 붙습니다"라 같은 동사로 맞추면 주어 혼동이 없다.
- quests.md:213 | d | 낮음 | Right를 다시 눌러 무엇을 처치해야 하는지 본 다음 | to see what to kill | ... 무엇을 처치해야 하는지 확인한 다음 | 독자가 듣는 사용자다. 22행 "퀘스트와 NPC를 봅니다"(look at)도 같다. 관용으로 넘어갈 수 있어 낮음.
- quests.md:10, 13 등 | e3 | 중간 | 출처 (data source) | source | — | 같은 "data source"가 quests.md에서는 "출처", scanner.md와 koKR("퀘스트 데이터 원본 없음")에서는 "원본"이다. quests.md:16은 한 문단 안에 "출처"와 화면 문구 "원본"이 함께 나온다. 로케일 값이 "원본"이므로 설명서를 "원본"으로 맞추거나 용어집에 올린다.

##### scanner.md
- scanner.md:30 | b | 중간 | 그러면 스캐너가 범주 목록에서 열리고, 목록을 열 때마다 새 목록이 이전 목록을 대신합니다: | The Scanner then opens on the list of categories | 그러면 스캐너를 열 때 범주 목록이 먼저 나오고, ... | "목록에서 열리고"(opens on) 직역.
- scanner.md:49 | d | 높음 | 창을 닫지 않고 목록을 최신으로 변경하려면 | To bring the lists up to date | 창을 닫지 않고 목록을 업데이트하려면 | "변경"은 원문이 change일 때만 쓴다(번역 지침). 낱말 표의 업데이트가 맞다.
- scanner.md:57 | b | 중간 | 그래서 모든 범주가 제자리를 지킵니다. | So every category keeps its place | 그래서 범주의 순서는 항상 같습니다. | "제자리를 지키다" 은유.
- scanner.md:73 | c | 중간 | 퀘스트 NPC를 미니맵 스캐너로 발견한 것뿐이면 | Where a giver is only a seen quest giver (found by the Minimap Scanner) | 퀘스트 NPC가 미니맵 스캐너로만 발견된 NPC이면 | "발견한 것뿐이면"의 구조가 귀로 안 풀린다. 92행은 "미니맵 스캔으로만 찾은 퀘스트 NPC"로 잘 옮겼다.
- scanner.md:80 | b | 중간 | 목표 진행에 세어지는 생물, 물체, 아이템 출처입니다. | that count towards it | 목표 진행에 포함되는 생물, 물체, 아이템 출처입니다. | "세어지는"은 쓰지 않는 피동형이다.
- scanner.md:80 | e3 | 중간 | 각 항목에는 다음 메모가 붙습니다: 부제, ... | its title | ... 칭호, ... | NPC 이름 아래 줄(title)을 targeting.md:86과 koKR(`L["Title"] = "칭호"`)은 "칭호"라 한다. minimap.md:74도 "칭호". 미확인: 이 자리가 koKR 값을 그대로 발화하는지는 코드 확인이 필요하다.
- scanner.md:37 | d | 낮음 | 한 단계 위로, 열었던 항목으로 돌아갑니다. | Go back one level, to the entry you opened. | 한 단계 이전으로 돌아가 열었던 항목에 놓입니다. | 사용자 표는 "한 단계 뒤로 → 한 단계 이전으로"다. 여기는 "위로"라 뜻은 통하지만 전체 방침을 정할 때 함께 본다.
- scanner.md:103 | d | 낮음 | 분류할 수 없었던 다른 추적 능력의 점이 들어 있습니다. | dots from other tracking abilities | ... 다른 추적 능력의 미니맵 점이 포함되어 있습니다. | 이 파일에서는 "점"이 처음 나온다. minimap.md는 첫 문단에서 "미니맵의 점"을 설명한다.
- scanner.md:109, 155 / minimap.md:13, 46, 98, 111 | e3 | 중간 | 추적 종류(scanner) / 추적 유형(minimap) | tracking type | — | 같은 말이 두 파일에서 갈린다. 하나로 정해 용어집에 올린다.

##### minimap.md
- minimap.md:50 | b | 낮음 | ### 결과가 가는 곳 | Where the results go | ### 결과를 확인하는 곳 | 제목이라 원문 구조 유지 규칙에는 걸리지 않는다. 뜻은 통하므로 낮음.
- minimap.md:111 | c | 중간 | 멈춰 서 있을 때, 전투 중일 때, ... 창이 있을 때는 건너뜁니다. | They are skipped while ... | ... 창이 있을 때는 알리지 않습니다. | "건너뜁니다"의 주어·목적어가 없다. 이 설명서에서 "건너뛰다"는 초점 이동(jump)에 쓰는 말이다.
- minimap.md:122 | b | 중간 | 커서가 게임 세계 위에 있지 않으면 스캔이 "창"으로 실패합니다. | scanning fails with "window" | ... 있지 않으면 스캔이 "창"이라는 메시지와 함께 실패합니다. | fails with 직역. "창으로 실패"는 뜻이 안 잡힌다.
- minimap.md:162, 164 | d | 낮음 | 걷기 기억 / 걷기 확인이 지금 기억하는 것 | the walking memory / the walking check | 걷는 중 확인 기록 / 걷는 중 확인이 지금 기억하는 것 | 본문은 "걷는 중 알림"인데 진단 표만 "걷기"다. 122행 "첫 걷기 확인"도 같다.

##### combat.md
- combat.md:15 | b | 중간 | 오른쪽 스틱 누르기처럼 월드에 필요한 키만 WowVision에 남습니다. | only the keys needed for the world ... stay with WowVision | ... 게임 세계에서 필요한 키만 WowVision이 계속 처리합니다. | "월드"는 이 설명서에 다른 곳에서 쓰지 않는 말이다(minimap.md:40은 "게임 세계").
- combat.md:41 | b | 중간 | WowVision은 내 생명력이나 마나를 스스로 알리지 않습니다. | does not announce ... by itself | WowVision은 내 생명력이나 마나를 자동으로 알리지 않습니다. | by itself 직역.
- combat.md:30 | b | 낮음 | WowVision을 쓸 때 드러나는 것은 다음과 같습니다. | These are the ones that you notice in WowVision | WowVision을 사용할 때 영향을 받는 것은 다음과 같습니다. | "드러나는 것"이 무엇인지(숨겨진 값의 영향) 흐리다.
- combat.md:104 | b | 중간 | 세 개 이상이 한꺼번에 걸리면(대개 광역 주문 하나) 개수가 됩니다. | become a count | ... 걸리면(대개 광역 주문 하나) 개수로 말합니다. | "개수가 됩니다"는 무엇이 개수가 되는지 없다.
- combat.md:106 | b,e4 | 중간 | 이름 미포함은 길어질 수 있는 이름("심판의 망치")을 건너뜁니다. | Without Names skips the names | 이름 미포함으로 두면 길어질 수 있는 이름("심판의 망치")을 말하지 않습니다. | 111행과 같은 "건너뛰다". 76행 "끄기는 단순한 수 세기를 유지합니다"도 같은 구조("끄기로 두면").
- combat.md:110 | b | 중간 | 전투 전체를 따라가려면 | to follow the whole fight | 전투 전체의 적 수를 들으려면 | follow 직역.
- combat.md:133 | b | 중간 | 지금까지 만난 모든 오류와 정보 메시지 목록이 나옵니다. | every error and info message you have met so far | 지금까지 나타난 모든 오류와 정보 메시지 목록이 나옵니다. | "메시지를 만나다" 직역. 143행은 "겪은"이라 한 파일 안에서도 갈린다.
- combat.md:161 | b | 낮음 | 매 프레임 되풀이되는 오류가 음성을 뒤덮지 않습니다. | does not flood speech | ... 오류가 음성을 가득 채우지 않습니다. | 뜻은 통한다.

#### 3. 로케일 값 문제 (설명서만 고칠 수 없음)

- scanner.md:73, 82, minimap.md:68, 152 | 로케일 값 | 중간 | "완료"(turn in) | turn in | — | koKR `L["turn in"] = "완료"`, `L["Complete"] = "완료"`가 같은 값이다. scanner.md:77의 퀘스트 상태 "완료"(Complete)와 82행의 완료 보고할 NPC 표시 "완료"(turn in)가 같은 말로 들린다. 고치려면 koKR `turn in`을 "완료 보고" 등으로 고쳐야 한다(quests.md는 본문에서 "완료를 보고할 상대"라고 쓴다).
- combat.md:156 | 로케일 값 연관 | 중간 | 오류 알림 알림으로 그대로 말합니다 | through the Announce Errors alert | 오류 알림(알림)으로 그대로 말합니다 | 설정 이름 "오류 알림"(Announce Errors, decisions 2026-11-07로 유지) 뒤에 alert의 "알림"이 붙어 "알림 알림"이 된다. 같은 파일 124행은 "오류 알림(알림)"으로 원문 괄호를 살렸다. 156행 원문에는 괄호가 없어서 설명서만으로는 깔끔히 못 고친다. 근본 해결은 Announce 계열 이름이다(사용자 결정 사항).
- targeting.md:191 | 로케일 값 | 참고 | "적 소프트 대상 사용함" / "적 소프트 대상 사용 안 함" | Enabled / Disabled | — | decisions 2026-11-09의 Disabled 키 분리(SettingDisabled) 병합 뒤 실제 발화와 맞는지 다시 확인할 곳이다. 지금 고칠 것은 아니다.

#### 4. 범위 밖에서 본 것 (한 줄씩)

- basics/interface.md는 navigation keys(10행)와 movement key(17행)를 둘 다 "이동 키"로 옮겼다. combat.md는 "탐색 키"와 "이동 키"로 구분한다(12, 172행). interface.md의 "키를 가져간다" 문단이 더 안 들리는 이유 하나다.
- combat.md:46의 링크 글자 "주 자원이 아닌 자원 지켜보기"는 information/buffers.md 제목과 묶여 있다("지켜보다" 전수 집계 때 함께 고쳐야 앵커가 안 깨진다).
- "단축키 화면"(targeting.md:19, 267, 272, scanner.md:6)과 "단축키 창"(minimap.md:24, combat.md:25)이 갈린다. 원문은 scanner·targeting·minimap·combat 모두 "keybinding window"다.

#### 5. 지적하지 않은 것

- decisions.tsv에 있는 문장(scanner.md:67 "이런 대원은 거리와 방향도 함께 나옵니다", minimap.md:166 mscan sku)은 건드리지 않았다.
- "쓰다 → 사용하다" 단순 사례는 부모 집계에 맡겼다.
- scanner.md:146 "영혼으로 전환합니다"는 게임 공식(DEATH_RELEASE "영혼으로 전환")이라 정상이다.
- 캐릭터가 실제로 도착하는 "도착"(scanner.md:117, 121, 142, minimap.md:72, 74, 150)은 정상이다. 이 5개 파일에는 초점 이동 뜻의 "도착하다"가 없다. "지켜보다", "한 단계 뒤로"도 본문에는 없다(combat.md:46 링크 글자 제외).
- minimap.md:80의 한국어 클라이언트 보충 설명은 decisions 2026-11-05 예외(한국어 사용자에게만 생기는 차이)에 해당해 그대로 뒀다.

---

### 감수 결과: windows 1 (social, auction-house, chat, group-finder, overview)

범위: `ko/windows/` 5개 파일을 `en/windows/` 같은 이름 파일과 끝까지 대조했다. 줄 번호는 ko 파일 기준이다.
부류: (a) 지시어 (b) 관용구·은유 직역 (c) 목적어·주어 생략 (d) 동사 선택 (e1) 용어 불일치 (e2) 조사 오류 (e3) 미번역 (e4) "X에서" 직역 (e5) 사람에게 이동.

#### 1. 반복 표현과 방침 제안

##### 1-1. switch를 "변경"으로 옮긴 곳 → "전환" (부류 d, 확신도 높음)

translation-guide `## 설명서` 문체 조항이 "switch는 전환하다"로 정했는데 아래가 남아 있다. 같은 파일 안에서도 갈린다(social.md:86은 "전환합니다").

- chat.md:83 "이전 또는 다음 대화 탭으로 변경합니다" (Switch to the previous or next chat tab) → "이전 또는 다음 대화 탭으로 전환합니다"
- chat.md:237 "이전 또는 다음 탭으로 변경하기" (Switch to the previous or next tab) → "이전 또는 다음 탭으로 전환하기"
- social.md:32 "Enter로 탭을 변경합니다" (Enter switches tab) → "Enter로 탭을 전환합니다"
- social.md:102 "누구 탭으로 변경합니다" (switch to the Who tab) → "누구 탭으로 전환합니다"
- auction-house.md:51 "Enter로 탭을 변경합니다" (Enter switches tabs) → "Enter로 탭을 전환합니다"
- group-finder.md:28 "그 탭으로 변경됩니다" (switches to it) → "그 탭으로 전환됩니다"
- group-finder.md:29 세 곳: "게임이 직접 탭을 변경할 때만", "탭을 변경한 직후", "평소처럼 탭이 변경됩니다" (switches the tab / right after switching / switches normally) → 모두 "전환"

become·turn into를 "변경"으로 옮긴 곳(같은 조항: turn into는 전환되다, replace는 대체하다):

- auction-house.md:60 "더 불러오기 버튼이나 스캔 버튼으로 변경됩니다" (They become Load More or Scan) → "더 불러오기 버튼이나 스캔 버튼으로 대체됩니다" (바로 위 59줄이 "스캔 중단 버튼으로 대체되고"다) | 확신도 중간
- auction-house.md:268 "결과가 구매 화면으로 변경됩니다" (The result becomes a purchase pane) → "결과 목록이 구매 화면으로 전환됩니다" | 확신도 중간

##### 1-2. "상황 메뉴" → "상황별 메뉴" (부류 e1, 확신도 높음, 설명서만 고치면 됨)

koKR `L["Context Menu"] = "상황별 메뉴"`(ui.lua:24, bindings.lua:66)이고 설명서 25개 파일이 "상황별 메뉴"를 쓴다. "상황 메뉴"는 이 두 파일에만 8곳 남아 있다.

- social.md:6, 141, 248, 355, 363
- group-finder.md:43, 103, 134

##### 1-3. "(사람)에게 이동합니다" → "(사람) 항목으로 이동합니다" (부류 e5, 확신도 높음~중간)

목록 안에서 초점을 옮기는 것인데, 귀로는 캐릭터가 그 플레이어에게 걸어간다는 뜻으로 들린다. 이 게임에는 실제로 플레이어에게 이동하는 기능(길 안내)이 있어서 더 헷갈린다. 설명서 전체에서 social.md 4곳뿐이다.

- social.md:146 "목록을 따라 친구에게 이동합니다" (Move through the list to the friend) → "목록에서 그 친구 항목으로 이동합니다"
- social.md:156 "친구 탭을 열고 친구에게 이동합니다" (move to the friend) → "친구 탭을 열고 그 친구 항목으로 이동합니다"
- social.md:199 "명단에서 구성원에게 이동합니다" (move to the member in the roster) → "명단에서 그 구성원 항목으로 이동합니다"
- social.md:276 "구성원 목록에 돌아가 그 플레이어에게 이동합니다" (move to the player) → "구성원 목록으로 돌아가 그 플레이어 항목으로 이동합니다"

##### 1-4. "X에서" (on a friend, on a player, on a card) (부류 e4, 확신도 중간)

영어 "on + 대상"을 "대상 + 에서"로 옮겨서, 사람·사물 이름 뒤에 바로 "에서"가 붙는다. "친구에서 Backspace를 누르고"는 귀로 들으면 뜻이 늦게 잡힌다. 방침 제안: 사람이나 추상 대상이면 "~ 항목에서"로 통일한다. 버튼, 머리글, 탭처럼 컨트롤 이름이면 지금대로 둔다("머리글에서 Enter"는 자연스럽다).

- social.md:45 "친구에서 쓰는 키:" (Keys on a friend) → "친구 항목에서 사용하는 키:"
- social.md:75 "친구에서 Backspace를 누르고" → "친구 항목에서 Backspace를 누르고"
- social.md:137 "카드에서:", 189 "구성원에서:", 203 "구성원에서 Backspace", 250 "길드 구성원에서 Enter", "커뮤니티 구성원에서는", 281 "구성원에서 Enter" → "~ 항목에서"
- social.md:313 "채널에서 Enter를 누르면 선택합니다" → "채널 항목에서 Enter를 누르면 그 채널을 선택합니다"
- chat.md:125~127 "플레이어에서는", "채널에서는", "링크에서는", "Battle.net 플레이어에서는" → "플레이어 부분에서는" 등(이 절은 메시지의 "부분"을 다루므로 "부분"이 맞다. 122줄이 "선택된 부분에서:"다)
- chat.md:153~155 "플레이어에서:", "채널에서:", "다른 링크에서:" → "플레이어 부분에서:" 등

##### 1-5. notice, pick up을 "알아차리다", "잡아내다"로 (부류 b, 확신도 중간)

프로그램 동작을 사람의 지각 동사로 옮겼다. interface.md:12는 같은 뜻을 "자동으로 감지됩니다"로 썼다. 방침 제안: notice, pick up, detect는 "감지하다"로 통일한다.

- overview.md:10 "WowVision은 창이 열린 것을 알아차리고 그 창을 WowVision 창으로 전환합니다" (WowVision notices that the window is open and turns it into a WowVision window) → "WowVision은 창이 열린 것을 감지하고 그 창을 WowVision 창으로 전환합니다"
- social.md:6 "게임이 창을 열면 WowVision이 이를 알아차리고 읽습니다" (WowVision notices when the game opens the window and reads it) → "게임이 창을 열면 WowVision이 감지해서 그 창을 읽습니다"
- chat.md:60 "게임이 이런 탭을 여는 즉시 잡아내므로" (picks these tabs up the moment the game opens them) → "게임이 이런 탭을 여는 즉시 감지하므로"
- chat.md:66 "WowVision이 탭을 잡아낼 때 이미 탭에 있던 줄" (Lines that were already in a tab when WowVision picked it up) → "WowVision이 탭을 감지했을 때 이미 그 탭에 있던 줄"

##### 1-6. 키를 "넘겨받다, 돌려주다, 가져가다, 놓다, 차지하다" (부류 b, 부모의 "가져가다" 방침과 묶을 것)

- overview.md:16 "키는 다시 게임으로 돌아갑니다" (your keys go back to the game) → "키 입력은 다시 게임이 처리합니다" | 중간
- overview.md:42 "게임은 전투 중에 애드온이 키를 넘겨받지 못하게 합니다. 전투가 시작되면 WowVision은 창 키를 게임에 돌려주고 창 읽기를 멈춥니다. 전투가 끝나면 키를 다시 넘겨받고, 전투 전에 머물렀던 요소에서 그대로 이어집니다." (The game does not let addons take over keys during a fight. ... hands its window keys back ... takes them back and you are where you left off) → "게임은 전투 중에 애드온이 키 입력을 처리하지 못하게 막습니다. 전투가 시작되면 창 키는 다시 게임이 처리하고, WowVision은 창 읽기를 멈춥니다. 전투가 끝나면 WowVision이 창 키를 다시 처리하고, 초점은 전투 전에 있던 요소에 그대로 있습니다." | 중간. 마지막 절 "그대로 이어집니다"는 주어가 없다(부류 c).
- chat.md:220 "대화 입력창이 키보드를 가져갈 때 나는 소리" (Sound when the chat box takes the keyboard) → "대화 입력창이 키보드 입력을 받기 시작할 때 나는 소리" | 높음. 같은 파일 209줄이 이미 "키보드 입력을 받기 시작할 때"로 옮겼다. 한 파일 안에서 갈린다.
- chat.md:221 "대화 입력창이 키보드를 놓을 때 나는 소리" (lets go of the keyboard) → "대화 입력창이 키보드 입력을 더 받지 않을 때 나는 소리" | 높음. 209줄과 같은 근거.
- chat.md:240 "이 세 동작은 메시지 목록에 초점이 있을 때만 그 키를 차지합니다" (They only hold their keys while the message list has the focus) → "이 세 키는 메시지 목록에 초점이 있을 때만 이 동작에 사용됩니다" | 중간
- auction-house.md:213 "WowVision이 게임의 목록 업데이트를 넘겨받으므로 검색 목록이 새로 고쳐지지 않습니다" (WowVision takes over the game's list updates) → "게임의 목록 업데이트를 WowVision이 대신 처리하므로 검색 목록이 새로 고쳐지지 않습니다" | 중간

##### 1-7. "도착하다", "오가다" 위치(부모 집계용)

단순 치환과 다른 것만 풀어 적는다.

- auction-house.md:26 "Ctrl+Tab으로 경매장 창과 가방 사이를 오갑니다" (switch between) → "전환합니다" (단순)
- chat.md:70 "창은 두 부분으로 되어 있고, Tab과 Shift+Tab으로 오갑니다" (which you reach with Tab and Shift+Tab) → "창은 두 부분으로 되어 있고, Tab과 Shift+Tab으로 두 부분 사이를 이동합니다". 원문이 switch가 아니라 reach라서 "전환"이 아니라 "이동"이 맞고, 목적어도 빠져 있다(부류 c). | 중간
- chat.md:121 "메시지에 도착하면" (When you arrive on a message) → "메시지로 이동하면" (단순)
- chat.md:147 "검색 결과는 대화에 시스템 메시지로 도착합니다" (Its answer arrives as a system message in your chat) → "검색 결과는 대화창에 시스템 메시지로 표시됩니다". 여기 "도착"은 초점 이동이 아니다. | 낮음
- chat.md:4, 16, 201과 auction-house.md:211, 322의 "메시지·데이터가 도착하다"는 통신 뜻이라 자연스럽다. 고치지 않는다.
- 이 5개 파일에 "가져가다(이동 키)", "지켜보다", "한 단계 뒤로"는 없다. 참고로 land on을 이미 잘 옮긴 예가 있다: social.md:61, 286과 auction-house.md:346의 "초점이 ~에 놓입니다", chat.md:72의 "초점이 먼저 이 목록으로 갑니다". land on 방침을 정할 때 이 표현을 후보로 쓸 수 있다.

##### 1-8. "떠 있는 창" (부류 d, 낱말 표: 뜨다·떠 있다, 확신도 중간)

- chat.md:42 "화면에 따로 떠 있는 창일 때만" (a window of its own on screen) → "화면에 따로 열려 있는 창일 때만"
- chat.md:73 "그다음 따로 떠 있는 창" (then windows that stand on their own) → "그다음 따로 열려 있는 창"

##### 1-9. 같은 영어를 파일마다 다르게 옮긴 용어 (부류 e1, 용어집 후보)

전체 설명서를 grep으로 센 값이다. 방침은 부모가 정한다.

- stop: "탭 정지점" 39회(interface, bags-and-bank, quests 등), "정지점" 115회(character, spells-and-talents, auction-house 등), "정지 지점" 9회(group-finder.md만). group-finder.md의 "정지 지점" 9곳(26, 35, 63, 96, 109 두 번, 117, 176 등)은 다른 파일과 맞춰야 한다. | 높음
- edit box: "편집 상자"(social 10, collections, professions 등), "입력 상자"(auction-house 5, interface), "입력 칸"(group-finder 3, bags-and-bank 3), "텍스트 상자"(interface, system), "입력란"(sku-login, navigation 등). WowVision이 실제로 읽는 컨트롤 종류 이름은 "편집"이다(translation-guide 문체 조항: Edit → 편집). 듣는 말과 맞추려면 "편집 상자"로 모으는 것이 근거가 있다. 범위 안: auction-house.md:43, 58, 110, 252, 253(입력 상자), group-finder.md:46, 99, 193(입력 칸). | 중간
- keybinding window: "단축키 창"과 "단축키 화면"이 파일마다 갈린다. 범위 안에서는 chat.md:232, 240과 group-finder.md:187이 "단축키 창", social.md:348이 "단축키 화면"이고 원문은 모두 keybinding window다. | 중간
- "X를 클릭 목록으로": chat.md:105 "같은 클릭을 목록으로 보여 줍니다", social.md:49 "위의 두 클릭을 메뉴로 나열합니다", social.md:165 "둘 다 나열합니다". 원문은 모두 "Shift+F10 lists ...". "메뉴로 나열합니다"로 통일을 제안한다. | 낮음

##### 1-10. 피동 "읽힙니다"와 능동 "읽습니다"가 파일마다 갈림 (부류 e1 문체, 확신도 낮음)

원문은 같은 "X reads ..."인데 group-finder.md는 "읽힙니다" 29회·"읽습니다" 6회, auction-house.md는 19회·16회, chat.md는 0회·12회, social.md는 5회·15회다. 설명서 문체 조항은 주어를 프로그램으로 두라고 했으므로 능동 "읽습니다"가 기준에 가깝다. 뜻은 통하므로 일괄 수정은 권하지 않고, 방침만 정해 두기를 제안한다.

#### 2. 개별 사례

`파일:줄 | 부류 | 확신도 | 현재 한국어 | 영어 원문 | 수정안 | 이유`

1. chat.md:226 | e2 | 높음 | "[알림](../basics/alerts.md)와 [음성](../basics/speech.md)을 참고하십시오" | see [Alerts] and [Speech] | "[알림](../basics/alerts.md)과 [음성](../basics/speech.md)을 참고하십시오" | 받침 있는 말 뒤라 "과"가 맞다. 2026-11-07에 경보를 알림으로 바꾸면서 조사가 남은 것으로 추정한다(미확인). 다른 파일에도 "알림와", "알림를", "알림가"가 남았는지 전수 검색이 필요하다.
2. auction-house.md:318 | e3 | 높음 | 예: "12 min 30 sec" | for example "12 min 30 sec" | 예: "12분 30초" | koKR `L["%s min %s sec"] = "%s분 %s초"`(auction.lua:87). 같은 파일 207줄은 "12분 30초"로 옮겼다.
3. auction-house.md:319 | e3 | 높음 | "스캔 중, 12 sec" | "Scanning, 12 sec" | "스캔 중, 12초" | koKR `L["%s sec"] = "%s초"`(auction.lua:89). 208줄은 "스캔 중, 45초"다.
4. chat.md:151 | b, c | 높음 | "각 항목은 선택된 부분에서 클릭 하나가 하는 일을 이름으로 말하고 그 뒤에 해당 클릭을 붙이므로, 키를 외울 필요가 없습니다" | It names what each click does for the selected part, followed by the click that does the same, so you do not need to remember the keys | "메뉴 항목마다 선택된 부분에서 할 수 있는 동작의 이름이 먼저 나오고, 그 뒤에 같은 동작을 하는 클릭이 붙습니다. 그래서 키를 외울 필요가 없습니다" | "클릭 하나가 하는 일을 이름으로 말하고"는 한 번 들어서 뜻이 잡히지 않는다.
5. auction-house.md:346 | a(귀로 구분 불가) | 높음 | "초점이 뒤로에 놓입니다" | Focus lands on Back | "초점이 뒤로 버튼에 놓입니다" | 버튼 이름 "뒤로"가 부사로 들린다. 같은 파일 268줄은 "뒤로 버튼"이라고 썼다.
6. auction-house.md:268 | a(귀로 구분 불가) | 중간 | "WowVision은 초점을 뒤로 버튼으로 옮기고 어느 결과에서 왔는지 기억하므로, 뒤로를 누르면 그 결과로 돌아갑니다" | WowVision moves the focus to its Back button and remembers which result you came from, so Back returns you there | "WowVision은 뒤로 버튼에 초점을 두고 어느 결과에서 왔는지 기억하므로, 뒤로 버튼을 누르면 그 결과로 돌아갑니다" | "초점을 뒤로"까지 들으면 초점을 뒤쪽으로 옮긴다는 뜻으로 들린다. 어순만 고치면 풀린다.
7. auction-house.md:168 | b | 중간 | "게임은 24시간으로 시작합니다" | The game starts on 24 Hours | "게임의 기본 선택은 24시간입니다" | "게임이 24시간으로 시작한다"는 뜻이 안 통한다. 184줄은 "기본으로 이미 선택되어 있습니다"로 썼다.
8. auction-house.md:142 | d, c | 중간 | "검색 탭과 같이 쓰지만 검색을 다시 실행하지는 않습니다" | used as on Browse (without searching again) | "사용법은 검색 탭과 같지만 검색을 다시 실행하지는 않습니다" | "같이 쓰다"는 "함께 쓰다"로 들린다.
9. auction-house.md:45 | d | 중간 | "가격은 항상 게임이 쓰는 그대로 읽힙니다" | Prices are always read out as the game writes them | "가격은 항상 게임에 표시되는 형식 그대로 읽습니다" | 원문은 write인데 "쓰다"가 use로 들린다.
10. auction-house.md:101 | d | 중간 | "지금 목록이 쓰는 정렬이면 "활성"을 읽습니다" | "Active" if it is the sort the list uses now | "지금 목록에 적용된 정렬이면 "활성"을 읽습니다" | "목록이 쓰는"은 사물 주어에 "쓰다"라 어색하다. 단순 "사용하는"으로 바꿔도 어색해서 따로 적는다.
11. auction-house.md:284 | a, c | 중간 | "Tab으로 그 사이를 이동하고 Enter로 누릅니다" | Tab moves between them, Enter presses one | "Tab으로 버튼 사이를 이동하고 Enter로 버튼을 누릅니다" | "그 사이"가 무엇의 사이인지, 무엇을 누르는지 빠졌다. group-finder.md:169는 "Tab으로 버튼 사이를 이동하고, Enter로 하나를 누릅니다"로 썼다.
12. group-finder.md:119 | a | 중간 | "Left와 Right로 그 사이를 이동하고, Enter로 하나를 체크하면" | Left and Right move along them; Enter ticks one | "Left와 Right로 체크 상자 사이를 이동하고, Enter로 하나를 체크하면" | "그 사이"가 가리키는 말이 한 문장 앞의 긴 나열이다.
13. auction-house.md:10 | b | 중간 | "총 가격이 낼 금액을 알려 주고 구매 버튼을 누르면 확인을 요청하므로" | Total Price tells you what you will pay, and Buy asks you to confirm | "총 가격 항목에서 낼 금액을 확인할 수 있고, 구매 버튼을 누르면 게임이 확인을 요청하므로" | "총 가격이 알려 주고"는 항목 이름이 주어인 직역이고, "확인을 요청"하는 주체도 빠졌다.
14. auction-house.md:8 | c | 낮음 | "창은 사용하는 도중에도 변경될 수 있고" | The window can change while you use it | "창의 내용은 사용하는 도중에도 변경될 수 있고" | 변경되는 것은 창이 아니라 창에 표시된 경매다.
15. chat.md:8, 10 | b | 중간 | "WowVision이 대화 탭을 따르는 방식", "WowVision은 게임에 있는 대화 탭을 그대로 따릅니다" | How WowVision follows your chat tabs / WowVision follows the chat tabs you have in the game | "WowVision이 대화 탭을 다루는 방식", "WowVision은 게임에 있는 대화 탭 구성을 그대로 사용합니다" | "탭을 따르다"는 무엇을 한다는 것인지 잡히지 않는다. 뒤 문장들이 "탭 구성과 수신 설정은 게임이 정한다"는 뜻을 설명한다.
16. chat.md:16 | b | 중간 | "읽기가 허용된 탭에 메시지가 도착하면" | When a message arrives in a tab that is allowed to speak | "메시지를 읽도록 설정된 탭에 메시지가 도착하면" | 같은 파일 23줄이 "읽도록 설정된 탭"이다. "허용"은 권한처럼 들린다.
17. chat.md:35 | b | 중간 | "끄면 탭은 조용해집니다(기록은 계속 보관합니다)" | When off, the tab is silent (its history is still kept) | "끄면 이 탭의 메시지를 읽지 않습니다(기록은 계속 보관합니다)" | silent 직역.
18. chat.md:246 | b | 중간 | "읽던 탭이 조용합니다" | A tab you read is silent | "보고 있던 탭의 메시지를 읽어 주지 않습니다" | 문제 해결 목록의 증상 문장인데 "읽던 탭"과 "조용합니다"가 둘 다 모호하다.
19. chat.md:45 | b, c | 중간 | "첫 번째 탭(일반 탭)의 설정은 대화 알림이 하나뿐이던 이전 버전의 WowVision에서 이어집니다" | The settings of the first tab (the General tab) carry over from older versions of WowVision | "첫 번째 탭(일반 탭)은 대화 알림이 하나뿐이던 이전 버전 WowVision의 설정을 그대로 이어받습니다" | "~에서 이어집니다"는 무엇이 이어지는지 흐리다.
20. chat.md:77 | b | 중간 | "최신 메시지에서 열립니다" | It opens on the newest message | "창을 열면 초점이 최신 메시지에 있습니다" | open on 직역. 72줄 "창을 열면 초점이 먼저 이 목록으로 갑니다"와 같은 방식으로 맞춘다.
21. group-finder.md:54, 142 | b | 중간 | "창이 등록 탭으로 열립니다", "창이 던전 및 공격대 탭으로 열립니다" | The window opens on the Listing tab / on the Group Finder tab | "창이 열리고 등록 탭이 선택되어 있습니다", "창이 열리고 던전 및 공격대 탭이 선택되어 있습니다" | 위와 같은 open on 직역. "탭으로 열린다"는 탭이 수단처럼 들린다.
22. group-finder.md:56 | c | 중간 | "이제 활동에 있습니다" | You are now in Activities | "이제 초점이 활동 목록에 있습니다" | 주어가 없고 "활동에 있다"는 뜻이 잡히지 않는다.
23. group-finder.md:151 | c | 중간 | "WowVision은 전투 준비 확인이라는 창을 열고 초점을 옮깁니다" | WowVision opens a window named Ready Check and focuses it | "WowVision은 전투 준비 확인이라는 창을 열고 그 창으로 초점을 옮깁니다" | 초점을 어디로 옮기는지 빠졌다.
24. group-finder.md:138 | b | 중간 | "게임이 던전 찾기 화면을 메시지로 덮습니다" | the game covers the finder with a message | "게임이 던전 찾기 화면 위에 메시지를 표시합니다" | 시각 은유 직역.
25. group-finder.md:29 | c | 중간 | "등록을 올리는 일은 게임이 직접 탭을 변경할 때만 되기 때문입니다" | because posting a listing only works when the game itself switches the tab | "게임이 직접 탭을 전환했을 때만 등록을 올릴 수 있기 때문입니다" | "~하는 일은 ~할 때만 되기"가 귀로 따라가기 어렵다. 1-1의 "전환"도 함께 적용한다.
26. group-finder.md:112~113 | b | 낮음 | "열린 버튼은 "선택됨"으로 읽힙니다. Enter로 엽니다.", "열린 버튼의 페이지" | The open one reads "selected". Enter opens it. / The page of the open button | "선택된 버튼은 "선택됨"으로 읽힙니다. Enter로 선택합니다.", "선택된 버튼의 페이지" | 버튼이 "열려 있다"는 말이 어색하다. 원문도 open이라 확신도는 낮다.
27. group-finder.md:157, 161 | d | 낮음 | "두 버튼은 게임 자체의 글을 씁니다", "제목은 게임의 것을 그대로 씁니다" | The two buttons use the game's own texts / under the game's own title | "두 버튼의 이름은 게임 자체의 문구입니다", "제목은 게임의 제목 그대로입니다" | "글을 쓰다"가 write로 들린다.
28. social.md:40 | d | 중간 | "친구 한 명은 한 번에 낭독됩니다" | Each friend is announced in one go | "친구 한 명의 정보는 한 번에 이어서 읽습니다" | "낭독"은 이 설명서에서 여기에만 나오고, 다른 곳은 모두 "읽다"다.
29. social.md:38 | d | 중간 | "목록에는 게임이 쓰는 순서대로 친구가 있습니다" | The list holds your friends in the order the game uses | "목록에는 게임과 같은 순서로 친구가 나열됩니다" | "게임이 쓰는 순서"와 "친구가 있습니다"가 둘 다 어색하다.
30. social.md:57 | c | 중간 | "요청에 초점이 있을 때 Tab을 누르면 수락에, 한 번 더 누르면 거절에 갑니다. 거절은 거절, 차단, 신고가 있는 드롭다운입니다. 둘 다 게임 자체의 버튼을 누릅니다." | Tab reaches Accept, and Tab again reaches Decline, a dropdown with decline, block and report. Both press the game's own buttons. | "요청에 초점이 있을 때 Tab을 누르면 수락 버튼으로, 한 번 더 누르면 거절 버튼으로 이동합니다. 거절 버튼은 거절, 차단, 신고가 있는 드롭다운입니다. 수락과 거절 모두 게임 자체의 버튼을 대신 누릅니다." | "거절은 거절, 차단"은 귀로 들으면 같은 말이 겹치고, "둘 다 ~ 누릅니다"는 주어가 무엇인지 흐리다.
31. social.md:80 | c | 중간 | "차단한 플레이어가 있는 차단 목록 제목이 있고" | It has a heading Ignore List with the players you ignore | "차단 목록이라는 제목 아래에 차단한 플레이어가 있고" | 꾸미는 말이 길어 "제목이 있다"는 것인지 "플레이어가 있다"는 것인지 늦게 잡힌다.
32. social.md:140, 227 | b | 중간 | "Backspace는 게임에서 그 카드의 메뉴를 엽니다", "Backspace는 게임에서 그 항목의 메뉴를 엽니다" | Backspace opens the game's menu for it | "Backspace는 그 카드의 게임 메뉴를 엽니다", "Backspace는 그 항목의 게임 메뉴를 엽니다" | "게임에서"가 장소로 들린다. group-finder.md:80은 "그 등록의 게임 메뉴를 엽니다"로 썼다.
33. social.md:348 | b | 중간 | "자신을 대상으로 지정했으면 모든 인스턴스 초기화, 전리품, 던전 난이도를 제공합니다" | With yourself targeted it offers Reset All Instances, loot and dungeon difficulty | "자신을 대상으로 지정했으면 메뉴에 모든 인스턴스 초기화, 전리품, 던전 난이도가 나옵니다" | offer 직역. "난이도를 제공한다"는 뜻이 다르게 들린다.
34. social.md:277 | d | 중간 | "Enter를 눌러 구성원 카드를 열고 파티 초대를 씁니다" | press Enter for the member card and use Group Invite | "Enter를 눌러 구성원 카드를 열고 파티 초대 버튼을 실행합니다" | 단순히 "사용합니다"로 바꿔도 어색하다. decisions.tsv 2026-11-08(테스터 안내)의 "X 버튼을 실행합니다"와 맞춘다.
35. social.md:338 | b | 낮음 | "메뉴 단계마다 따로 이동하는 구역이 됩니다" | Each menu level is a separate stop | "메뉴 단계마다 별도의 정지점이 됩니다" | 다른 곳의 stop 번역(1-9)과 맞춘다.
36. chat.md:166 | b | 중간 | "그동안 WowVision은 줄 안을 들여다볼 수 없습니다" | WowVision cannot look inside the lines then | "그동안 WowVision은 줄 안의 이름과 링크를 읽어 낼 수 없습니다" | look inside 의인화 직역. 뒤 목록이 영향받는 것(이름·링크 클릭)을 설명하므로 뜻을 덧붙이는 것은 아니지만, 원문에 없는 낱말이 들어가므로 "줄의 내용을 분석할 수 없습니다"도 후보다.
37. chat.md:168 | b | 중간 | "동작하지 않고 "여기서는 링크 사용 불가"라고 답합니다" | answer "Links unavailable here" instead of acting | "동작하지 않고 "여기서는 링크 사용 불가"라고 말합니다" | 키가 "답한다"는 의인화다. 바로 아래 169줄은 "말합니다"다.
38. chat.md:109 | b | 중간 | "WowVision은 같은 클릭을 제공합니다" | WowVision gives you the same clicks | "WowVision에서도 같은 부분을 클릭할 수 있습니다" | "클릭을 제공한다"는 직역.
39. chat.md:201 | b | 중간 | "대화 탭 버퍼는 최신 줄에서 시작해 새 줄이 도착하는 대로 따라갑니다" | A chat tab buffer starts on the newest line and follows new lines as they arrive | "대화 탭 버퍼는 최신 줄에서 시작하고, 새 줄이 들어오면 그 줄로 자동으로 이동합니다" | "따라갑니다"의 목적어가 없다.
40. chat.md:190 | d | 낮음 | "대화 창에서 탭 줄을 열고" | open the tab strip | "대화 창에서 탭 줄로 가서" | 탭 줄은 여는 것이 아니라 Tab으로 가는 구역이다. 같은 파일 180줄은 "탭 줄로 가서"다. 원문이 open이라 확신도는 낮다.
41. overview.md:4 | b | 낮음 | "비장애인 플레이어는 마우스로 이 창들 안을 클릭합니다" | A sighted player clicks around in them with the mouse | "비장애인 플레이어는 이 창들을 마우스로 클릭해서 다룹니다" | "창들 안을 클릭한다"가 어색하다.

#### 3. 로케일 값 문제 (설명서만 고칠 수 없음)

1. `L["Controls"] = "조작"`(ui.lua:216) | 확신도 중간 | social.md:30, 51, 66, 82, 88, 96, 105, 229, 269와 loot-trade-mail 등에서 구역 이름으로 인용된다. "Tab으로 조작에 가서", "조작에는 ~ 버튼이 있습니다"는 귀로 들으면 구역 이름이 아니라 일반 명사 "조작"으로 들려 뜻이 끊긴다. 후보는 "컨트롤" 또는 "조작 버튼"이다. koKR을 고치면 설명서 인용은 `tools.sync_locale`이 따라간다.
2. `L["items updated"] = "개 아이템 갱신"`(auction.lua:51) | 확신도 중간 | auction-house.md:211, 322의 "전체 스캔 완료, 3200 개 아이템 갱신". 낱말 표(갱신 → 업데이트)와 어긋난다. 화면 문구 인용이라 설명서는 실물을 따른 것이 맞고, 고친다면 koKR에서 "개 아이템 업데이트"로 고친다.
3. `L["Day Mean"] = "일간 평균"`과 코드가 붙이는 하이픈 | 확신도 중간 | auction-house.md:220, 231의 "7-일간 평균". decisions.tsv 2026-11-05는 영어 복합어 하이픈을 옮기지 않는다고 했는데, 여기 하이픈은 코드가 숫자와 "Day Mean" 사이에 넣는 것으로 추정한다(미확인: WowVision 저장소에서 `L["Day Mean"]` 사용처를 봐야 한다). 코드가 넣는 것이면 번역으로 고칠 수 없으므로 `docs/upstream-report.md` 대상이다.
4. `L["Available"] = "사용 가능"`(ui.lua:69) | 기결정 | auction-house.md:260, 271, 345의 "구리 광석, 5 실버, 사용 가능 340". decisions.tsv 2026-11-09에 따라 원본 키 분리 PR(AuctionAvailable → "구매 가능 수량") 병합을 기다리는 중이다. 병합되면 이 세 줄도 따라 바뀌어야 한다.
5. `L["Vendor price per item"] = "개당 상인에게 파는 가격"`(auction.lua:61) | 확신도 낮음 | auction-house.md:326. "개당"이 "상인"을 꾸미는 것처럼 들린다. 후보는 "상인에게 파는 개당 가격"이다.
6. `L["Link %s in Chat"] = "대화창에 %s 링크 걸기"`(chat.md:155 인용) | 확신도 낮음 | 같은 동작을 interface.md:42와 201은 "대화창에 아이템 링크를 넣습니다", "대화창에 아이템 링크 넣기"라고 설명한다. "링크 걸기"와 "링크 넣기"가 갈린다. 화면 문구는 실물을 따르는 것이 맞으므로, 맞춘다면 koKR 값을 기준으로 정한다.

참고(로케일 값 아님, 게임 공식 문자열로 추정): social.md:179의 버튼 이름 "갱신"(Update), auction-house.md:67의 "새로고침"(Reset), social.md:75의 "쪽지 설정"(Set Note)은 koKR에 없다. 게임 자체 버튼 이름으로 보이므로(미확인: `cache/gs_koKR.csv` 대조 필요) 실물 유지가 맞다. 다만 social.md는 같은 것을 42, 73, 76줄에서 "메모", 75, 193, 205줄에서 "쪽지"로 부르고 있어 독자가 같은 것인지 헷갈릴 수 있다.

#### 4. 건수

- (a) 지시어: 4건 (개별 5, 6, 11, 12)
- (b) 관용구·은유 직역: 개별 20건 + 반복 1-5(4곳), 1-6(6곳)
- (c) 목적어·주어 생략: 개별 8건(b와 겹치는 것 포함)
- (d) 동사 선택: 개별 8건 + 반복 1-1(switch 9곳, become 2곳), 1-8(2곳)
- (e1) 용어 불일치: 상황 메뉴 8곳(높음), 정지 지점 9곳, 편집 상자 계열, 단축키 창·화면, 피동·능동
- (e2) 조사 오류: 1건(chat.md:226 "알림와")
- (e3) 미번역: 2건(auction-house.md:318, 319)
- (e4) "X에서" 직역: 약 17곳
- (e5) "(사람)에게 이동": 4곳
- 로케일 값 문제: 6건(기결정 1건 포함)

---

### 감수 결과: windows 2부

범위: `ko/windows/`의 loot-trade-mail, action-bars, npcs, character, professions, bags-and-bank, system, collections, spells-and-talents (9개 파일, 전부 끝까지 읽음). 영어는 의심 줄만 `en/windows/` 같은 파일의 (한국어 줄 번호 - 1) 줄과 대조했다. 줄 번호는 한국어 파일 기준이다.

부류: (a) 지시어 (b) 관용구·은유 직역 (c) 목적어·주어 생략 (d) 동사 선택 (e1) 무생물 주어 + 읽다/말하다 (e2) 파일 간 용어·표기 불일치 (e3) "변경하다" 과적용(뜻은 이동·전환)

총평: 이 9개 파일은 interface.md보다 상태가 낫다. "가져가다", "지켜보다", "한 단계 뒤로"는 거의 없다. 반복되는 문제는 아래 반복 표현 1~6이고, 나머지는 개별 사례다.

#### 반복 표현과 방침 제안

##### 1. you land on / opens on → "놓입니다" (주어 없음) [c, b]

주어 없이 "~에 놓입니다"라고만 쓴 곳은 무엇이 놓이는지 들리지 않는다. 같은 파일 묶음 안에 이미 좋은 형태("초점이 여기에 놓입니다", professions 6곳)가 있으므로 그쪽으로 통일한다.

- 주어 없음(수정 대상): action-bars.md:22, character.md:30, character.md:90, spells-and-talents.md:32, 47, 79, 118(한 줄에 2회)
- 이미 "초점이 ~에 놓입니다"(수정 불필요): professions.md:37, 75, 91, 142, 179, 199
- action-bars.md:130은 "주문은 … 단축바에 놓입니다"로 다른 뜻(수정 불필요)

방침 제안: land on / opens on → "초점이 ~에 놓입니다" 또는 "~에서 시작합니다"(bags-and-bank.md:129, 141, 150과 system.md:28이 이미 "~에서 시작합니다"). 둘 중 하나로 통일. "도착하다"보다 둘 다 낫다.

대표 사례:
- character.md:90 | c | 높음 | C를 누릅니다. 장비 목록에 놓입니다. | Press C. You land on the equipment list. | C를 누릅니다. 초점이 장비 목록에 놓입니다. | 주어가 없어 무엇이 놓이는지 알 수 없다
- action-bars.md:22 | c | 높음 | 넘어가면 그 단축바의 첫 칸에 놓입니다. | You land on the first slot of that bar. | 넘어가면 초점이 그 단축바의 첫 칸에 놓입니다. | 위와 같음
- spells-and-talents.md:118 | c | 높음 | 탭 정지점에 놓입니다(전문화 줄이 있으면 그 줄에 놓입니다). | You land on the tabs stop (or on the specialization row if you have one). | 초점이 탭 정지점에 놓입니다(전문화 줄이 있으면 그 줄에 놓입니다). | 위와 같음

##### 2. walk / move through → 훑다, 돌아다니다, 따라가다, 오가다 [b, d]

walk가 파일마다 다른 은유로 옮겨졌다. 모두 "이동하다"면 된다.

- 훑다: character.md:4, 70, 74
- 돌아다니다: professions.md:4, 61
- 따라가다: spells-and-talents.md:120, 170
- 오가다(move through/between, switch): loot-trade-mail.md:73(switch between → 전환), 77(move between → 이동), 134(Tab chain between fields), character.md:4, spells-and-talents.md:27, 96

방침 제안: walk, move through, move along → "이동하다". switch between → "전환하다". "오가다·훑다·돌아다니다·따라가다"는 설명서에서 쓰지 않는다.

대표 사례:
- professions.md:61 | b | 높음 | Up과 Down으로 줄을 돌아다닙니다. | Walk the lines with Up and Down. | Up과 Down으로 줄 사이를 이동합니다. | "돌아다니다"는 정처 없이 다닌다는 뜻이라 목록 이동에 맞지 않는다
- character.md:4 | b | 높음 | WowVision은 이 창을 Tab으로 오가는 여러 정지점으로 읽고, 각 탭의 내용을 화살표 키로 훑는 목록으로 배치합니다. | WowVision reads it as a set of stops you move through with Tab, with the contents of each tab laid out as lists you walk with the arrow keys. | WowVision은 이 창을 Tab으로 이동하는 여러 정지점으로 읽고, 각 탭의 내용은 화살표 키로 이동하는 목록으로 보여 줍니다. | 오가다·훑다 두 은유가 한 문장에 겹친다
- spells-and-talents.md:170 | b | 중간 | Left와 Right로 그 줄의 특성을 따라갑니다. | Left and Right walk the talents of that row. | Left와 Right로 그 줄의 특성 사이를 이동합니다. | "특성을 따라간다"는 뜻이 통하지 않는다
- loot-trade-mail.md:73 | d | 높음 | (Ctrl+Tab으로 둘 사이를 오갑니다.) | (Press Ctrl+Tab to switch between them.) | (Ctrl+Tab으로 두 창을 전환합니다.) | switch → 전환(사용자 지적 3과 같은 부류)

##### 3. the game draws → 그리다 [b]

화면에 "그린다"는 개발자 말투다. 같은 파일들에 "게임이 표시하는"이 이미 많다.

- 위치: action-bars.md:57, bags-and-bank.md:22, 109, 129, 134, collections.md:132
- 방침 제안: draw → "표시하다".
- 대표: bags-and-bank.md:109 | b | 높음 | 이 버전들에서는 게임이 정렬 버튼을 그리더라도 WowVision이 정렬 버튼을 읽지 않습니다. | WowVision reads no sort button on these versions, even where the game draws one. | 이 버전들에서는 게임이 정렬 버튼을 표시하더라도 WowVision이 정렬 버튼을 읽지 않습니다. | 버튼을 "그린다"는 사용자 말이 아니다
- 대표: collections.md:132 | b | 중간 | 그다음 그려진 순서대로 각 부위를 … 읽습니다. | then every piece in the order drawn | 그다음 화면에 표시된 순서대로 각 부위를 … 읽습니다. | 위와 같음

##### 4. popup → 뜨다, 띄우다 [d, 낱말 표]

낱말 표와 translation-guide("창이 뜨다 → 열리다")에 이미 있는 규칙인데 남아 있다.

- 위치: npcs.md:30(확인 팝업이 뜹니다), loot-trade-mail.md:107(게임이 팝업을 띄웁니다), character.md:82(확인 팝업을 띄우며), professions.md:70(시전 바를 띄우며)
- 방침 제안: 팝업·창이 뜨다 → 열리다, 띄우다 → 열다. 시전 바는 "표시하다".
- 대표: npcs.md:30 | d | 높음 | NPC가 대답하며, 대개 확인 팝업이 뜹니다. | The NPC answers, probably with a confirmation popup. | NPC가 대답하며, 대개 확인 팝업이 열립니다. | 가이드의 "창이 뜨다 → 열리다"
- 대표: professions.md:70 | d | 중간 | 그러면 게임이 평소처럼 시전 바를 띄우며 아이템을 만듭니다. | The game then makes the items with its normal cast bar. | 그러면 게임이 평소처럼 시전 바를 표시하며 아이템을 만듭니다. | 위와 같음

##### 5. A slot reads / What a slot says → 무생물 주어 + 읽다·말하다 [e1, 새 부류]

원문의 "Each slot reads X"(칸에서 X가 읽힌다)를 "각 칸은 X를 읽습니다"로 옮겨서, 칸·편지·아이템이 스스로 읽는 것처럼 들린다. 읽는 주체는 WowVision이다. 같은 제목 "What a slot/item/entry says"도 세 가지로 갈렸다.

- 제목: action-bars.md:47 "칸이 말하는 내용", bags-and-bank.md:27 "칸이 읽는 내용", npcs.md:45 "아이템이 읽는 내용", npcs.md:98 "항목이 읽는 내용", bags-and-bank.md:56(표 머리) "오른쪽 클릭이 읽는 내용"
- 본문(대표 위치): loot-trade-mail.md:55, 86 / action-bars.md:51, 59, 63, 71, 141 / npcs.md:47, 100, 126, 150 / bags-and-bank.md:4, 29, 37, 70, 113, 116, 134, 149 / character.md:50, 99, 128, 163, 169 / professions.md:44, 91, 114, 165, 167, 176, 186, 187 / collections.md:57, 79, 93, 108, 126, 131, 173, 175, 192 / spells-and-talents.md:36, 52, 59, 67, 82, 111, 137, 165, 170, 172, 197
- 방침 제안(사용자 결정 필요, 대상이 많다): 제목은 interface.md의 "들리는 내용"에 맞춰 "칸에서 들리는 내용"으로 통일. 본문은 "각 칸은 ~을 읽습니다" → "칸마다 ~을 읽습니다"(주어를 WowVision으로 되돌리는 최소 수정) 또는 "각 칸에서는 ~이 들립니다". system.md는 이미 "~로 읽힙니다"로 써서 이 문제가 없다.
- 대표: loot-trade-mail.md:86 | e1 | 중간 | 각 편지는 보낸 사람과 제목을 읽습니다. | Each letter reads who it is from and the subject: | 편지마다 보낸 사람과 제목을 읽습니다. | 편지가 읽는 것이 아니다
- 대표: npcs.md:45 | e1 | 높음 | ### 아이템이 읽는 내용 | ### What an item says | ### 아이템에서 들리는 내용 | 아이템이 무언가를 읽는다는 뜻으로 들린다
- 대표: bags-and-bank.md:56 | e1 | 높음 | 가방 아이템에서 오른쪽 클릭이 읽는 내용 | What right-click on a bag item reads | 가방 아이템의 오른쪽 클릭 항목 이름 | "클릭이 읽는다"는 뜻이 통하지 않는다(상황별 메뉴의 항목 이름을 말한다)

##### 6. fills the details / the list fills → 채우다 [b]

- 위치: professions.md:50(세부 정보가 채워집니다), collections.md:131(세부 정보를 채우고), spells-and-talents.md:84(추천어 목록이 채워집니다)
- 방침 제안: fill → "표시하다/표시되다".
- 대표: collections.md:131 | b | 중간 | Enter로 세트를 선택해 세부 정보를 채우고, Backspace로 즐겨찾기 메뉴를 엽니다. | Enter selects a set and fills the details, Backspace opens the favorite menu. | Enter로 세트를 선택하면 세부 정보에 그 세트가 표시되고, Backspace로 즐겨찾기 메뉴를 엽니다. | "세부 정보를 채운다"는 사용자가 무언가를 입력한다는 뜻으로 들린다

##### 7. change tier / change row → 변경하다 [e3, 새 부류]

낱말 표의 "바꾸다 → 변경하다"를 기계적으로 적용해, 뜻이 "다른 줄로 이동"인 곳이 "줄을 수정한다"로 들린다. 가이드는 "변경하다는 원문이 change일 때만"이라고 했지만, 이 change는 뜻이 이동이다.

- 위치: spells-and-talents.md:137(단계를 변경하고 … 선택지를 변경합니다), 170(줄을 변경하고), npcs.md:40(탭을 변경합니다, 원문 Enter to switch), character.md:32(탭을 변경하려면, 원문 To switch tabs)
- 방침 제안: 초점이 다른 줄·단계로 옮겨 가는 change는 "이동하다", 탭은 "전환하다".
- 대표: spells-and-talents.md:137 | e3 | 높음 | Up과 Down으로 단계를 변경하고, Left와 Right로 선택지를 변경합니다. | Up and Down change tier, Left and Right the choice. | Up과 Down으로 단계 사이를 이동하고, Left와 Right로 선택지 사이를 이동합니다. | "선택지를 변경한다"는 특성을 바꿔 찍는다는 뜻으로 들린다. 실제로는 초점만 움직인다
- 대표: character.md:32 | e3 | 높음 | 탭을 변경하려면 탭 정지점으로 가서 … | To switch tabs, go to the Tabs stop, … | 탭을 전환하려면 탭 정지점으로 가서 … | 가이드: switch는 전환하다

#### 개별 사례

##### loot-trade-mail.md
- loot-trade-mail.md:134 | d | 높음 | Tab은 상자를 떠나 다음 정지점으로 가고, Shift+Tab은 뒤로 갑니다. | Tab leaves the box and moves on to the next stop, Shift+Tab goes back. | Tab은 상자에서 나와 다음 정지점으로 이동하고, Shift+Tab은 이전 정지점으로 이동합니다. | "뒤로 간다"가 어디인지 불분명(사용자 지적 4와 같은 부류)
- loot-trade-mail.md:142 | c | 중간 | 가방에서 리넨 옷감에 대고 Backspace를 누릅니다(…). Ctrl+Tab으로 돌아옵니다. | In your bags, press Backspace on the Linen Cloth (…). Return with Ctrl+Tab. | 가방의 리넨 옷감에서 Backspace를 누릅니다(…). Ctrl+Tab으로 우편 창에 돌아옵니다. | "대고"는 다른 곳의 "~에서 누릅니다"와 다르고, 어디로 돌아오는지 빠졌다
- loot-trade-mail.md:77 | d | 중간 | Left와 Right로 둘 사이를 오가고, Enter로 전환합니다. | Left and Right move between them, and Enter switches. | Left와 Right로 두 탭 사이를 이동하고, Enter로 그 탭으로 전환합니다. | 오가다 + 무엇을 전환하는지 빠짐

##### action-bars.md
- action-bars.md:15 | b | 높음 | WowVision은 전투 중에 사용자의 게임 단축키가 계속 작동하도록 자기 키를 게임에 돌려주고, 전투가 끝나면 다시 가져옵니다. | WowVision gives its keys back to the game during combat so that your own key bindings keep working, and takes them again when combat ends. | WowVision은 전투 중에 사용자의 게임 단축키가 계속 작동하도록 창 이동 키를 가로채지 않고, 전투가 끝나면 다시 처리합니다. | take keys 계열(사용자 지적 2). "키를 돌려주다/가져오다" 단순 치환이 안 되는 문맥. 방침은 부모 결정에 따름. 같은 표현: action-bars.md:156(자기 키를 게임에 돌려줍니다)
- action-bars.md:91 | b | 중간 | WoW는 커서를 씁니다. 무언가를 집어 든 다음 다른 곳에 내려놓습니다. WowVision은 같은 일을 키로 합니다. | WoW uses a cursor: you pick something up, and then you put it down somewhere. WowVision does the same with keys. | WoW에서는 커서로 물건을 옮깁니다. 무언가를 집어 든 다음 다른 곳에 내려놓습니다. WowVision에서는 같은 일을 키로 합니다. | "커서를 씁니다"만으로는 무슨 말인지 안 잡힌다. bags-and-bank.md:78은 "WoW는 커서로 물건을 옮깁니다"로 잘 옮겼다
- action-bars.md:59 | d | 중간 | 게임이 버튼을 꺼 둔 칸은 이름 뒤에 "사용 불가"라고 말합니다. | A slot whose button the game has switched off says "Disabled" after its name. | 게임이 버튼을 비활성화한 칸은 이름 뒤에 "사용 불가"라고 말합니다. | 버튼을 "꺼 둔다"보다 비활성화가 관례. system.md:51은 "비활성화"를 쓴다
- action-bars.md:141 | d | 낮음 | 이어서 그 칸을 발동하는 컨트롤러 버튼을 말합니다. | followed by the controller button that triggers it | 이어서 그 칸을 실행하는 컨트롤러 버튼을 말합니다. | "발동"은 효과에 쓰는 말

##### npcs.md
- npcs.md:4 | c | 높음 | 각 창은 게임이 그 창을 열 때 열립니다. | All of them open when the game opens them. | 이 창들은 모두 게임이 열 때 함께 열립니다. | 동어 반복으로 들려 뜻이 빈다. 원문 뜻은 "WowVision 쪽에서 따로 여는 것이 아니라 게임을 따라 열린다"
- npcs.md:82 | b | 중간 | 두 설정 모두 상인에게 들러 무엇을 팔고 수리했는지 들은 뒤 다시 길을 떠나는 흔한 흐름을 위한 것입니다. | Both are meant for the common run: arrive at a vendor, hear what you sold and repaired, and move on. | 두 설정 모두 상인에게 들러 무엇을 팔고 수리했는지 듣고 바로 떠나는 흔한 경우를 위한 것입니다. | "흐름"은 낱말 지침 3번이 피하라는 은유
- npcs.md:93 | c | 중간 | 새 캐릭터는 항목을 하나만 듣고 나중에 배울 것은 하나도 듣지 못합니다. | so a new character hears only one entry and nothing of what comes later | 새 캐릭터로는 항목 하나만 들리고 나중에 배울 것은 하나도 들리지 않습니다. | 듣는 것은 캐릭터가 아니라 사용자
- npcs.md:106 | b | 중간 | 목록의 머리글(사용 가능처럼 게임이 쓰는 묶음)에는 "펼쳐짐"이나 "접힘"이 붙으며 | Headers in the list (the groups the game uses, such as Available) say Expanded or Collapsed | 목록의 머리글(사용 가능처럼 게임이 구분해 둔 묶음)에는 "펼쳐짐"이나 "접힘"이 붙으며 | "게임이 쓰는 묶음"은 뜻이 안 잡힌다
- npcs.md:114 | b | 중간 | 게임이 주문을 가르쳐 주고, 돈이 줄어듭니다. | The game teaches you the spell, and your money goes down. | 주문을 배우고, 그만큼 돈이 줄어듭니다. | "게임이 가르쳐 준다"는 직역
- npcs.md:53 | c | 낮음 | 이 레이블은 실시간으로 변경됩니다. | These labels are live. | 이 내용은 실시간으로 업데이트됩니다. | "레이블"은 이 문서의 다른 곳에 없는 말(다른 곳은 이름·내용). bags-and-bank.md:37은 "칸 이름은 실시간으로 변경됩니다"

##### character.md
- character.md:20 | a,c | 중간 | 게임 자체의 창은 WowVision이 대신 닫습니다. | WowVision closes the game's own panel for you. | 게임의 캐릭터 창도 WowVision이 함께 닫습니다. | "게임 자체의 창"이 무엇인지, "대신"이 누구 대신인지 안 잡힌다
- character.md:22 | b | 중간 | 두 애드온이 같은 키를 두고 부딪치지 않도록 WowVision은 이 창을 읽지 않습니다. | to avoid two addons fighting over the same keys | 두 애드온이 같은 키를 두고 충돌하지 않도록 WowVision은 이 창을 읽지 않습니다. | 소프트웨어 관례는 "충돌"
- character.md:32 | b | 중간 | 그 아래 본문이 다시 만들어지고, Tab을 누르면 본문으로 들어갑니다. | The body below it is rebuilt and Tab takes you into it. | 그 아래 본문이 새 탭의 내용으로 변경되고, Tab을 누르면 본문으로 이동합니다. | rebuild 직역. 같은 표현: spells-and-talents.md:41(목록이 다시 만들어지므로)
- character.md:60 | d | 중간 | 능력치는 "힘 142"나 "방어도 1500"처럼 읽기만 하는 줄입니다. | The stats are read-only lines | 능력치는 "힘 142"나 "방어도 1500" 같은 읽기 전용 줄입니다. | read-only의 관례 번역
- character.md:84 | b,c | 중간 | 창이 열리면 커서가 이름 상자에 있지만 입력 상태는 풀려 있으므로 바로 화살표 키를 쓸 수 있습니다. | The window opens with the cursor in the name box cleared, so you can use the arrow keys at once | 창이 열리면 WowVision이 이름 상자의 입력 상태를 해제해 두므로 바로 화살표 키로 이동할 수 있습니다. | "입력 상태는 풀려 있다"가 귀로 안 잡힌다
- character.md:6 / spells-and-talents.md:6 | e2 | 높음 | "## 쓸 수 있는 곳" / "## 사용할 수 있는 곳" | 둘 다 ## Where it is available | 둘 다 "## 사용할 수 있는 곳"(또는 professions.md:6·collections.md:6처럼 "지원 범위") | 같은 원문 제목이 파일마다 다르다

##### professions.md
- professions.md:32 | b | 중간 | 화면은 이어진 정지점으로 읽힙니다: | the screen reads as a chain of stops: | 화면은 다음 순서의 정지점으로 읽힙니다: | "이어진 정지점"이 무슨 뜻인지 안 잡힌다. 다른 파일은 "정지점은 다음 순서입니다"
- professions.md:59 | b | 중간 | 게임이 붙인 재료 문구("재료:")를 이름으로 쓰는 묶음입니다. | A group named after the game's reagent label ("Reagents:") | 게임의 재료 문구("재료:")가 이름인 묶음입니다. | "문구를 이름으로 쓰는 묶음"은 한 번 듣고 안 풀린다
- professions.md:129, 144 | e2 | 중간 | 129 "줄일 능력치 하나와 얻을 능력치 하나", 144 "포기할 능력치를 고르고" | 129 one stat to reduce, 144 the stat you give up | 144도 "줄일 능력치를 고르고" | 같은 대상을 한 절 안에서 두 말로 부른다(원문도 갈려 있으나 한국어는 맞추는 편이 낫다. 원문 충실 우선이면 유지)
- professions.md:178 | c | 중간 | 입력하면 제조법이 좁혀집니다. | Type to narrow the recipes. | 입력하면 제조법 목록이 좁혀집니다. | 36번 줄은 "제조법 목록이 좁혀집니다". "제조법이 좁혀진다"는 뜻이 빈다

##### bags-and-bank.md
- bags-and-bank.md:37 | b | 높음 | 아이템을 집으면 지금 서 있는 칸이 곧바로 "비어 있음"이라고 읽습니다. | the slot you are standing on says "Empty" at once | 아이템을 집으면 초점이 있는 칸을 곧바로 "비어 있음"이라고 읽습니다. | 칸 위에 "서 있다"는 은유. 게임에서 "서 있는 곳"은 캐릭터 위치로 들린다
- bags-and-bank.md:10 | b | 중간 | 가방 창은 배경 창입니다. | The bags window is a background window. | 가방 창은 초점을 가져오지 않고 뒤에서 열리는 창입니다. → 최소 수정: 유지하되 다음 문장으로 뜻이 풀리므로 낮은 우선순위 | "배경 창"은 설명 없이 나오는 말(문제 해결 180줄에서도 반복). 원문에 없는 설명을 덧붙이지 않는 규칙 때문에 보고 목록 후보
- bags-and-bank.md:109 | b | 중간 | 아이템은 손으로 정리하거나 | Arrange items by hand | 아이템은 직접 정리하거나 | by hand 직역
- bags-and-bank.md:132 | c | 낮음 | 나가려면 Tab으로 빠져나옵니다. | Tab out to leave it. | 검색 칸에서 나가려면 Tab을 누릅니다. | "나가려면 … 빠져나옵니다" 동어 반복
- bags-and-bank.md:134 | b | 중간 | 아래 개별 보기에서처럼 각각 자기 탭 정지점을 가지며, 가방 보관함이 첫 항목입니다. | Each gets a stop of its own, with its bag slot first | 아래 개별 보기에서처럼 각각 별도의 탭 정지점이며, 가방 보관함이 첫 항목입니다. | "자기 ~을 가지며"는 have 직역. 같은 파일 101줄은 "각각 별도의 탭 정지점이며"
- bags-and-bank.md:156 | b,c | 중간 | 은행원이 엽니다. | A banker opens it. | 은행원에게 말을 걸면 열립니다. | 은행원이 창을 여는 것처럼 들린다. 113줄은 "은행원에게 가서 은행을 엽니다"
- bags-and-bank.md 전체(10, 26, 35, 82, 94, 176) | e2 | 높음 | "~을 보십시오" | See [...] | "~을 참고하십시오" | 이 파일만 "보십시오"이고 나머지 8개 파일은 "참고하십시오"다. spells-and-talents.md:63의 "살펴보십시오"는 다른 뜻이라 해당 없음

##### system.md
- system.md:13 | b,d | 중간 | Enter를 누르면 지금 있는 버튼을 사용합니다. | Press Enter to use the one you are on. | Enter를 누르면 초점이 있는 버튼을 누릅니다. | "버튼을 사용한다"보다 "누른다"가 관례(같은 파일 47줄 "버튼이 눌립니다")
- system.md:22 | b | 중간 | WowVision 읽기 기능은 이 창의 거의 전부를 다룹니다. | The WowVision reader covers almost all of it | WowVision은 이 창의 거의 모든 부분을 읽습니다. | "읽기 기능이 다룬다"는 직역
- system.md:24 | c | 중간 | 로그인되어 있어도 로그인으로 읽힐 수 있고, 게임이 이 줄의 동작을 거부합니다. | they may read Sign In even when you are signed in, and the game refuses them | 로그인되어 있어도 버튼이 "로그인"으로 읽힐 수 있고, 이 줄에서 Enter를 눌러도 게임이 받아들이지 않습니다. | "로그인으로 읽힌다"가 버튼 이름이라는 것이 안 잡힌다
- system.md:51, 53, 61 | e2 | 높음 | 조작 요소 | control | 컨트롤 | basics/interface.md는 control을 "컨트롤"로 쓴다. 이 파일만 "조작 요소"다
- system.md:62 | c | 중간 | 이런 줄은 알려 주십시오. | Please report these. | 이런 줄을 발견하면 개발자에게 알려 주십시오. | 누구에게 무엇을 하라는 것인지 빠졌다("신고해 주십시오"도 가능)
- system.md:80 | b | 높음 | 설정 목록에 닿을 때까지 Tab을 누르고 아래로 읽어 자동 전리품 획득까지 가십시오. | Press Tab until the settings list and read down to Auto Loot. | 설정 목록이 나올 때까지 Tab을 누르고 Down으로 자동 전리품 획득까지 이동하십시오. | "닿다", "아래로 읽어"는 직역. 같은 표현: system.md:125(그 버튼에 닿습니다)
- system.md:105 | b | 낮음 | 이 창은 두 가지 방식으로 읽힙니다. | The window reads in two modes. | 이 창에는 두 가지 상태가 있습니다. | 뒤에 나오는 것은 "기본 창"과 "이름 상자"라는 두 화면이지 읽는 방식이 아니다
- system.md:160 | c | 높음 | 변경하려면 WowVision 메뉴에서 목표 선택, 하드 대상을 차례로 열고 거리 변경을 고르십시오. | To change it, open Targeting, then Hard Target, … | 거리 안내 설정을 변경하려면 WowVision 메뉴에서 … | 목적어가 없다. 바로 뒤에 "거리 변경"이라는 설정 이름이 나와 더 헷갈린다

##### collections.md
- collections.md:114 | a | 중간 | 이것은 형상변환사가 아니라 형상 도감입니다. | This is the wardrobe journal, not the transmogrifier. | 이 탭은 형상변환사 창이 아니라 형상 도감입니다. | 절 첫 문장의 "이것"이 가리키는 대상이 없다
- collections.md:46 | c | 중간 | 게임의 수집한 것만 표시 필터를 켜 두면 비어 있는 수집품의 탭이 빠질 수 있습니다. | Tabs for empty collections may be missing while the game's Only show collected filter is on. | 게임의 수집한 것만 표시 필터를 켜 두면 수집한 것이 없는 종류의 탭은 나오지 않을 수 있습니다. | "비어 있는 수집품의 탭이 빠진다"가 한 번에 안 잡힌다
- collections.md:126 | a | 중간 | 도감에서 그냥 Enter를 누르면 아무 일도 일어나지 않습니다. | A plain Enter does nothing in the journal | 형상에서 Enter만 누르면 아무 일도 일어나지 않습니다. | "도감에서"는 범위가 넓어 다른 탭의 Enter 동작(행 선택, 장난감 사용)과 어긋나게 들린다. 단 원문도 in the journal이라 원문 충실 우선이면 유지
- collections.md:160 | b | 중간 | "획득"은 영예가 도달한 레벨에 붙습니다. | "Earned" appears for levels your renown has reached. | "획득"은 내 영예 레벨이 이미 도달한 레벨에 붙습니다. | "영예가 도달한 레벨"은 주어가 이상하다
- collections.md:178 | e2 | 높음 | "체크됨" 또는 "체크되지 않음"으로 읽히는 체크박스입니다. | a checkbox | … 체크 상자입니다. | 가이드와 다른 모든 파일은 "체크 상자"
- collections.md:189 | b | 낮음 | 포인트 사용 조건에 막힌 줄에는 게임의 조건 글자(N 포인트 더 소모)가 붙습니다. | a row held back by a spend gate adds the game's gate text | 포인트를 더 써야 열리는 줄에는 … | "조건에 막힌 줄"보다 spells-and-talents.md:170의 풀이가 낫다

##### spells-and-talents.md
- spells-and-talents.md:89 | b,c | 중간 | 둘 사이에는 탭이 없습니다. | there are no tabs between the two | 두 창을 전환하는 탭은 없습니다. | "둘 사이에 탭이 없다"는 위치를 말하는 것처럼 들린다
- spells-and-talents.md:175 | c | 중간 | "거인의 강타, 등급 0/1, 잠김, 필사의 일격 필요": 이 특성에 필요한 선행 특성입니다. | …: the talent it waits for. | …: "필요" 앞의 이름이 먼저 배워야 하는 특성입니다. | 무엇이 선행 특성인지 가리키는 말이 없다
- spells-and-talents.md:182 | b | 낮음 | Space는 툴팁 전체(설명, 다음 등급, 비용, 막고 있는 것)를 읽습니다. | what blocks it | … 배울 수 없는 이유)를 읽습니다. | "막고 있는 것"은 직역
- spells-and-talents.md:162 | d | 낮음 | 지금 쓰는 전문화가 아니면 활성화 버튼이, 쓰는 전문화이면 "활성"이라는 줄이 나옵니다. | when it is not the specialization you are using | 지금 사용 중인 전문화가 아니면 활성화 버튼이, 사용 중인 전문화이면 … | 쓰다 → 사용하다(문장 구조가 얽혀 단순 치환과 다름)
- spells-and-talents.md:199 | e2 | 낮음 | ### 예: WoW: Forever에서 특성을 찍고 적용하기 | take a talent | 특성을 배우고 적용하기 | "찍다"는 이 문서에서 여기 한 번뿐인 게이머 속어. 본문은 "배우다"

#### 로케일 값 문제

- collections.md:192, spells-and-talents.md:100, 179 | 로케일 값 문제 | 높음 | "일치하는 항목 검색" | "Search Match" (koKR `windows.lua:168` `L["Search Match"] = "일치하는 항목 검색"`) | "검색 일치" 또는 "검색 결과와 일치" | 지금 값은 "일치하는 항목을 검색하라"는 명령으로 들린다. 실제 뜻은 "이 특성이 검색어와 일치함"이라는 상태 표시다. 설명서만 고칠 수 없고 koKR 값을 고쳐야 한다. 게임 공식 문자열에 같은 표시가 있는지(`cache/gs_enUS.csv`에서 "Search Match")는 미확인
- 따옴표 인용 중 "가방 보관함"(`Bag Slot`), "매크로를 끌어서 집기", "필터링됨", "사용함"은 koKR 값과 일치하며 문제 없음

#### 손대지 않은 것(과잉 수정 경계)

- "포인트를 쓰다"(spend points: spells-and-talents.md:4, 11, 114, 116, 165, 184, collections.md:186, 204)는 낱말 표의 "쓰다(기능·키를 쓰다)"와 다른 뜻(소비)이다. "사용하다"로 일괄 치환하면 안 된다. 부모가 grep으로 집계할 때 제외 필요
- "Sku에 맡깁니다"(leaves to Sku), "초점이 여기에 놓입니다", "~에서 시작합니다", "글이 도착하면 읽습니다"(서버에서 오는 글이라 문자 그대로), npcs.md:131 "지금 서 있는 곳"(캐릭터 위치)은 뜻이 통해 유지
- "아래 화살표로"(character.md:92, 118, professions.md:76)는 원문이 arrow down이라 Down 키 표기와 다르지만 뜻은 통함
- "사용함 스위치"와 "사용함 토글"이 파일마다 섞여 있다(스위치: loot-trade-mail, action-bars, npcs, professions, bags, system / 토글: character, collections, spells). 원문이 switch/toggle로 갈려 있는지는 확인하지 않았다(미확인)

---

### 감수 결과: information/ + reference/

범위: ko/information (index, group-health, monitors, buffers), ko/reference (index, glossary, keybindings, commands, versions). 9개 파일 전부 en과 줄 단위로 대조해 끝까지 읽었다.
경로는 `docs/src/user/ko/` 기준이고 줄 번호는 ko 파일의 실제 줄이다.
형식: `파일:줄 | 부류 | 확신도 | 현재 | 원문 | 수정안 | 이유`

부류: (a) 지시어 (b) 관용구·은유 직역 (c) 목적어·주어 생략 (d) 동사·낱말 선택 (e1) 조사 오류 (e2) 따옴표 없는 설정·상태 이름이 문장에 녹아 경계가 안 들림 (e3) 파일 사이 용어 불일치

#### 1. 개별 사례

##### (a) 지시어

1. information/monitors.md:309 | a | 중간 | 모든 규칙에는 주문 설정이 있습니다. 거기서 Enter를 누르면 작은 화면이 열립니다. | Every rule has a Spell setting. Press Enter on it to open a small screen | 주문 설정에서 Enter를 누르면 작은 화면이 열립니다. | "거기서"가 장소처럼 들린다. 가리키는 것은 설정 항목이다.
2. information/buffers.md:260 | a | 높음 | 표시 이름을 원하는 이름으로 변경합니다(그 위에서 Enter를 누르고, 입력한 뒤, 다시 Enter). | Change Label to a name you like (press Enter on it, type, Enter again) | (표시 이름에서 Enter를 누르고, 입력한 뒤, 다시 Enter) | on it 직역. "그 위"는 화면 위치로 들린다. 같은 꼴: buffers.md:304 "그 위에서 Shift+F10을 눌러" → "그 설정에서 Shift+F10을 눌러".
3. information/buffers.md:294 | a | 중간 | 꺼 둔 그룹이나 버퍼는 설정을 유지하지만, Alt+Left, Alt+Right, Alt+Ctrl+Left, Alt+Ctrl+Right가 그것을 건너뜁니다. | ...skip over it | 꺼 둔 그룹이나 버퍼는 설정을 유지하지만, Alt+Left, Alt+Right, Alt+Ctrl+Left, Alt+Ctrl+Right로 이동할 때는 건너뜁니다. | 키 이름 네 개를 듣고 난 뒤의 "그것"은 대상이 멀다. 주제어가 이미 문장 앞에 있으므로 지시어를 뺀다.
4. reference/commands.md:92 | a | 중간 | 직선 비컨을 설정하거나, ... 현재 위치를 알려 줍니다. 그러면 걸어가는 동안 비컨이 소리를 내고 말합니다. | The beacon then plays its sound and speaks as you walk. | 비컨을 설정하면 걸어가는 동안 비컨이 소리를 내고 말합니다. | 앞 문장이 세 가지 동작을 나열해서 "그러면"이 어느 것을 받는지 불분명하다(위치 읽기에는 해당하지 않는다).

##### (b) 관용구·은유 직역

5. information/monitors.md:10 | b | 높음 | 규칙 하나는 한 가지, 보통 주문 하나를 지켜보며 효과 적용, 확산, 만료 임박, 없음 같은 상태를 오갑니다. | A rule watches one thing, usually one spell, and moves through states such as Applied, Pandemic, Expiring and Missing. | 규칙 하나는 대상 한 가지(보통 주문 하나)를 감시하며, 규칙의 상태는 효과 적용, 확산, 만료 임박, 없음 등으로 변경됩니다. | "상태를 오가다"는 왕복처럼 들린다. 상태 이름 네 개가 따옴표 없이 이어져 "없음 같은 상태"도 걸린다(e2).
6. information/monitors.md:22 | b | 높음 | 규칙이 시작된 뒤 처음 보는 상태는 조용히 정해집니다. | The first state a rule sees after it starts is established silently | 규칙이 시작된 뒤 처음 확인한 상태는 알리지 않고 기준 상태로만 저장합니다. | "조용히 정해진다"로는 무슨 일이 일어나는지 알 수 없다. 같은 꼴: monitors.md:174 "규칙이 처음 보는 상태(예: 로그인할 때)는 조용히 지나갑니다" → "규칙이 처음 확인한 상태(예: 로그인할 때)는 알리지 않습니다".
7. information/monitors.md:27 | b | 중간 | 변경한 뒤에 모든 규칙이 말하지 않고 현재 상태만 받아들입니다. | every rule just takes in the current state without speaking | 변경한 뒤에 모든 규칙이 알리지 않고 현재 상태만 확인합니다. | take in 직역.
8. information/monitors.md:119 | b | 높음 | 주문 하나가 유닛에 걸려 있는 동안 그 흐름을 따라갑니다. | It follows one spell through its life on the unit. | 주문 하나가 유닛에 걸린 뒤 사라질 때까지 상태 변화를 추적합니다. | "그 흐름"은 가리키는 것이 없고, "흐름"은 사용자 표(fluent-korean 3번)가 피하라는 비유다.
9. information/monitors.md:6 | b | 중간 | 고를 주문 목록을 만들 때만 재사용 대기시간 관리자를 빌려 씁니다. | only borrows the cooldown manager for its list of spells to pick from | 고를 주문 목록을 만들 때만 재사용 대기시간 관리자를 이용합니다. | borrow 직역.
10. information/monitors.md:145 | b | 중간 | 모니터가 유닛에서 그 오라를 한 번 보면 빠른 선택에 나옵니다. | once your monitor has seen it on the unit | 모니터가 유닛에서 그 오라를 한 번 감지하면 빠른 선택에 나옵니다. | 같은 파일 206줄은 이미 "감지하는"을 쓴다. 같은 꼴: monitors.md:230 "각 규칙이 ... 프레임에서 본 것", reference/commands.md:215, 219 "규칙이 본 내용" → "감지한 내용".
11. information/monitors.md:185 | b | 중간 | 재사용 대기시간 관리자가 따라가는 두 유닛입니다. | the two the cooldown manager follows | 재사용 대기시간 관리자가 추적하는 두 유닛입니다. | follow=추적. 같은 꼴: monitors.md:264 "게임이 그 주문 둘레에 그리는 빛을 따라갑니다" → "빛을 감시합니다".
12. information/group-health.md:98 | b | 중간 | 모니터는 생명력이 변하는 즉시 그 변화를 따라가지 않으며 | does not follow health changes as they happen | 모니터는 생명력 변화를 실시간으로 알려 주지 않으며 | follow 직역.
13. information/buffers.md:155 | b | 중간 | 버퍼는 가장 최신 줄에서 열리고, 대화 기록처럼 새 줄이 들어오면 따라갑니다. | It opens on the newest line and follows new lines as they arrive | 버퍼는 가장 최신 줄에서 열리고, 대화 기록처럼 새 줄이 들어오면 현재 위치가 그 줄로 이동합니다. | "따라갑니다"의 주어와 대상이 모두 빠졌다.
14. information/buffers.md:302 | b | 중간 | 그룹 안의 버퍼와 항목은 그룹을 따라가며 자체 범위 선택이 없습니다. | travel with it | 그룹 안의 버퍼와 항목은 그룹과 같은 범위에 저장되며 자체 범위 선택이 없습니다. | travel with 직역.
15. information/buffers.md:185 | b | 중간 | 연계 점수를 쌓기 시작할 때처럼 나중에 나타나는 자원도 잡아냅니다. | picks up a resource that appears later | ...나중에 나타나는 자원도 목록에 추가합니다. | pick up 직역.
16. information/buffers.md:301 | b | 중간 | 그래서 변경한 버퍼는 계정의 버퍼 옆에 따로 놓입니다. | so a changed buffer sits beside the account's | 그래서 캐릭터에서 변경한 버퍼는 계정의 버퍼와 합쳐지지 않고 따로 남습니다. | sit beside 직역. 목록에서의 위치 이야기가 아니라 병합되지 않는다는 뜻이다.
17. information/buffers.md:141, 143 | b | 중간 | 보고 있던 오라가 사라지면 "사라짐"이라고 읽습니다. / 오라에 있는 동안 툴팁 키로 그 오라를 한 줄씩 읽을 수 있습니다. | An aura that vanishes while you are on it / While you are on an aura | 현재 항목인 오라가 사라지면 "사라짐"이라고 읽습니다. / 현재 항목이 오라일 때는 툴팁 키로 그 오라를 한 줄씩 읽을 수 있습니다. | be on 직역. 이 파일 18줄이 "현재 항목"이라는 말을 이미 정의했다.
18. information/buffers.md:118, 119 | b | 중간 | 오라가 남은 시간을 말할지 여부 / 오라가 하는 일을 말할지 여부 | Whether an aura says how much time it has left / what it does | 오라의 남은 시간을 읽을지 여부 / 오라의 설명을 읽을지 여부 | "오라가 말한다"는 의인화다. 설정 이름도 "남은 시간 읽기", "설명 읽기"다.
19. reference/keybindings.md:97 | b | 중간 | 지금 비컨이 이끄는 경유지에서 이어 갑니다 | going on at the waypoint the beacon leads to now | 비컨이 지금 안내하고 있는 경유지부터 계속합니다 | lead/go on 직역.
20. reference/versions.md:61 | b | 중간 | 스캐너는 여전히 항목이 있는 방향을 곧바로 가리킬 수 있습니다. | the scanner can still point you straight at entries | 스캐너는 지도 데이터가 없어도 항목까지 직선으로 안내할 수 있습니다. | point straight at 직역. 실제 동작은 직선 비컨 안내다(world/scanner.md 표현과 맞출 것).
21. reference/commands.md:232 | b | 중간 | WowVision은 이 설정을 창으로 읽습니다 | which WowVision reads as a window | WowVision은 이 설정 화면을 다른 창과 같은 방식으로 읽습니다 | "창으로 읽다"는 뜻이 안 잡힌다.
22. 키를 가져가다·돌려주다 계열(부모 집계용, 문맥별 수정안):
    - reference/glossary.md:84 | 높음 | WowVision은 WowVision 창이 열려 있는 동안에만 화살표 키를 가져가고, 전투 중에는 게임에 돌려줍니다. | only takes the arrow keys ... gives them back in combat | 화살표 키는 WowVision 창이 열려 있는 동안에만 WowVision 창에서 작동하고, 전투 중에는 다시 게임에서 작동합니다.
    - reference/keybindings.md:13 | 높음 | 전투 중에는 WowVision이 창 키를 게임에 돌려줍니다 | hands the window keys back | 전투 중에는 창 키가 다시 게임에서 작동합니다
    - reference/commands.md:207 | 중간 | 각 창이 탐색 키를 넘겨받는 시점, 넘겨받기를 기다리는 시점, 돌려주는 시점 | when windows take, wait for and release the navigation keys | 각 창이 이동 키를 사용하기 시작한 시점, 사용하려고 기다리는 시점, 게임에 반환한 시점
    - 본보기로 삼을 기존 문장: reference/glossary.md:68 "창이 열려 있지 않을 때와 전투 중에는 이 키들이 다시 게임에서 작동합니다", reference/keybindings.md:10 "게임 창에서는 Escape를 게임이 그대로 처리해". 이 두 문장은 같은 원문 부류(go back to the game, stays with the game)를 은유 없이 옮겼다.

##### (c) 목적어·주어 생략

23. information/monitors.md:260 | c | 높음 | 전역 재사용 대기는 치지 않습니다. | The global cooldown never counts. | 전역 재사용 대기는 재사용 대기에 포함하지 않습니다. | 보어 없이 "치지 않습니다"만 들리면 "때리지 않는다"로 들린다.
24. information/monitors.md:64 | c | 중간 | 모든 모니터를 한꺼번에 전환하려면 | To switch every monitor at once | 모든 모니터의 범위를 한꺼번에 변경하려면 | 무엇을 전환하는지(저장 범위)가 빠졌다. buffers.md:303은 같은 원문을 "한 번에 모두 변경하려면"으로 옮겼다.
25. information/monitors.md:331 | c | 중간 | 규칙이 효과 적용에서 없음으로 변경되었기 때문입니다. | because the rule changed from Applied to Missing | 규칙의 상태가 효과 적용에서 없음으로 변경되었기 때문입니다. | 변경된 것은 규칙이 아니라 규칙의 상태다. 같은 문단의 "효과 적용이 딸깍 소리를 냅니다" → "효과 적용 상태의 딸깍 소리가 납니다"(e2).
26. information/group-health.md:62 | c | 중간 | 모든 구성원을 번호 순서대로 현재 음 높이로 한 번씩 말합니다. | says everyone once, in number order, at their current pitch | 모든 구성원의 번호를 번호 순서대로, 각자의 현재 음 높이로 한 번씩 말합니다. | "구성원을 말하다"는 뜻이 빈다. 같은 꼴: reference/keybindings.md:159.
27. reference/glossary.md:40 | c | 중간 | 대상에게서 약화 효과가 사라지는 경우가 그 예입니다. 규칙으로 이루어집니다. | Made of rules. | 모니터는 규칙으로 이루어집니다. | 앞 문장의 주어가 "경우"라서 주어 없는 문장이 떠 버린다.
28. information/buffers.md:203 | c | 중간 | 비워 둔 채 확인하면 항목이 표준 문구로 돌아갑니다. | Leaving it empty and confirming | 입력란을 비워 둔 채 Enter를 누르면 항목이 표준 문구로 돌아갑니다. | 무엇을 확인하는지 없다. 바로 앞 문장이 "Enter를 누르십시오"다.
29. reference/keybindings.md:189 | c | 중간 | Tab은 다음으로 넘어가고, Escape는 WowVision 입력창을 취소합니다 | Tab moves on; Escape cancels a WowVision box | Tab은 다음 요소로 넘어가고, Escape는 WowVision 입력창의 입력을 취소합니다 | "다음"이 무엇인지, 무엇을 취소하는지 빠졌다. 같은 줄 앞부분 "입력을 확정합니다"는 목적어가 있어 괜찮다.
30. reference/keybindings.md:42 | c | 중간 | 커서에 있는 것을 비우거나 파괴합니다(실제 아이템이면 먼저 묻습니다). | Clears or destroys what is on the cursor (asks first for a real item) | 커서를 비우거나 커서에 든 아이템을 파괴합니다(실제 아이템이면 먼저 확인을 요청합니다). | "있는 것을 비우다"는 호응이 안 맞고, "묻습니다"는 무엇을 묻는지 없다. interface.md 234줄은 "게임이 확인을 요청한 뒤에야"라고 쓴다.
31. information/buffers.md:388 | c | 중간 | 키가 아무 반응도 하지 않으면 | If the keys do nothing | 키를 눌러도 아무 반응이 없으면 | 키가 반응한다는 주술 관계가 어색하다.
32. information/monitors.md:88 | c | 중간 | 무언가가 재생될지는 안에 있는 소리 알림이나 TTS 알림의 사용함 스위치만 정합니다. | only the Enabled switch of the Sound Alert or TTS Alert inside decides whether something plays | 알림이 재생될지는 그 상태 안에 있는 소리 알림이나 TTS 알림의 사용함 스위치로만 결정됩니다. | "스위치만 정합니다"가 문장 끝에서 주어인지 목적어인지 안 잡힌다. "안에 있는"도 무엇의 안인지 없다.

##### (d) 동사·낱말 선택

33. "뒤로 가다" 4곳 | d | 높음(사용자 표: 한 단계 뒤로 → 한 단계 이전으로)
    - information/monitors.md:55 | Escape를 누르면 한 화면 뒤로 갑니다. | Escape goes back one screen. | Escape를 누르면 이전 화면으로 돌아갑니다.
    - information/buffers.md:248 | 같은 문장 | 같은 수정안
    - information/monitors.md:328 | 뒤로 가서 없음을 열고 TTS 알림을 엽니다. | Go back and open Missing | 이전 화면으로 돌아가 없음 상태를 열고 TTS 알림을 엽니다.
    - reference/keybindings.md:31 | 한 단계 뒤로 가거나 WowVision 자체 화면과 메뉴를 닫습니다. | Goes back one level or closes | 한 단계 이전으로 돌아가거나 WowVision 자체 화면과 메뉴를 닫습니다.
34. reference/keybindings.md:148 | d | 높음 | 화면에 뜬 파티 초대를 수락합니다. | Accepts the group invitation that is shown | 화면에 표시된 파티 초대를 수락합니다. | 사용자 표의 "뜨다". commands.md:88은 같은 원문을 "표시된 파티 초대"로 옮겼다.
35. reference/versions.md:58 | d | 높음 | WowNav 경로 계획기 | WowNav route planner | WowNav 경로 계획 도구 | 사용자 표의 "-기 행위자 이름"(설치기) 규칙에 걸린다. glossary.md:70은 이미 "경로 계획 도구"다.
36. information/group-health.md:85 | d | 높음 | 공격대 파티마다 1 파티부터 8 파티까지 확인란이 하나씩 있습니다. | One checkbox per raid group | ...체크 상자가 하나씩 있습니다. | koKR ui.lua:41 Checkbox = "체크 상자". 설명서 전체에서 "확인란"은 이 한 곳뿐이다(범위 안 기준).
37. information/buffers.md:104 | d | 중간 | 항목에 사용자 설정 형식을 줄 수 없습니다. | You cannot give their items a custom format. | 항목에 사용자 설정 형식을 지정할 수 없습니다. | give 직역.
38. information/buffers.md:4 | d | 낮음 | WowVision에 들어 있는 버퍼를 그대로 써도 되고 | the buffers that come with WowVision | WowVision에 기본으로 포함된 버퍼를 그대로 사용해도 되고 | 사용자 표의 "들어가다(포함) → 포함되다". 같은 꼴: reference/versions.md:4 "처음부터 들어 있습니다".
39. information/buffers.md:88 | d | 낮음 | 늘 같은 자리에서 확인하고 싶은 것에 쓰십시오. | things you want to check in a fixed place | 늘 같은 위치에서 확인하고 싶은 정보에 사용하십시오. | "자리"는 사용자 표 3번의 비유 낱말(자리 → 곳, 위치).

#### 2. 반복 표현과 방침 제안

##### R1. count as → "치다" (5곳)
위치: information/group-health.md:92(변화로 치지만), information/monitors.md:174(재사용 대기로 치지 않습니다), information/monitors.md:260(치지 않습니다, 위 23번), reference/glossary.md:12(도착한 것으로 치고), reference/keybindings.md:99(도착한 것으로 칠지).
방침 제안: count as는 "간주하다" 또는 "포함하다"로 통일한다. "A로 치다"는 구어이고, 보어가 빠지면 "때리다"로 들린다.
수정안: 변화로 간주하지만 / 재사용 대기에 포함하지 않습니다 / 도착한 것으로 간주하고 / 도착한 것으로 간주할지.

##### R2. fire, trigger → "울리다" (10곳)
위치: information/monitors.md:20(제목 "알림이 울리는 조건"), 22(새 상태의 출력이 울립니다), 40(자기 출력이 켜져 있을 때만 울립니다), 128(상태와 울리는 때), 167, 186, 230, 365, 366, reference/glossary.md:40(알림을 울리는 기능), 44, 48.
문제: 출력에는 소리와 음성 메시지가 모두 있다. "출력이 울립니다", "TTS 알림이 울립니다"는 음성에 맞지 않는다. 같은 파일 42줄은 "자기 출력만 재생합니다"로 썼다.
방침 제안: 주어가 출력이면 "재생되다", 주어가 알림이면 "나오다"(알림이 나옵니다, 알림을 냅니다)로 통일한다. 확신도 중간. 뜻은 통하므로 우선순위는 R1보다 낮다.

##### R3. watch → "지켜보다" 19곳과 "감시하다"가 섞임
지켜보다: information/index.md:7, monitors.md:4, 10, 14, 112, 116, 123, 151, 157, 184, 185, 204, 248, 268, buffers.md:94, 186, 331, reference/glossary.md:40, 48.
감시하다: information/group-health.md 전체(koKR 설정 이름이 "파티 감시", "공격대 감시", 화면 문구가 "감시할 대상 없음"), reference/commands.md:245("실시간 감시 상태").
방침 제안: 모니터 기능의 watch는 "감시하다"로 통일한다. 근거는 koKR 값(파티 감시)이고, 설명서 규칙상 로케일 값과 같은 말을 쓴다. interface.md의 "WowVision은 그 컨트롤을 지켜봅니다"(사용자 지적 5번)도 같은 방침으로 정리된다. 추적 버퍼의 watch(buffers.md:94)는 "추적하다"가 기능 이름과 맞는다. 확신도 중간(사용자 결정 필요).

##### R4. share → "함께 쓰다" (범위 저장 문맥 6곳)
위치: information/monitors.md:61, 63, information/buffers.md:196, reference/glossary.md:6, 92.
방침 제안: 설정·재사용 대기시간을 여러 캐릭터나 아이템이 share한다는 뜻은 "공유하다"로 옮긴다. 사용자 표가 "쓰다 → 사용하다"라서 단순 치환하면 "함께 사용하다"가 되는데, 저장 범위 설명에는 "공유"가 정확하다. versions.md:14는 이미 "모든 버전이 공유하는 기능"이다. "Sku와 함께 쓰기"(use together) 계열은 "함께 사용하기"로 단순 치환이면 된다(reference/commands.md:32~35, glossary.md:56, 86, 88, keybindings.md:201, versions.md:132).

##### R5. follow → "따라가다" (7곳)
위치: information/group-health.md:98, monitors.md:119, 185, 264, buffers.md:155, 302, reference/glossary.md:36(경로가 따라가는 경유지: 이것은 문자 그대로라 유지).
방침 제안: 기능이 값을 follow하면 "추적하다", 위치가 follow하면 "이동하다", 범위가 follow하면 "같은 범위에 저장되다". 개별 수정안은 위 8, 11, 12, 13, 14번.

##### R6. 줄 번호만(단순 치환으로 충분한 것)
- 오가다: information/monitors.md:10(위 5번), reference/keybindings.md:185("목록과 새로고침 버튼 사이를 오갑니다" → "사이를 이동합니다").
- 도착: reference/glossary.md:12, 112, reference/keybindings.md:99. 모두 경유지에 실제로 도착하는 뜻이라 유지한다.
- land on 계열은 이 범위에서 이미 "첫 항목으로 갑니다"(buffers.md:35, 361), "초점을 둘 수 있는 것"(glossary.md:28), "초점이 있는 요소"(glossary.md:22, keybindings.md:37~41)로 옮겨져 있다. 다른 파일을 고칠 때 본보기로 쓸 수 있다.

#### 3. 새 부류

##### (e1) 조사 오류: "알림"에 받침 없는 말의 조사가 붙음 (설명서 전체 16곳, 확신도 높음)
"경보"를 "알림"으로 바꾼 치환(decisions.tsv 2026-11-07)에서 조사가 따라가지 않은 것으로 보인다(추정: 16곳 전부 링크 글자 "알림" 바로 뒤).
- "알림](…)를" → "을": information/group-health.md:106, information/monitors.md:53, reference/glossary.md:8, 42, basics/menu-and-settings.md:48, 107, basics/speech.md:58, 76, getting-started/quick-start.md:61, getting-started/troubleshooting.md:44, world/minimap.md:127, world/quests.md:128
- "알림](…)와" → "과": reference/glossary.md:108, windows/chat.md:226, windows/system.md:168, world/minimap.md:173
(전체 설명서를 `알림\]\([^)]*\)(를|와)`로 grep한 결과다. 링크가 아닌 "알림를"은 따로 확인하지 않았다.)

##### (e2) 따옴표 없는 설정·상태 이름이 문장에 녹아 경계가 안 들림
영어는 대문자(Missing, Cast by Me, Only)로 이름임을 알리지만 한국어는 그 표시가 사라진다. 이름이 "없음", "내가 시전", "해당만", "기본", "이 값 미만일 때 반복"처럼 평범한 구절이면 귀로는 문장의 일부로 들린다. 원문에 없는 따옴표는 넣지 않는 규칙이므로, 이름 뒤에 종류 명사(상태, 설정, 필터, 버튼)를 붙이는 방법을 제안한다. 원문에 없는 낱말을 더하는 일이라 **사용자 방침 결정이 필요하다**(확신도: 문제 인식 높음, 해법 중간).
- information/group-health.md:41 | 생명력이 자기 역할의 이 값 미만일 때 반복 설정값보다 낮은 구성원은 반복 간격마다 번호가 다시 들립니다. | Every member below their role's Repeat Below value is spoken again at the interval of Repeat Every. | 생명력이 자기 역할의 이 값 미만일 때 반복 설정의 값보다 낮은 구성원은 반복 간격 설정에 정한 시간마다 번호가 다시 들립니다. | 설정 이름 안의 "이 값"이 지시어로 들린다. 근본 해결은 로케일 값 쪽이다(4절 L1).
- information/buffers.md:122 | 전체로 두면 필터를 적용하지 않습니다. 해당만으로 두면 필터가 가리키는 오라만 남깁니다. ... 내가 시전을 해당만으로 두면 내가 건 오라만 나열하고 | Cast by Me set to Only lists only auras that you cast | 값을 전체로 설정하면 필터를 적용하지 않습니다. 해당만으로 설정하면 그 필터에 해당하는 오라만 남깁니다. ... 내가 시전 필터를 해당만으로 설정하면 내가 건 오라만 나열하고
- information/buffers.md:328 | 내 약화 효과만 궁금하면 내가 시전을 해당만으로 설정합니다. | → 내가 시전 필터를 해당만으로 설정합니다.
- information/buffers.md:135 | 예전 설정인 내 오라만은 이제 내가 시전입니다. 내 오라만이 켜져 있던 버퍼는 내가 시전을 설정할 때까지 | The old setting Only My Auras is now Cast by Me | 예전의 내 오라만 설정은 이제 내가 시전 필터입니다. 내 오라만 설정이 켜져 있던 버퍼는 내가 시전 필터를 설정할 때까지
- information/buffers.md:201 | 기본값은 기본이며, 이것은 그 종류의 표준 문구(위의 예)입니다. | By default it reads Default | 처음에는 기본으로 설정되어 있으며, 기본은 그 종류의 표준 문구(위의 예)입니다. | "기본값은 기본이며"는 동어 반복으로 들린다.
- information/monitors.md:40 | 없음은 대체가 없습니다. | Missing has no fallback | 없음 상태는 대체가 없습니다. 같은 꼴: 142(없음은 추적하던 오라가 사라질 때 말합니다), 328(없음을 열고), 354(없음과 확산의 TTS 알림을 켭니다), 331(효과 적용이 딸깍 소리를 냅니다).
- information/monitors.md:26 | 규칙의 주문(또는 내가 적용함), 모니터의 유닛을 변경하거나 | a rule's Spell (or Applied by Player), the monitor's Unit | 규칙의 주문 설정(또는 내가 적용함 설정), 모니터의 유닛 설정을 변경하거나. 같은 꼴: 144, 362(내가 적용함을 꺼야 합니다).
- information/monitors.md:311 | 주문 이름은 입력란을 엽니다. | Spell Name opens a text field. | 주문 이름에서 Enter를 누르면 입력란이 열립니다.
- information/buffers.md:327 | (추가는 "플레이어 약화 효과"로 시작하는 새 행을 끝에 붙입니다. | Add appends a new row that starts as "Player Debuffs" | (추가 버튼은 처음 값이 "플레이어 약화 효과"인 새 행을 끝에 추가합니다.
- reference/keybindings.md:107 | 길 안내의 비컨과 경로 모듈에 있는 Alt Gr로 거리 알림 설정으로 이 기능을 끌 수 있습니다. | can be turned off with the Announce Distance with Alt Gr setting | 이 기능은 길 안내의 비컨과 경로 모듈에 있는 Alt Gr로 거리 알림 설정에서 끌 수 있습니다. | 이름 속 "로"와 조사 "으로"가 겹친다.

##### (e3) 파일 사이 용어 불일치 (같은 원문, 다른 한국어)
translation-guide `### 용어` 3번은 파일 사이에 갈린 말을 고칠 때 용어집에도 올리라고 정한다. 아래는 용어집 후보다.
| 원문 | 갈린 표기 | 위치 | 제안 |
|---|---|---|---|
| tab stop | 탭 정지점 / 탭 위치 | basics/interface.md, reference/glossary.md:58 / reference/keybindings.md:23, 24 | 탭 정지점(용어집 표제어가 이미 이 말) |
| modifier | 보조 키 / 조합 키 | basics/interface.md:42 / reference/keybindings.md:37, 38 | 하나로 통일(게임 공식 표기 확인 필요, 모름) |
| navigation keys | 이동 키 / 탐색 키 | basics/interface.md / reference/commands.md:207 | 이동 키 |
| keybinding window | 단축키 화면 / 단축키 창 | buffers.md:31, monitors.md:226, 281, 305, ref/keybindings.md:4 / ref/commands.md:27, 76, ref/glossary.md:62, 116 | 하나로 통일. commands.md:76은 한 문단에서 "단축키 창 ... 화면과 같습니다"로 둘을 섞는다 |
| binding | 바인딩 / 단축키 | ref/glossary.md:16, 62 / 그 밖 전부 | 용어집 표제어 "바인딩"이 본문에서는 쓰이지 않는다. 표제어를 "단축키(바인딩)"로 할지 결정 필요 |
| route planner | 경로 계획 도구 / 경로 계획기 | ref/glossary.md:70 / ref/versions.md:58 | 경로 계획 도구(위 35번) |
| pitch | 음 높이 / 음높이 | group-health.md:6, 31, 33, 62, 104, information/index.md:8 / ref/glossary.md:14, 32, ref/keybindings.md:159, ref/versions.md:48 | 음높이(표준국어대사전 표제어, 한 낱말) |
| loaded (addon) | 불러온 상태 / 로드되어 | ref/commands.md:115, 119, 123, 256, ref/versions.md:132 / ref/keybindings.md:195 | 불러오다 |
| enabled (monitor) | 켜진 / 사용 중인 | monitors.md:224, 279 / ref/keybindings.md:157, 158 | 켜진 |
| see | 보십시오 / 참고하십시오 | buffers.md 14곳, monitors.md 5곳, ref/glossary.md:108 한 곳 / group-health.md, reference 전체 | 참고하십시오(다수). 뜻은 통하므로 우선순위 낮음 |
| On, Off (기본값 열) | 켬·끔 / 켜짐·꺼짐 | buffers.md, monitors.md 표 / group-health.md 표 | 하나로 통일 |
| voice | 음성 / 목소리 | 대부분 / monitors.md:103, ref/glossary.md:60, 100 | 음성(설정 이름이 "음성 종류") |
표 칸의 문체도 갈린다. monitors.md 표는 명사형("소리를 켬"), buffers.md와 group-health.md 표는 합니다체이고, buffers.md:116, 117은 한 칸 안에 둘이 섞였다("들리는 이름. 비우면 ... 됩니다"). 확신도 낮음(뜻은 통함).

#### 4. 로케일 값 문제 (설명서만 고칠 수 없음)

L1. information/group-health.md:41, 57, 96 | "이 값 미만일 때 반복" | koKR groupHealth.lua:19 `Repeat Below (percent)` = "이 값 미만일 때 반복 (퍼센트)" | 이름 안에 지시어 "이 값"이 있어서 설명서 문장에 넣으면 "자기 역할의 이 값 미만일 때 반복 설정값"처럼 들린다. 메뉴에서 단독으로 들을 때는 문제가 없으므로 로케일 변경 여부는 사용자 판단. 후보: "반복 기준 생명력 (퍼센트)". 확신도 중간.
L2. information/buffers.md:122, 135, 328, 373 | "해당만", "전체", "제외" | buffers.lua:26~28 Any/Only/Not | "해당만으로 두면"은 귀로 "해당 만으로"와 구별되지 않는다. 설명서에서는 "필터"와 "설정하면"을 붙여 완화할 수 있고(e2), 값 자체는 로케일 소관. 확신도 낮음.
L3. information/buffers.md:135 | "내 오라만", "내가 시전" | buffers.lua:22, 29 | 조사가 붙으면 "내 오라만은", "내가 시전을"이 되어 이름으로 안 들린다. 설명서에서 종류 명사를 붙이는 것으로 해결 가능(e2).
L4. information/monitors.md:49, 322, 335 | "신규 Aura", "Aura를 고릅니다", "Cooldown을 고릅니다" | ui.lua:222 New = "신규". 종류 이름 "Aura"는 koKR 키가 없고(코드 core/graph/settings.lua:381이 `L["New"] .. " " .. typeLabel`로 조립), "Cooldown"은 monitors.lua:72에 "재사용 대기"가 있다 | 설명서 335줄이 실제 화면과 같은지 모름(확인 방법: 게임에서 모니터 종류 선택 목록을 열어 본다). "Aura"가 실제로 영어로 나오면 코드에 박힌 영어이므로 docs/upstream-report.md 대상이다. 또 같은 로케일 안에서 New가 "신규"(신규 고정 버퍼)와 "새"(ui.lua:221 "새 버퍼")로 갈린다.
L5. reference/keybindings.md:107 | "Alt Gr로 거리 알림" | navigation.lua:102 | 이름이 "로"로 이어지는 구절이라 문장 안에서 조사와 겹친다. 설명서 어순 변경으로 완화 가능(e2 마지막 항목).
L6. information/monitors.md:188 | "항목 메뉴에서 알림을 고르면(신규 경보 또는 기존 경보 편집) 게임의 알림 편집기가 별도 창으로 열립니다" | 게임 공식 COOLDOWN_VIEWER_SETTINGS_ADD_NEW_ALERT = "신규 경보", ..._EDIT = "경보 편집"(cache/gs_koKR.csv). WowVision 창 이름은 windows.lua:281 Alert Editor = "알림 편집기" | 한 문장 안에서 같은 것이 "알림"과 "경보"로 갈린다. 게임 메뉴 글자는 "경보"이고 WowVision이 읽는 창 이름은 "알림"이다. alert = 알림 결정(2026-11-07)의 예외로 이 창 이름만 "경보 편집기"로 할지는 사용자 판단. 설명서에서는 "항목 메뉴에서 경보 항목(신규 경보 또는 기존 경보 편집)을 고르면"으로 앞부분을 실물에 맞출 수 있다.
L7. information/monitors.md 여러 곳 | 상태 이름 "없음" | monitors.lua:59 Missing = "없음" | 문장 주어로 쓰면 "없음은 대체가 없습니다"가 된다. 알림 발화("달빛섬광 없음")로는 자연스러우므로 로케일은 유지하고 설명서에서 "없음 상태"로 쓰는 쪽을 권한다.

#### 5. 고치지 않는 것(과잉 수정 방지 메모)

- "훑어보다"(walk through, buffers.md 여러 곳), "담다"(hold), "맡기다"(leave to Sku), "스스로 채워지고 비워집니다"는 뜻이 바로 통한다.
- information/group-health.md:13 "기본 목록의 맨 끝, 퀘스트 다음에 있습니다"는 원문(G를 눌러 이동)과 다르지만 한국어 메뉴 순서에 맞춘 것으로, decisions.tsv 2026-11-05 예외(메뉴 글자 이동)에 해당한다.
- 오라 "갱신"(monitors.md:133, 213, 356, glossary.md:44)은 게임 용어 예외다.
- reference/commands.md의 "덤프"(170, 244, 245, 248, 250, 253)는 개발자용 표 안이라 유지해도 된다. 170줄만 일반 명령 표라서 "원시 데이터를 그대로 출력합니다"를 고려할 수 있다(낮음).
- 링크 글자가 대상 제목과 다른 곳(buffers.md:240 "WowVision 창 사용하기", keybindings.md:201 "설치")은 원문 링크 글자 유지 결정에 따른 것이다.

#### 6. 건수 요약

| 부류 | 건수 |
|---|---|
| (a) 지시어 | 4건(5곳) |
| (b) 관용구·은유 직역 | 18건(약 27곳, 키 가져가기 계열 3곳 포함) |
| (c) 목적어·주어 생략 | 10건(11곳) |
| (d) 동사·낱말 선택 | 7건(12곳) + 반복 표현 R1~R5 |
| (e1) 조사 오류 | 16곳(설명서 전체 grep, 이 범위 안 5곳) |
| (e2) 이름이 문장에 녹음 | 10건(약 18곳) |
| (e3) 파일 사이 용어 불일치 | 12쌍 + 표 문체 |
| 로케일 값 문제 | 7건 |

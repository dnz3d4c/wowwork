# WowVision 설명서 한국어 번역 계획

## 현재 상태

- 상태: 51개 파일 번역, 평가, 회귀 확인 완료 (2026-11-06). 회귀는 3회차까지 돌렸고(중대 이상 167 → 38 → 21건), 남은 21건은 `docs/decisions.tsv` 2026-11-06 기준으로 처리했다. 기록은 `reviews/2026-11-05-manual-regression`, `reviews/2026-11-06-manual-regression2`, `reviews/2026-11-06-manual-regression3`. 원문과 실제 동작이 다른 곳은 `reviews/2026-11-05-manual-regression/upstream-raw.json`에 모았다(upstream 보고 전, 중복 정리 필요). 남은 일: 사용자 최종 확인(절차 6단계)
- 다듬기 결과 (2026-11-07): 본 평가 지적 1,427건 중 1,283건 반영, 회귀 확인 2회(1회차 51개 중 24개 통과, 2회차 45개 중 28개 통과), 상한 뒤 근거가 글자 그대로 확인된 32건 반영. 사용자 결정 4건(alert=알림, koKR 변경 기준, 버전 이름 영어, Buffered=모아 말하기)을 koKR·용어집·설명서에 반영. koKR 변경 후보 9종은 두 회사 판정이 모두 일치해 2건(죽음, 핵심 능력)만 반영, 공유 키 3개와 띄어쓰기 1건은 `docs/upstream-report.md` 3·4절. 기록: `reviews/2026-11-07-*`. 남은 일: 사용자 판단 목록(아래 다듬기 항목의 남은 결정), 설명서 재배포, 설치 프로그램 재빌드
- 다듬기 (2026-11-06 사용자 지시): 게임 설명서 적합성 기준으로 51개 파일을 다시 본다. 사용자 예시는 "경보는 알림이 아닐까"(`basics/alerts.md`)와 "그 화면 같은 표현"(`basics/keybindings.md`)이다. 스크린리더 낭독은 사용자가 판단하므로 평가에서 뺐다. 페르소나 3명(한국어 WoW 용어·기능 검수자, 한국어 게임 설명서 편집자, WowVision을 처음 설치한 플레이어)을 Claude와 GPT가 따로 맡는다(`tools/review/prompts/polish-*.md`, `tools/review/workflows/manual-polish.js`). 페르소나 설계는 GPT 검토를 받아 고쳤다. 오류 심기 검증은 2회 했다: 1회차는 Claude 7/8, GPT 6/8로 GPT가 기준에 못 미쳐 프롬프트를 고쳤고, 2회차는 다른 파일에 새로 심어 Claude 13/15, GPT 14/15, 오탐 0건이었다(`reviews/2026-11-06-manual-polish-calibrate`). koKR 문구나 여러 파일에 걸친 용어를 바꾸자는 지적(alert=경보 포함)은 파일에서 고치지 않고 모아서 사용자 결정을 받는다. 기록: `reviews/2026-11-06-manual-polish`
- 설치 프로그램에 설명서는 넣지 않는다(`docs/decisions.tsv` 2026-11-06)
- 공개 주소: https://gong.aheu.org/WowVision/user/ko/getting-started/introduction.html (2026-11-06 사용자 지시로 `dnz3d4c/WowVision` 공개, GitHub Pages는 Actions 방식, 계정 개인 도메인 gong.aheu.org). ko 브랜치에 push해도 자동 배포되지 않는다(원본 `docs.yml`은 main push에만 돈다). 설명서를 고친 뒤 `gh workflow run docs.yml -R dnz3d4c/WowVision --ref ko`로 다시 배포한다. main에 push하면 원본 `docs.yml`(영어판으로 Pages를 덮어씀)과 `beta.yml`(beta 프리릴리스 생성)이 돈다. main을 원본에 맞출 때는 `gh workflow disable`로 두 워크플로를 끄고 push한 뒤 다시 켠다(2026-11-07 V1.0.1 갱신 때 이렇게 했고 실행된 작업 없음을 확인함). 원본 태그(V*)는 push하지 않는다(`release.yml`). 배포 허용 브랜치(github-pages 환경)에 ko를 추가해 두었다.
- 기준 원문: 번역은 upstream `397ffc3`(V1.0.0 태그 + 문서 커밋 2개) 기준이다. 2026-11-07 원본 V1.0.1(`2c7d4cb`)을 main과 ko에 병합하고 서브모듈을 원본 기록대로 맞췄다(locale 3a77089, WoW_NavigationData 0d79304, 나머지 그대로, 네 개 모두 각 원격의 최신). vision-locale main에도 원본 3a77089를 병합했다. koKR 새 키 66개(targeting 52, navigation 6, windows 3, buffers 2, quests 2, ui 1)는 2026-11-07 번역·평가를 마쳤다(`reviews/2026-11-07-ui-v1.0.1`, vision-locale a78f05a). 남은 일(4단계 유지 절차): V1.0.1에서 바뀐 영어 설명서 14개 파일을 다시 번역한다. 그중 9개(basics/keybindings, information/buffers, reference/commands, reference/keybindings, windows/group-finder, world/movement, world/navigation, world/targeting, world/wownav)는 `tools.manual check`가 구조 차이로 잡는다.- 번역본 위치: 비공개 복제 저장소 `dnz3d4c/WowVision`의 `docs/src/user/ko` (2026-11-05 결정). 완성 후 공개한다.
- 품질 평가: 모든 묶음이 `docs/review-process.md`를 통과해야 커밋한다(Claude 5명 + GPT 5명 블라인드 평가, 교차 판정).
- 결정 대기: 아래 `## 미결 결정` 2건.

## 규모

upstream `docs/src/user/en`을 실측한 결과다(`docs/src/user/de`도 같은 구성이다).

| 항목 | 값 |
|------|----|
| 파일 | 51개 (mdBook, `docs/src/SUMMARY.md`가 목차) |
| 영어 단어 | 107,090 |
| 가장 큰 파일 | `information/buffers.md` 5,497단어, `getting-started/sku-login.md` 5,447단어, `world/navigation.md` 4,682단어 |
| 따옴표로 인용된 문구 | 1,359개, 그중 531개가 enUS 로케일 문자열과 정확히 일치 |
| 본문에 등장하는 두 단어 이상 로케일 문자열 | 585종, 1,984회 (메뉴 이름·설정 이름·알림 문구) |
| 상대 링크 | 459개 |
| 변경 빈도 | 2026-09-01 이후 `docs/src/user` 커밋 64개 |

여기서 계획의 전제 세 가지가 나온다.

1. **설명서는 UI 문자열 번역과 분리할 수 없다.** 설명서가 "TTS Alert를 켠다"라고 하면 한국어판은 게임이 실제로 말하는 "TTS 경보"를 써야 한다. koKR 번역값이 설명서의 용어집이다.
2. **원문이 자주 변경된다.** 한 번 번역하고 끝나는 문서가 아니므로, 파일마다 어느 원문 커밋을 번역했는지 기록하고 변경분만 다시 번역해야 한다.
3. **양이 많아 한 번에 끝낼 수 없다.** 묶음 단위로 나눠 진행하고, 묶음마다 기계 검사를 통과시킨다.

## 원칙

### 원문

- 원문은 영어판이다. `book.toml`의 언어가 `en`이고 개발자 문서도 영어다. 영어판과 독일어판은 같은 커밋(`95122f9`, Broesel33)에서 추가됐고 제목 수가 파일마다 같다.
- 독일어판은 뜻이 애매할 때 대조하는 참고본으로만 사용한다.
- 개발자 문서(`docs/src/developer`)는 번역하지 않는다.

### 용어

우선순위는 앞의 것이 이긴다.

1. **koKR 번역값.** 원문에 로케일 문자열이 나오면 그 키의 한국어 값을 그대로 쓴다. 따옴표 안팎을 가리지 않는다.
2. **게임 공식 한국어.** `cache/game_terms.tsv`와 GlobalStrings. 기준은 `docs/translation-guide.md` `## 용어`와 같다(문맥 우선).
3. **설명서 전용 용어집.** 로케일에 없지만 설명서에 반복되는 말(예: Sku, Sku Login Tool, route network)은 `docs/manual-glossary.tsv`에 한 번 정하고 따른다.
4. 셋 다 없으면 보고 목록에 올리고 지어내지 않는다.

설명서를 번역하다 koKR 번역값이 어색하다고 판단되면 설명서만 다르게 쓰지 않는다. koKR 값을 고치고 설명서가 그 값을 따른다. 듣는 말과 읽는 말이 갈라지지 않게 하기 위해서다.

### 번역하지 않는 것

키 이름(Shift, Ctrl, F10 등), 슬래시 명령(`/wv`, `/focus1`), 인라인 코드와 코드 블록, URL, 파일 경로, 고유 이름(WowVision, WowNav, Sku, WoW: Forever, Battle.net, Discord). 링크 대상 경로도 변경하지 않고 링크 텍스트만 번역한다.

### 문체

- 습니다체로 쓴다. 설명서는 Tutorial(시작하기), How-to(창별 사용법), Reference(키·명령·용어집)가 섞여 있고 셋 다 습니다체다.
- 독자를 부르는 "you"는 대부분 생략한다. "You hear X" → "X라고 들립니다"가 아니라 "X라고 안내합니다" 식으로 주어를 프로그램으로 둔다. 원문 뜻이 달라지는 경우만 예외다.
- 원문 구조를 그대로 둔다: 제목 수준, 표의 행과 열, 목록 항목 수, 링크 수. 스크린리더 사용자는 제목 단위로 탐색하므로 구조가 원문과 같아야 영어판 안내와도 대조할 수 있다.
- 원문에 없는 내용을 덧붙이지 않는다. 한국 사용자에게 필요한 보충 설명이 생기면 보고 목록에 올린다.

## 진행 단계

### 1단계: 도구 (번역 전)

1. `tools/doc_terms.py`: 파일 하나를 받아 그 안에 등장하는 로케일 문자열과 koKR 값, 설명서 용어집 항목을 표로 출력한다. 번역할 때 이 표를 함께 넘긴다.
2. `tests/test_manual.py`: 번역된 파일마다 원문과 기계 대조한다.
   - 제목 수와 수준, 표 행 수, 링크 수와 링크 대상, 인라인 코드 목록이 원문과 같은가
   - 원문에 등장하는 로케일 문자열의 koKR 값이 번역문에 들어 있는가 (빠진 것은 실패가 아니라 경고 목록으로 출력. 문장 안에서 조사가 붙거나 문맥상 생략될 수 있기 때문이다)
   - 첫 줄의 원문 커밋 기록이 있는가
3. `tools/doc_status.py`: 번역 파일마다 기록된 원문 커밋과 upstream 현재 커밋을 비교해 원문이 바뀐 파일과 그 diff를 출력한다. 업데이트 때 이 목록만 다시 번역한다.

원문 커밋은 번역 파일 첫 줄에 `<!-- source: docs/src/user/en/<경로> @ <커밋> -->`로 기록한다. mdBook은 HTML 주석을 출력하지 않는다.

### 2단계: 시범 번역 1묶음

`getting-started/`에서 `sku-login.md`를 뺀 9개 파일(약 9,300단어). 사용자가 실제로 읽고 문체·용어를 확정한다. 여기서 정한 것을 이 문서 `## 원칙`에 반영한 뒤 다음 단계로 간다.

### 3단계: 나머지 묶음

묶음 하나는 약 1만 단어, 한 장(章) 단위로 끊는다. 순서는 사용자가 먼저 찾을 곳부터다.

| 순서 | 묶음 | 파일 수 | 단어 |
|------|------|---------|------|
| 1 | 시작하기 (시범, sku-login 제외) | 9 | 9,300 |
| 2 | 기본 (`basics/`) | 7 | 12,700 |
| 3 | 참조 (`reference/`) | 5 | 7,400 |
| 4 | 길 안내 (`world/navigation.md`, `world/wownav.md`, `world/movement.md`) | 3 | 11,200 |
| 5 | 월드 나머지 (`world/` 나머지 6개) | 6 | 12,300 |
| 6 | 정보 (`information/`) | 4 | 11,600 |
| 7 | 게임 창 1 (`windows/` overview, action-bars, bags-and-bank, npcs, loot-trade-mail, character, spells-and-talents) | 7 | 13,800 |
| 8 | 게임 창 2 (`windows/` professions, collections, group-finder, auction-house) | 4 | 11,300 |
| 9 | 게임 창 3 (`windows/` chat, social, system) | 3 | 10,100 |
| 10 | 컨트롤러, 감사의 말, Sku 로그인 도구 | 3 | 7,400 |

단어 수는 반올림한 값이다. 묶음마다 `uv run pytest -q`를 통과한 뒤 커밋한다.

### 4단계: 유지

upstream을 업데이트할 때마다 `docs/translation-guide.md` `## upstream 업데이트 절차`로 문자열을 먼저 맞추고, 그다음 `tools/doc_status.py`로 바뀐 설명서 파일만 다시 번역한다. 문자열을 먼저 맞추는 까닭은 설명서가 koKR 값을 용어로 쓰기 때문이다.

## 미결 결정

1. **읽는 형태는 무엇인가.** 마크다운 파일만 둘지, mdBook으로 HTML까지 만들지. mdBook은 이 PC에 설치되어 있지 않다(`which mdbook` 실패). HTML이 필요하면 scoop으로 설치한다.
2. **Sku 로그인 도구 문서(`sku-login.md`, 5,447단어)를 번역할까.** 두 번째로 큰 파일이고 Sku 사용자 대상이다. 한국 사용자에게 필요한지 판단이 필요해서 마지막 묶음에 두었다.

## 보고 목록 (1.0 문자열 번역에서 나온 것)

설명서 용어에도 영향이 있으므로 여기에 모은다.

- `Direct`: 음성 방식 선택지(`speech.lua`)와 길 안내 창 체크 상자(`navigation.lua`)가 같은 키를 사용한다. 기존 "직접"에 맞췄다. 길 안내 쪽 다른 문구(`Direct: %s, %d yards`, `Direct to the Nearest Unvisited...`)는 기존 `last %d yards direct`="직선"에 맞춰 "직선"으로 했다.
- WoW: Forever 전용 지명 `Rohashi Spires`, `Valanaar`, `Valanaar Sanctuary`, `Wind Bridge`: 리테일 AreaTable에 없어서 공식 한국어가 없다. 영어 그대로 두었다.
- `Raid Groups`: 공식 후보가 "공격대", "공격대 구성"인데 공격대 안의 파티 1~8을 고르는 설정이라 "공격대 파티"로 했다.
- `Guild and Communities`: 공식은 "길드 & 커뮤니티"지만 원문에 없는 기호라서 "길드 및 커뮤니티"로 했다.
- `Stable`: 공식 후보는 "우리"와 "야수 우리"이며, "우리"만으로는 뜻이 모호해서 "야수 우리"로 했다.

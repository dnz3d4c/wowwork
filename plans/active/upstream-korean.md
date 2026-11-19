---
작업: 한국어 패치를 원본 WowVision에 올리기
상태: in_progress
작성일: 2026-11-07
---

**상태**: in_progress

# 한국어 패치를 원본 WowVision에 올리기

## 현황 (Status Board)  [강제]

- 단계: Phase 2 / 전체 6 — koKR 로케일, 관리자 답 대기
- 직전(2026-11-19, 인계 시점): 사용자 결정으로 만든 `Copy` 키 분리 PR(vision-locale#87, WowVision#140)이 2026-11-15에 병합됐다. 원본 V1.0.4(08a7617, 로케일 3172cd5)가 2026-11-17에 나왔지만 아직 병합하지 않았다(README `## 내려받은 뒤 할 일` 3번). V1.0.4를 반영할 때 `CopyName`을 "사본"으로 번역한다. 원본 로그인 툴 4.2가 2026-11-18에 나왔다(README 4번). 설치 프로그램을 원본처럼 안정판 미리 선택으로 되돌려 다시 빌드했다(`docs/builds.md`). #110은 2026-11-14 멘션 뒤에도 답이 없다.
- 그 전(2026-11-14): 원본 V1.0.3 릴리스(82a1a9d, 로케일 8add2d9)를 vision-locale main과 WowVision ko에 병합했다. koKR 새 키 25개를 번역·평가해 넣었고, 사용자 지시로 배·지하철 지점 이름 2개도 장소 이름으로 고쳤다. 한국어 설명서 13쪽을 원본에 맞추고 테스터 설치 프로그램을 다시 빌드했다(`docs/builds.md`). `korean-locale` PR 브랜치는 원본 ca4a12c 기준 그대로다. 사용자 결정으로 `Copy` 키 분리 PR을 열었다(vision-locale#87, WowVision#140, 브랜치 `copy-name`). 병합되면 koKR `CopyName`을 "사본"으로 번역한다. 사용자 지시로 #110에 관리자 bradjrenshaw(지금까지 PR을 병합한 사람)를 멘션해 다시 물었다(2026-11-14). koKR PR을 열어도 되는지와 함께 한국어 설명서(`docs/src/user/ko`)를 원본에 넣어도 되는지 물었다. 포크 사이트 대안은 사용자 지시로 언급하지 않는다(병합 가능 여부가 요점).
- 그 전(2026-11-11): 원본 V1.0.2 릴리스(94c2b0f, 로케일 1048bae)를 vision-locale main과 WowVision ko에 병합했다. koKR 새 키 51개와 11-09 판에서 평가를 건너뛴 21개를 평가해 반영했고, 한국어 설명서 25쪽을 원본에 맞췄다. 테스터 설치 프로그램을 다시 빌드했다(`docs/builds.md`). `korean-locale` PR 브랜치는 아직 원본 ca4a12c 기준이라, PR을 열 때 새 원본 main 위에 다시 만들어야 한다.
- 그 전(2026-11-09): Phase 1(#66, #109)과 Phase 1b(#75, #122)가 2026-11-08 22:39에 병합됐다. 후속으로 vision-locale main과 WowVision ko에 원본 main을 병합하고, koKR 새 키 23개를 번역·평가해 넣었다. 설명서 인용 3곳을 "사용 안 함"으로 되돌리고 배포했으며, payload와 설치 프로그램도 다시 만들었다. PR용 브랜치는 #110 본문이 가리키는 `korean-locale`이고, 원본 main ca4a12c 위의 커밋 하나(b35bd03, enUS와 키 일치)다. 병합 커밋이 섞였던 3be0ed0을 사용자 확인 뒤 강제 push로 교체했다(2026-11-09). 같은 커밋을 가리키던 `korean-locale-v2`는 사용자 지시로 지웠다.
- 다음: #110에 답이 오면 `korean-locale`로 koKR PR을 연다(그때까지 원본 키가 늘면 새 원본 main 위에 커밋 하나로 다시 만든다. 강제 push는 그때마다 사용자 확인). 한국어 설명서 11쪽은 원본 main(5cbf76a)을 따라갔다(평가 지적 75건 중 68건 반영, 회귀 확인 뒤 2건 반영, 모호한 원문 3건은 docs/upstream-report.md 5절). 배포함. Phase 1c는 보류(2026-11-09 사용자 결정). #105, #108이 병합되면 Phase 6의 퀘스트 스캐너 이어 붙이기를 다시 본다.
- 사용자 결정(2026-11-07): 새 이름으로 공개 포크(`vision-locale-pr`, `WowVision-pr`. 2026-11-19에 원래 이름 `vision-locale`, `WowVision`으로 변경, Phase 0), 이번 범위는 koKR만, 큰 단위는 이슈로 먼저 상의. 설치 프로그램·설명서·음성 팩(Phase 3~5)은 이번에 진행하지 않는다.
- 제외한 접근: 기존 비포크 저장소에서 바로 PR 열기(포크가 아니라 불가), `ko` 이력을 섞은 PR 브랜치, Phase 3~5를 이번 범위에 넣기(2026-11-07 사용자 결정).

## 배경  [강제]

목표: 한국어 관리 부담을 최소로 줄인다. 원본에 넣을 수 있는 것은 모두 원본에 넣고, 한국어 전용으로 남는 것은 버전이 올라가도 빨리 합칠 수 있는 작은 덧붙임으로만 남긴다.

원본은 이미 독일어·프랑스어를 세 곳에서 받고 있다: 로케일 저장소(`wow-vision/vision-locale`, WowVision의 `locale` 서브모듈), 설치 프로그램 `Loc.cs`의 `Lang` 표, 설명서 `docs/src/user/de`. 한국어도 같은 틀에 들어갈 수 있다.

2026-11-07 실측:

| 저장소 | 한국어 차이 | 원본에 넣을 수 있는가 |
|--------|-------------|----------------------|
| vision-locale | `koKR/` 24파일 +1711줄, `modules.xml` 1줄. 키 1429개가 enUS와 완전히 일치(deDE는 10개 부족) | 그대로 가능 |
| wowvision-installer | `Loc.cs` Ko 표(206키, En과 일치), `ComponentsForm.cs` 2줄 / 한국어 전용: `KoreanLocale.cs`, `KoreanVoice.cs`, payload 2개, 브리지 기본값, 자체 검사 kolocale·kovoice, `status.korean*` 키 | Ko 표만 가능. 나머지는 포크 전용 |
| WowVision | `docs/src/user/ko` 51쪽(en과 쪽수 같음) + `SUMMARY.md` 54줄. 코드 차이 없음 | 가능하지만 유지 방침 결정이 필요 |
| vision-default-audio | 한국어 음성 팩 Yuna(현재 설치 프로그램이 덮어씀) | 관리자가 정한다(2026-11-19 결정) |

## 실행 계획  [강제]

### Phase 0. 정리 (PR마다 적용)

- PR 브랜치는 `ko` 이력이 아니라 `upstream/main`에서 새로 딴다. 포크 이력의 한국어 커밋 메시지와 포크 전용 변경이 섞이지 않게 하기 위해서다.
- 원본 관례: 커밋 제목 `영역: 내용`(영어), 본문에 이유, `Co-Authored-By` 줄. 로케일 PR과 코드 PR은 같은 브랜치 이름으로 짝을 짓는다. 동작을 바꾸면 en·de 설명서를 함께 고친다. 줄 끝은 LF, BOM 없음.
- 공개 GitHub 포크가 있어야 PR을 열 수 있다. 2026-11-19에 PR용 포크(`-pr`)로 한국어 브랜치를 옮기고 포크의 이름을 원래 이름으로 변경했다(vision-locale, WowVision). 로컬 복제본의 `origin`이 그 포크다.
- PR은 `gh api repos/wow-vision/<저장소>/pulls -f head=<계정>:<브랜치> -f head_repo=<저장소> ...`로 연다. 같은 원본의 저장소가 계정에 둘이던 2026-11-19 이전에는 `gh pr create --head`가 실패했다. 하나로 합친 뒤에는 확인하지 않았다.

### Phase 1. 작은 PR: 경매장 스캔 결과·대기 시간 문구 [병합: vision-locale#66, WowVision#109, 2026-11-08]

- 문제: `" in "`, `" min "`, `" sec"`가 `L[]` 밖에 있어서 모든 언어에서 영어로 나온다(`tbc/auction/ScanSession.lua:147`, `tbc/auction/module.lua:78-93`).
- 수정: 서식 문자열 4개(`Scan complete, %s Results in %s scanned`, `%s min %s sec`, `%s min`, `%s sec`), enUS·deDE·frFR, 독일어 설명서 인용 3곳.
- 열린 원본 PR 16개 중 이 파일들을 고치는 것은 없다.

### Phase 1b. 작은 PR: Disabled·Available 키 분리 [병합: vision-locale#75, WowVision#122, 2026-11-08. 후속 완료 2026-11-09]

- 문제: 한 키를 뜻이 다른 문맥이 같이 쓴다. `Disabled` 16곳 중 14곳은 흐린 버튼(한국어 "사용 불가"), 2곳은 설정 끄기("사용 안 함": `core/targeting/module.lua:322`, `core/objects/types/unit/PVP.lua:28`). `Available`은 특성 1곳("사용 가능")과 Mists 경매장 수량 2곳(공식 "구매 가능 수량": `mists/auction.lua:253`, `284`). 사용자 지적: 퀘스트 수락 버튼이 "사용 안 함"으로 들림.
- 수정: 소수 쪽만 새 키 `SettingDisabled`, `AuctionAvailable`(영어 값은 그대로)로 바꾼다. enUS·deDE·frFR `ui.lua` 끝에 두 키, 독일어·프랑스어는 지금 값.
- 병합 전 koKR: `Disabled` = "사용 불가"(`docs/decisions.tsv` 2026-11-09). 설정 끄기 2곳도 그동안 "사용 불가"로 들린다.
- 병합 뒤 할 일: vision-locale main에 원본 병합, `tools.sync_locale`로 `SettingDisabled` "사용 안 함", `AuctionAvailable` "구매 가능 수량". 설명서 인용 3곳을 "사용 안 함"으로 되돌린다(`world/targeting.md`, `reference/keybindings.md`의 "적 소프트 대상 사용 불가", `information/buffers.md` PvP 줄). 원본 릴리스가 나와야 테스터에게 코드가 닿는다.

### Phase 1c. 설명서 페이지 언어 [미제출]

- 원본 `docs.yml`이 독일어 페이지도 `lang="en"`으로 낸다. ko 브랜치 a5e64f8의 단계(빌드 뒤 `user/<언어>/` 페이지의 `lang` 교체)를 원본에 낼 후보다. 독일어 사용자에게도 이득이라 한국어 PR과 묶지 않고 따로 낼 수 있다.

### Phase 2. koKR 로케일 [승인 필요]

- `upstream/main`에서 `koKR/` 전체와 `modules.xml` 1줄을 커밋 하나로 만든다. PR 직전에 원본 main이 앞서 있으면 기존 브랜치에 병합하지 말고 새 원본 main 위에 다시 만든다(2026-11-09 codex 지적: 병합하면 커밋 하나가 아니게 된다).
- 이후 관리: 원본에 키가 추가되면 키 대조 스크립트로 빠진 키를 찾아 koKR 보충 PR을 낸다. 빠진 키는 AceLocale이 영어로 대신 보여 주므로 원본 기여자에게 부담이 없다.
- 로케일 저장소 밖의 언어별 표(2026-11-09 발견, 게임에서 미확인). koKR PR을 낼 때 함께 다룰지 정한다.
  - `core/minimap/gatheringNames.lua`: 채집물 이름이 enUS·deDE·frFR만 있고 없는 언어는 enUS로 대체한다(7-8줄 주석). 미니맵 글자와 이름을 부분 일치로 맞추므로 한국어 클라이언트에서는 채집물 탐지가 안 될 것으로 추정한다. 확인: 한국어 클라이언트에서 약초 찾기를 켜고 미니맵 스캔이 알리는지 듣는다. 고치면 `core/minimap/tests.lua`에 koKR 테스트를 더한다.
  - WowNav의 생물·물체 이름은 원본 #113부터 영어·독일어 외 클라이언트에서 Questie의 현지어 이름을 쓴다(`camelot/wownav/text.lua:195-200`). 한국어 클라이언트에도 따로 할 일 없이 적용된다(게임에서 미확인).
  - `mapdata/WowVision_MapData_TBC/locale/`: 지명 번역이 deDE·frFR만 있다. `wv-mapdata-tools/names.py`가 만드는 파일이라 mapdata 저장소에 따로 PR을 낸다.
- `changes-latest.md` 한 줄은 필수가 아니다(병합된 외부 PR 9개 중 3개만 넣었다). 넣는다면 `changes.md:89`의 독일어·프랑스어 줄 형식을 따른다.

### Phase 3. 설치 프로그램 한국어 화면 [승인 필요]

- `Loc.cs` Ko 표, `Lang.Ko`, `ko` 감지, `ComponentsForm.cs` 언어 이름, 표 머리 주석(`English/German/French`)만 넣는다.
- 빼는 것: `status.koreanFailed`·`status.koreanVoiceFailed` 키(En/De/Fr 표에서도), `KoreanLocale.cs`, `KoreanVoice.cs`, payload, 브리지 기본값, 자체 검사 kolocale·kovoice.
- 원본 `build.ps1 -RunTests` 통과를 확인한다.

### Phase 4. 한국어 설명서 [승인 필요, 방침 결정]

- 원본의 기능 PR은 모두 en·de 설명서를 함께 고친다(열린 PR 8개 모두). ko를 넣으면 기여자가 ko를 고칠 수 없으므로 ko는 늘 뒤처진다. 원본에 넣을지, "ko는 뒤처질 수 있음"과 한국어 관리자를 밝히고 넣을지, 포크에 둘지 결정이 필요하다.

### Phase 5. 한국어 음성 팩 Yuna [승인 필요]

- Yuna는 이전 관리자가 작업한 음성 엔진이다. `wow-vision/vision-default-audio`에 PR을 낼지는 관리자가 정한다(`docs/decisions.tsv` 2026-11-19).

### Phase 6. 나중으로 미룬 것

- "12 개 출현 지점" 이어 붙이기(`core/quests/scanner.lua:111,156`): 열린 PR #103, #105, #108이 같은 파일을 고치고 있어 지금 내면 충돌한다. 합쳐진 뒤 낸다.
- 같은 키를 여러 문맥이 쓰는 문제(`Trainers`, `Repair`, `Available`): 키를 나누는 설계가 필요하다. 이슈로 먼저 상의한다.
- `docs/upstream-report.md` 1번(설명서와 동작 차이)은 한국어와 무관하고 사람이 확인하지 않았으므로 이 작업 범위가 아니다.

### 끝난 뒤 포크에 남는 한국어 전용 부분

- 설치 프로그램: NVDA 브리지 기본 설치(원본은 꺼 둔다), 로그인 툴 한국어판 덮어쓰기(`KoreanLoginTool.cs`, `koLoginTool.zip`), 센스 리더 프록시(서브모듈 `korean`, `koSenseReader.zip`). Phase 2가 원본 릴리스에 들어가면 `KoreanLocale.cs`와 koKR payload는 지운다. Phase 5가 들어가면 `KoreanVoice.cs`도 지운다.

## 검증 방법  [강제]

- Phase 1: 영어 출력이 수정 전과 바이트 단위로 같은지 luajit로 비교(통과), 원본 `luajit tools/headless-tests.lua` 629개 통과. 게임 안에서는 확인하지 않았다.
- Phase 2: 키 대조 스크립트로 enUS와 koKR 키 집합이 같은지 확인한다.
- Phase 3: 원본 `build.ps1 -RunTests` 통과, Ko 표 키가 En과 같은지 확인한다.
- 모든 PR: `git diff upstream/main` 결과에 포크 전용 파일과 한국어 커밋 메시지가 없는지 확인한다.
- 강제층: 해당없음(이 저장소의 자동화 동작을 바꾸지 않는다. PR 관례 준수는 위 수동 확인으로만 지킨다).

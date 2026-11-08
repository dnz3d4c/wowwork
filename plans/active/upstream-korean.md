---
작업: 한국어 패치를 원본 WowVision에 올리기
상태: in_progress
작성일: 2026-11-07
---

**상태**: in_progress

# 한국어 패치를 원본 WowVision에 올리기

## 현황 (Status Board)  [강제]

- 단계: Phase 2 / 전체 6 — koKR 로케일, 관리자 답 대기
- 직전: 경매장 PR wow-vision/vision-locale#66, wow-vision/WowVision#109 제출. koKR 상의 이슈 wow-vision/WowVision#110 제출. koKR 브랜치는 `dnz3d4c/vision-locale-pr`의 `korean-locale`(3a37df9)에 준비됨.
- 다음: #110에 답이 오면 koKR PR을 연다. #66이 합쳐지면 새 키 4개의 koKR 값을 보충한다.
- 사용자 결정(2026-11-07): 새 이름으로 공개 포크(`vision-locale-pr`, `WowVision-pr`), 이번 범위는 koKR만, 큰 단위는 이슈로 먼저 상의. 설치 프로그램·설명서·음성 팩(Phase 3~5)은 이번에 진행하지 않는다.

## 배경  [강제]

목표: 한국어 관리 부담을 최소로 줄인다. 원본에 넣을 수 있는 것은 모두 원본에 넣고, 한국어 전용으로 남는 것은 버전이 올라가도 빨리 합칠 수 있는 작은 덧붙임으로만 남긴다.

원본은 이미 독일어·프랑스어를 세 곳에서 받고 있다: 로케일 저장소(`wow-vision/vision-locale`, WowVision의 `locale` 서브모듈), 설치 프로그램 `Loc.cs`의 `Lang` 표, 설명서 `docs/src/user/de`. 한국어도 같은 틀에 들어갈 수 있다.

2026-11-07 실측:

| 저장소 | 한국어 차이 | 원본에 넣을 수 있는가 |
|--------|-------------|----------------------|
| vision-locale | `koKR/` 24파일 +1711줄, `modules.xml` 1줄. 키 1429개가 enUS와 완전히 일치(deDE는 10개 부족) | 그대로 가능 |
| wowvision-installer | `Loc.cs` Ko 표(206키, En과 일치), `ComponentsForm.cs` 2줄 / 한국어 전용: `KoreanLocale.cs`, `KoreanVoice.cs`, payload 2개, 브리지 기본값, 자체 검사 kolocale·kovoice, `status.korean*` 키 | Ko 표만 가능. 나머지는 포크 전용 |
| WowVision | `docs/src/user/ko` 51쪽(en과 쪽수 같음) + `SUMMARY.md` 54줄. 코드 차이 없음 | 가능하지만 유지 방침 결정이 필요 |
| vision-default-audio | 한국어 음성 팩 Yuna(현재 설치 프로그램이 덮어씀) | 라이선스 미확인 |

## 실행 계획  [강제]

### Phase 0. 정리 (PR마다 적용)

- PR 브랜치는 `ko` 이력이 아니라 `upstream/main`에서 새로 딴다. 포크 이력의 한국어 커밋 메시지와 포크 전용 변경이 섞이지 않게 하기 위해서다.
- 원본 관례: 커밋 제목 `영역: 내용`(영어), 본문에 이유, `Co-Authored-By` 줄. 로케일 PR과 코드 PR은 같은 브랜치 이름으로 짝을 짓는다. 동작을 바꾸면 en·de 설명서를 함께 고친다. 줄 끝은 LF, BOM 없음.
- 공개 GitHub 포크가 있어야 PR을 열 수 있다. 기존 저장소(`dnz3d4c/vision-locale` 등)는 포크가 아니다. PR용 포크는 `dnz3d4c/vision-locale-pr`, `dnz3d4c/WowVision-pr`이고 로컬 복제본의 remote 이름은 `fork`다.
- `gh pr create --head dnz3d4c:브랜치`는 같은 계정에 같은 원본의 저장소가 여럿이라 실패한다. `gh api repos/wow-vision/<저장소>/pulls -f head=dnz3d4c:<브랜치> -f head_repo=<포크 이름> ...`로 연다.

### Phase 1. 작은 PR: 경매장 스캔 결과·대기 시간 문구 [제출: vision-locale#66, WowVision#109]

- 문제: `" in "`, `" min "`, `" sec"`가 `L[]` 밖에 있어서 모든 언어에서 영어로 나온다(`tbc/auction/ScanSession.lua:147`, `tbc/auction/module.lua:78-93`).
- 수정: 서식 문자열 4개(`Scan complete, %s Results in %s scanned`, `%s min %s sec`, `%s min`, `%s sec`), enUS·deDE·frFR, 독일어 설명서 인용 3곳.
- 열린 원본 PR 16개 중 이 파일들을 고치는 것은 없다.

### Phase 2. koKR 로케일 [승인 필요]

- `upstream/main`에서 `koKR/` 전체와 `modules.xml` 1줄을 커밋 하나로 만든다.
- 이후 관리: 원본에 키가 추가되면 키 대조 스크립트로 빠진 키를 찾아 koKR 보충 PR을 낸다. 빠진 키는 AceLocale이 영어로 대신 보여 주므로 원본 기여자에게 부담이 없다.
- 로케일 저장소 밖의 언어별 표(2026-11-09 발견, 게임에서 미확인). koKR PR을 낼 때 함께 다룰지 정한다.
  - `core/minimap/gatheringNames.lua`: 채집물 이름이 enUS·deDE·frFR만 있고 없는 언어는 enUS로 대체한다(7-8줄 주석). 미니맵 글자와 이름을 부분 일치로 맞추므로 한국어 클라이언트에서는 채집물 탐지가 안 될 것으로 추정한다. 확인: 한국어 클라이언트에서 약초 찾기를 켜고 미니맵 스캔이 알리는지 듣는다. 고치면 `core/minimap/tests.lua`에 koKR 테스트를 더한다.
  - `mapdata/WowVision_MapData_TBC/locale/`: 지명 번역이 deDE·frFR만 있다. `wv-mapdata-tools/names.py`가 만드는 파일이라 mapdata 저장소에 따로 PR을 낸다.
- `changes-latest.md` 한 줄은 필수가 아니다(병합된 외부 PR 9개 중 3개만 넣었다). 넣는다면 `changes.md:89`의 독일어·프랑스어 줄 형식을 따른다.

### Phase 3. 설치 프로그램 한국어 화면 [승인 필요]

- `Loc.cs` Ko 표, `Lang.Ko`, `ko` 감지, `ComponentsForm.cs` 언어 이름, 표 머리 주석(`English/German/French`)만 넣는다.
- 빼는 것: `status.koreanFailed`·`status.koreanVoiceFailed` 키(En/De/Fr 표에서도), `KoreanLocale.cs`, `KoreanVoice.cs`, payload, 브리지 기본값, 자체 검사 kolocale·kovoice.
- 원본 `build.ps1 -RunTests` 통과를 확인한다.

### Phase 4. 한국어 설명서 [승인 필요, 방침 결정]

- 원본의 기능 PR은 모두 en·de 설명서를 함께 고친다(열린 PR 8개 모두). ko를 넣으면 기여자가 ko를 고칠 수 없으므로 ko는 늘 뒤처진다. 원본에 넣을지, "ko는 뒤처질 수 있음, 관리자 dnz3d4c"를 밝히고 넣을지, 포크에 둘지 결정이 필요하다.

### Phase 5. 한국어 음성 팩 Yuna [승인 필요]

- Vocalizer Expressive 음성 녹음을 재배포해도 되는지 확인하지 않았다(미확인). 사용권을 확인한 뒤 `wow-vision/vision-default-audio`에 PR을 낼지 정한다.

### Phase 6. 나중으로 미룬 것

- "12 개 출현 지점" 이어 붙이기(`core/quests/scanner.lua:111,156`): 열린 PR #103, #105, #108이 같은 파일을 고치고 있어 지금 내면 충돌한다. 합쳐진 뒤 낸다.
- 같은 키를 여러 문맥이 쓰는 문제(`Trainers`, `Repair`, `Available`): 키를 나누는 설계가 필요하다. 이슈로 먼저 상의한다.
- `docs/upstream-report.md` 1번(설명서와 동작 차이 13건)은 한국어와 무관하고 사람이 확인하지 않았으므로 이 작업 범위가 아니다.

### 끝난 뒤 포크에 남는 한국어 전용 부분

- 설치 프로그램: NVDA 브리지 기본 설치(원본은 꺼 둔다). Phase 2가 원본 릴리스에 들어가면 `KoreanLocale.cs`와 koKR payload는 지운다. Phase 5가 들어가면 `KoreanVoice.cs`도 지운다.

## 검증 방법  [강제]

- Phase 1: 영어 출력이 수정 전과 바이트 단위로 같은지 luajit로 비교(통과), 원본 `luajit tools/headless-tests.lua` 629개 통과. 게임 안에서는 확인하지 않았다.
- Phase 2: 키 대조 스크립트로 enUS와 koKR 키 집합이 같은지 확인한다.
- Phase 3: 원본 `build.ps1 -RunTests` 통과, Ko 표 키가 En과 같은지 확인한다.
- 모든 PR: `git diff upstream/main` 결과에 포크 전용 파일과 한국어 커밋 메시지가 없는지 확인한다.
- 강제층: 해당없음(이 저장소의 자동화 동작을 바꾸지 않는다. PR 관례 준수는 위 수동 확인으로만 지킨다).

# wowwork: WowVision 한국어화 작업 저장소

작업 대상은 복제 저장소 3개다(`../wowvision-ko/vision-locale`, `../wowvision-ko/wowvision-installer`, `../wowvision-ko/WowVision`). 한국어 작업은 `ko` 브랜치(vision-locale은 `main`)에 둔다. 이유는 `docs/builds.md` `## 원본 워크플로 주의`.

## 원본에 PR 내기 [필수]

- 위 복제 저장소는 GitHub 포크가 아니라서 원본에 PR을 열 수 없다. PR용 공개 포크는 `dnz3d4c/vision-locale-pr`, `dnz3d4c/WowVision-pr`이고, 로컬 복제본의 remote 이름은 `fork`다(2026-11-07).
- PR 브랜치는 `upstream/main`에서 새로 딴다. `ko` 이력(한국어 커밋, 포크 전용 변경)을 섞지 않는다. 원본 관례: 영어 커밋 `영역: 내용`, 로케일 PR과 코드 PR은 같은 브랜치 이름으로 짝을 짓고, 동작을 바꾸면 en·de 설명서를 함께 고친다.
- PR은 `gh api repos/wow-vision/<저장소>/pulls -f head=dnz3d4c:<브랜치> -f head_repo=<포크 이름> -f base=main ...`로 연다. `gh pr create --head`는 같은 원본의 저장소가 계정에 둘이라 실패한다.
- 계획과 진행 상황: `plans/active/upstream-korean.md`.

### PR이 병합된 뒤

1. 세션 시작 훅(`.claude/settings.json`)이 `tools/pr_cleanup.py --hook`을 실행해서, 병합된 PR의 머리 커밋에 포함된 브랜치를 fork·origin·로컬에서 지운다. 새로 병합된 PR이 있으면 `[PR 정리] 병합됨:` 줄로 알린다(2026-11-09 사용자 결정: 묻지 않고 지운다). 세션 도중에는 `uv run python -m tools.pr_cleanup`을 묻지 않고 실행한다. `남김:` 줄(병합 없이 닫힘, 병합 뒤 새 커밋)은 사용자에게 보고하고 확인을 받는다. 이 도구가 지우지 않은 브랜치를 지울 때는 지금처럼 확인을 받는다.
2. vision-locale `main`과 WowVision `ko`에 원본 main을 병합하고 원본 `luajit tools/headless-tests.lua`를 돌린다. 그 전에 WowVision에서 `git submodule update --init`과 `luajit tools/wownav-pack.lua`를 실행한다. 테스트는 git 밖의 생성물 `mapdata/WowNavPacked/`를 읽어서, 묶음이 낡으면 WowNav 경로 테스트가 실패한다(2026-11-14 V1.0.3: 7건 실패, 다시 묶은 뒤 1016개 통과). luajit이 결과 없이 세그폴트(종료 코드 139)로 끝나면 다시 돌린다(같은 날 세 번 중 두 번).
3. `uv run python -m tools.sync_locale`로 새 키를 찾아 `docs/review-process.md` 절차로 번역한다. 설명서가 바뀌었으면 설명서도 따라간다.
4. payload, 설치 프로그램, 설명서 배포: `docs/builds.md`.
5. 계획서 현황판을 업데이트한다.

## WoW Login Tool [필수]

로그인 툴은 네 번째 복제 저장소 `../wowvision-ko/Sku-WoW-Addon-TBC`(원본 `Sku75/Sku-WoW-Addon-TBC`의 `logintool/`, sparse checkout)의 `ko` 브랜치에서 관리한다. 이 저장소에는 **원본 규약을 그대로 적용한다**(2026-11-07 사용자 결정): 원본 `dev/FOREVER-PRS.md`의 규칙. 커밋은 영어 `logintool ...: 변경 내용`, 게임에서 확인하지 않은 커밋은 끝에 `(UNTESTED)`, 모든 클라이언트에 영향을 주는 수정은 별도 커밋에 `(all clients)`, 주제와 무관한 이름 변경·정리 금지, 코드 주석은 영어, 원본 파일의 BOM·줄 끝 유지. 큰 주제는 PR 전에 이슈로 관리자와 먼저 상의한다.

- 설치 프로그램 배포: `uv run python -m tools.installer_loc payload`가 이 저장소 ko 브랜치로 `koLoginTool.zip`을 만들고, 설치 프로그램이 원본 설치 뒤 덮어쓴다(`docs/builds.md`). ko 브랜치를 고치면 payload와 설치 프로그램을 다시 만든다.
- 테스트 실행 폴더는 `WoW Login Tool Korean/`(git 제외)이다. 브랜치를 바꾸면 `v2/`, `data/*.ini`, `data/localization/`, 다시 빌드한 `helper/SkuLoginSense.exe`를 이 폴더에 복사한다. `data/settings.ini`는 사용자 설정이라 덮지 않는다.
- 2026-11-07 이전 작업본(4.1 기반, `T()`를 `TranslateText()`로 바꾼 판)은 `WoW Login Tool Korean/_reset-backup-20261107/pre-4.2/`에 있다.

## 원본 기능을 빼지 않는다 [필수]

한국어판은 원본에 한국어를 **더한** 것이다. 원본 사용자가 할 수 있는 일은 한국어 사용자도 할 수 있어야 한다.

- 사용자에게 주는 안내(테스터 안내, README, 설명)는 **원본 문서의 절차에서 출발해** 쓴다. "한국어에서 달라진 점"만 적지 않는다. 원본에 있는 선택 기능과 경로는 모두 옮기고, 뺄 때는 그 이유를 안내에 적는다.
- 근거: 2026-11-06, 테스터 안내(`docs/tester-guide.md`)가 "평소처럼 설치합니다"라고만 해서 NVDA 음성 브리지를 설치하는 방법이 빠졌다. 원본 설명서 `getting-started/installer.md`는 그 방법을 적고 있었다. 실행 파일에는 기능이 있었지만 사용자는 찾을 수 없었다.
- 기계 검사: `tests/test_tester_guide.py`가 설치 프로그램 구성 요소 페이지의 모든 옵션 이름이 안내에 있는지 확인한다. 옵션 목록은 `ComponentsForm.cs`에서 뽑으므로, 원본에 옵션이 새로 생기면 검사가 실패한다.
- 코드: 원본 태그와 `ko` 브랜치의 차이에서 지운 줄(`git diff <원본 태그> ko`의 `-` 줄)은 모두 이유가 있어야 한다. 설치 프로그램을 빌드하기 전에 확인한다.

## 도구를 늘리지 않는다 [필수]

사고가 나면 그 일의 **원래 주인 도구**를 고친다. 새 도구, 새 검사, 새 복사본(상수·목록·프롬프트 문단)은 기존 것이 맡을 수 없는 이유를 커밋 메시지에 적을 때만 만든다.

- 근거: 2026-11-08 점검. 재발 방지 장치 12개가 전부 덧붙인 것이었고 합치거나 지운 것은 없었다. 설명서 인용 맞추기를 `sync_locale` 밖의 도구로 만들어 실행 순서 의존과 누락 경로가 생겼다.
- 재발 방지 기록에는 더한 것과 함께 **합치거나 지운 것**을 적는다.
- 같은 정보는 한 곳에만 둔다. 다른 곳에는 그 위치를 가리키는 한 줄만 쓴다.

## 번역을 고칠 때 [필수]

- **되돌린 번역은 `docs/glossary.tsv`에 넣는다.** 기록만으로는 다시 제안되는 것을 막지 못했다("카메라 따라가기 방식", 2026-11-06). 용어집은 `uv run pytest -q`가 모든 번역에 적용한다.
- **게임 공식 용어는 영어가 같아야 근거다.** `cache/gs_enUS.csv`의 같은 ID 영어가 원문 구절과 같은 말인지 확인한다. "Roll Bonus"에 "Bonus Loot"의 번역 "추가 전리품"을 쓴 것이 반영됐다가 되돌려졌다.
- **koKR은 `tools.sync_locale`로만 고친다.** 설명서 인용도 같은 실행에서 따라 바뀐다. 손으로 일괄 치환하지 않는다(같은 값을 쓰는 다른 키를 잘못 바꾼 사례가 있다).
- **많은 항목에 걸리는 방침은 대량 작업 전에 사용자 결정을 받는다**(`docs/review-process.md` 원칙 7).
- 번역으로 고칠 수 없는 것(코드에 박힌 영어, 설명서와 동작의 차이)은 `docs/upstream-report.md`에 모은다.

## 절차 문서

| 문서 | 내용 |
|------|------|
| `docs/review-process.md` | 번역 품질 평가 절차 (Claude + GPT, 교차 판정) |
| `docs/translation-guide.md` | 번역 규칙 |
| `docs/decisions.tsv` | 사용자 결정 |
| `docs/glossary.tsv` | 확정 용어 |
| `docs/builds.md` | 테스터 배포 빌드와 다시 만드는 법, 설명서 배포 |
| `docs/archive/` | 끝난 계획과 진행 기록(1.0 최종 검수, 설명서 번역 계획). 현행 규칙은 위 문서로 옮겼다 |

# wowwork: WowVision 한국어판 작업 저장소

이 저장소에는 번역 도구(`tools/`), 규칙과 절차(`docs/`), 작업 기록(`reviews/`, `docs/archive/`)이 있다. 번역 파일과 프로그램은 옆 폴더 `../wowvision-ko/`의 저장소에 있다.

## 저장소 구성

| 폴더(`../wowvision-ko/` 아래) | 작업 브랜치 | 내용 |
|------|------|------|
| `vision-locale` | `main` | koKR 번역 파일 |
| `WowVision` | `ko` | 한국어 설명서 |
| `wowvision-installer` | `ko` | 한국어 설치 프로그램. 서브모듈 `korean`(wowvision-korean 저장소, `main` 브랜치) 포함 |
| `Sku-WoW-Addon-TBC` | `ko` | WoW Login Tool 한국어판. `installer/`와 `logintool/`만 sparse checkout |

- 각 저장소의 `origin`은 원본의 포크이고, `upstream`은 원본(`wow-vision`, `Sku75`)이다.
- 한국어 작업은 위 작업 브랜치에만 커밋한다. 포크의 `main`에 push하면 원본 워크플로가 포크에서 실행된다(`docs/builds.md` `## 원본 워크플로 주의`). wowvision-installer의 `main`에는 push하지 않는다. WowVision의 `main`에 push해야 할 때는 `docs/builds.md` `## 한국어 설명서 배포`의 절차(설명서 워크플로를 끄고 push)를 따른다.
- 한국어판에만 있는 새 기능은 서브모듈 `korean`에 둔다. 원본 파일에는 호출 줄과 csproj 포함 줄만 더한다. 구성은 `../wowvision-ko/wowvision-installer/korean/README.md`에 있다.
- vision-locale, WowVision, wowvision-installer의 기준은 원본 릴리스다. 설치 프로그램은 원본처럼 안정판을 미리 선택하고, 원본을 따라갈 때는 릴리스 태그를 병합한다. 로그인 툴은 원본 `main`을 기준으로 한다(아래 `## WoW Login Tool`). 원본과 다르게 둔 기본값은 NVDA 음성 브리지 기본 설치 하나다(`docs/builds.md`).

## 원본 새 릴리스 따라가기

1. 병합, 원본 테스트, 새 문자열 번역: `docs/translation-guide.md` `## upstream 업데이트 절차`
2. 영어 설명서가 변경된 경우: `docs/translation-guide.md` `### 원본이 바뀌었을 때`
3. payload, 설치 프로그램, 테스터 파일, 설명서 배포: `docs/builds.md` `## 다시 만드는 법`, `## 한국어 설명서 배포`
4. `plans/active/upstream-korean.md` 현황판과 `docs/builds.md` 현재 배포 표를 업데이트한다.

## 원본에 PR 내기

- PR 브랜치는 `upstream/main`에서 새로 딴다. `ko` 이력(한국어 커밋, 포크에만 있는 변경)을 섞지 않는다.
- 원본 관례를 따른다: 커밋 제목은 영어 `영역: 내용`, 로케일 PR과 코드 PR은 같은 브랜치 이름으로 짝을 짓고, 동작을 바꾸면 en·de 설명서를 함께 고친다.
- PR은 `gh api repos/wow-vision/<저장소>/pulls -f head=<계정>:<브랜치> -f head_repo=<저장소> -f base=main -f title=<제목> -f body=<본문>`으로 연다.
- 계획과 진행 상황은 `plans/active/upstream-korean.md`에 있다.
- PR이 병합되면 `uv run python -m tools.pr_cleanup`을 묻지 않고 실행해 병합된 브랜치를 `origin`과 로컬에서 지운다. 출력에 `남김:` 줄(병합 없이 닫힘, 병합 뒤 새 커밋)이 있으면 사용자에게 보고하고 확인을 받는다. 이 도구가 지우지 않은 브랜치를 지울 때도 확인을 받는다. 마지막으로 `plans/active/upstream-korean.md` 현황판을 업데이트한다.

## WoW Login Tool

- 로그인 툴 저장소에는 원본 규약(`dev/FOREVER-PRS.md`)을 그대로 적용한다. 이 파일은 sparse checkout 밖에 있으므로 `git -C ../wowvision-ko/Sku-WoW-Addon-TBC show HEAD:dev/FOREVER-PRS.md`로 읽는다.
  - 커밋 제목은 영어 `logintool ...: 변경 내용`
  - 게임에서 확인하지 않은 커밋은 끝에 `(UNTESTED)`
  - 모든 클라이언트에 영향을 주는 수정은 별도 커밋으로 하고 끝에 `(all clients)`
  - 주제와 무관한 이름 변경과 정리를 하지 않는다
  - 코드 주석은 영어로 쓰고, 원본 파일의 BOM과 줄 끝을 유지한다
  - 큰 주제는 PR 전에 이슈로 원본 관리자와 먼저 상의한다
- `ko` 브랜치를 고치면 `uv run python -m tools.installer_loc payload`로 payload(`koLoginTool.zip`)를 다시 만들고 설치 프로그램을 다시 빌드한다.
- 게임에서 시험하는 폴더는 `WoW Login Tool Korean/`(git 제외)이다. 브랜치를 변경하면 `v2/`, `data/*.ini`, `data/localization/`, 다시 빌드한 `helper/SkuLoginSense.exe`를 이 폴더에 복사한다. `data/settings.ini`는 사용자 설정이라 덮지 않는다.

## 원본 기능 유지

원본 사용자가 할 수 있는 일은 한국어 사용자도 할 수 있어야 한다.

- 사용자에게 주는 안내(테스터 안내, README, 설명)는 원본 문서의 절차에서 출발해 쓴다. 한국어판에서 달라진 점만 적지 않는다. 원본의 선택 기능과 경로를 모두 옮긴다. 옮기지 않은 내용이 있으면 그 이유를 안내에 적는다.
- `tests/test_tester_guide.py`가 설치 프로그램 구성 요소 페이지의 모든 옵션 이름이 테스터 안내에 있는지 검사한다. 옵션 목록은 `ComponentsForm.cs`에서 읽으므로 원본에 옵션이 생기면 이 검사가 실패한다.
- 설치 프로그램을 빌드하기 전에 `git diff <원본 태그> ko`에서 지운 줄(`-` 줄)을 확인한다. 지운 줄은 모두 이유가 있어야 한다.

## 도구를 늘리지 않는다

- 문제가 생기면 그 작업을 담당하는 기존 도구를 고친다. 새 도구, 새 검사, 새 복사본(상수, 목록, 프롬프트 문단)은 기존 도구로 처리할 수 없을 때만 만들고, 그 이유를 커밋 메시지에 적는다.
- 재발 방지 조치를 커밋할 때는 추가한 것뿐 아니라 통합하거나 삭제한 것도 커밋 메시지에 적는다.
- 같은 정보는 한 곳에만 둔다. 다른 곳에는 그 위치를 가리키는 한 줄만 쓴다.

## 번역을 고칠 때

- koKR은 `tools.sync_locale`로만 고친다. 같은 실행이 설명서의 화면 문구 인용도 새 값에 맞춘다. 손으로 일괄 치환하지 않는다. 같은 값을 사용하는 다른 키까지 바뀐다.
- 되돌린 번역은 `docs/glossary.tsv`에 넣는다. 기록만으로는 같은 번역이 다시 제안되는 것을 막지 못한다. `uv run pytest -q`가 용어집을 모든 번역에 적용한다.
- 게임 공식 용어를 근거로 삼으려면 `cache/gs_enUS.csv`에서 같은 ID의 영어가 원문 구절과 같아야 한다. 예: "Roll Bonus"에 "Bonus Loot"의 공식 번역 "추가 전리품"을 사용하지 않는다.
- 여러 항목에 걸리는 방침(문체, 여러 곳에 쓰인 용어)은 대량 작업 전에 사용자 결정을 받고, `docs/decisions.tsv`에 날짜와 함께 적는다. 이미 기록된 결정은 다시 정하지 않는다.
- 작업 중 남긴 의문은 검수에서 지적이 없어도 사용자에게 넘긴다.
- 사용자가 번역을 지적하면 그 문장만 고치지 않는다. 같은 유형(낱말, 관용구 직역, 지시어, 성분 누락)을 전체에서 찾아 세고, 그 유형에 대한 결정을 한 번 받은 뒤 용어집이나 번역 지침에 올린다.
- 번역으로 고칠 수 없는 것(코드에 박힌 영어, 설명서와 동작이 다른 곳)은 `docs/upstream-report.md`에 모은다.
- 번역 작업의 순서와 확인 항목은 스킬 `kokr-translation`에 있다.

## 검증

- 커밋 전에 `uv run pytest -q`와 `uv run ruff check tools tests`가 통과해야 한다.
- 설치 프로그램을 고치면 wowvision-installer 폴더에서 `.\build.ps1 -RunTests`가 통과해야 한다(`docs/builds.md` `## 다시 만드는 법`).

## 문서

| 문서 | 내용 |
|------|------|
| `README.md` | 처음 내려받기, 설치할 프로그램, 넘겨받는 순서 |
| `docs/translation-guide.md` | 번역 규칙, 원본 새 릴리스 따라가기 명령 |
| `docs/builds.md` | 설치 프로그램 빌드, 테스터 배포, 설명서 배포, 배포 기록 |
| `docs/glossary.tsv` | 확정 용어 |
| `docs/decisions.tsv` | 사용자 결정과 이유 |
| `docs/upstream-report.md` | 원본에 알릴 문제 |
| `docs/archive/review-pipeline/review-process.md` | 1.0 번역 검수 방식의 기록 |
| `reviews/`, `docs/archive/` | 끝난 작업의 기록. 현행 규칙은 위 문서에 있다 |

# wowwork

WowVision 한국어판을 만드는 작업 저장소입니다. 번역 도구, 검수 기록, 빌드 절차를 둡니다. 번역과 코드는 아래 저장소에 있습니다.

## 저장소

| 저장소 | 작업 브랜치 | 내용 |
|--------|-------------|------|
| [dnz3d4c/vision-locale](https://github.com/dnz3d4c/vision-locale) | `main` | koKR 번역 파일. 원본 `wow-vision/vision-locale`의 포크 |
| [dnz3d4c/WowVision](https://github.com/dnz3d4c/WowVision) | `ko` | 한국어 설명서. 원본 `wow-vision/WowVision`의 포크. 설명서는 이 저장소의 GitHub Pages로 배포 |
| [dnz3d4c/wowvision-installer](https://github.com/dnz3d4c/wowvision-installer) | `ko` | 한국어 설치 프로그램. 원본 `wow-vision/wowvision-installer`의 포크 |
| [dnz3d4c/wowvision-korean](https://github.com/dnz3d4c/wowvision-korean) | `main` | 한국어판 전용 기능(센스 리더 연결). 설치 프로그램의 서브모듈 `korean` |
| [dnz3d4c/Sku-WoW-Addon-TBC](https://github.com/dnz3d4c/Sku-WoW-Addon-TBC) | `ko` | WoW Login Tool 한국어판. 원본 `Sku75/Sku-WoW-Addon-TBC`의 포크 |

`WowVision-old`, `vision-locale-old`, `wowvision-installer-old`는 포크로 옮기기 전의 복제본입니다. 보관 처리되어 읽기만 할 수 있습니다.

이 문서에서 "원본"은 한국어판의 바탕이 되는 원래 프로젝트(`wow-vision`, `Sku75`)를 뜻합니다.

## 넘겨받는 순서

1번은 저장소를 넘겨받은 직후에 합니다. 2번은 `## 설치 환경`의 GitHub CLI를 설치하고 로그인한 뒤에 합니다. 3번부터는 `## 처음 받기`까지 끝낸 뒤에 합니다.

### 1. 저장소 이전

GitHub의 Transfer ownership으로 저장소 6개를 넘겨받습니다. 위 표의 5개와 이 저장소(wowwork)입니다. `-old` 저장소 3개는 기록용이라 넘기지 않아도 됩니다.

받는 계정에 다음 저장소가 있으면 이전되지 않습니다. 그런 저장소는 먼저 지우거나 이름을 변경합니다.

- 넘겨받을 저장소와 이름이 같은 저장소
- 원본 `wow-vision/vision-locale`, `wow-vision/WowVision`, `wow-vision/wowvision-installer`, `Sku75/Sku-WoW-Addon-TBC` 중 하나의 포크

### 2. 설명서 사이트 켜기

지금 WowVision 포크는 워크플로가 꺼져 있습니다. 저장소의 Actions 탭에서 워크플로를 켜는 버튼을 누른 뒤, 다음을 실행합니다. 앞의 두 줄은 한국어판에 필요 없는 원본 워크플로(베타 빌드, 릴리스)를 끄고, 마지막 줄은 한국어 설명서를 배포합니다.

    gh workflow disable beta.yml -R <계정>/WowVision
    gh workflow disable release.yml -R <계정>/WowVision
    gh workflow run docs.yml -R <계정>/WowVision --ref ko

설명서 주소는 `https://<계정>.github.io/WowVision/user/ko/getting-started/introduction.html`입니다. 이전 뒤 Pages 주소는 리디렉션되지 않으므로, 이전 관리자 계정의 옛 주소는 더는 열리지 않습니다.

`docs.yml`은 켜 둡니다. 다만 원본 설명서 워크플로이기도 해서, 포크의 `main`에 `docs/`가 바뀐 커밋이 push되면 영어판으로 사이트를 덮어씁니다. 포크의 `main`은 원본에 맞출 필요가 없습니다. 원본에 내는 PR 브랜치는 `upstream/main`에서 따기 때문입니다. 그래도 맞출 때는 `docs/builds.md` `## 한국어 설명서 배포`의 절차를 따릅니다.

### 3. 계정 이름 바꾸기

저장소 안에 이전 계정 이름 `dnz3d4c`가 적힌 곳을 새 계정으로 변경합니다. 각 저장소에서 `git grep -n dnz3d4c`로 찾습니다. 지금 쓰는 안내와 명령이 있는 곳은 다음과 같습니다.

- 이 README의 저장소 링크
- `CLAUDE.md`: 저장소 이름, PR 명령, 로그인 툴 포크 이름
- `docs/tester-guide.md`: 설명서 주소
- `docs/builds.md` `## 한국어 설명서 배포`: 설명서 주소와 배포 명령
- `docs/translation-guide.md`: 첫 단락의 포크 이름
- `plans/active/upstream-korean.md`: PR 명령
- wowvision-installer `ko` 브랜치의 `.gitmodules`: 서브모듈 `korean`의 주소. 고친 뒤 `git submodule sync`를 실행하고 커밋합니다.

코드 주석(`tools/*.py`, wowvision-installer의 `*.csproj`)에 있는 이름은 동작에 영향이 없습니다. `reviews/`, `docs/archive/`, `docs/decisions.tsv`, `docs/builds.md`의 지난 배포 기록처럼 당시 사실을 적은 기록은 그대로 둡니다.

### 4. 원본 V1.0.4 따라가기

2026-11-19 기준 원본 WowVision의 안정판은 V1.0.4이고, 한국어판(koKR, 설명서)은 V1.0.3 기준입니다. 병합할 대상은 다음과 같습니다.

- WowVision `ko`: 원본 태그 `V1.0.4`
- vision-locale `main`: 원본 커밋 `3172cd5`(V1.0.4의 `locale` 서브모듈이 가리키는 커밋)

명령은 `docs/translation-guide.md` `## upstream 업데이트 절차`에 있고, 전체 순서는 `CLAUDE.md` `### PR이 병합된 뒤` 2~5단계입니다. 원본 병합과 테스트, 새 문자열 번역, payload(설치 프로그램에 넣는 한국어 파일 묶음)와 설치 프로그램 빌드, 설명서 배포, 계획서 현황판 업데이트 순서입니다. 영어 설명서가 바뀐 쪽을 따라가는 순서는 `docs/translation-guide.md` `### 원본이 바뀌었을 때`에 있습니다.

1.0 때는 번역마다 Claude와 GPT로 교차 검수했습니다(`docs/review-process.md`). 그 도구는 기록으로만 남아 있으니, 검수 방식은 넘겨받는 사람이 정합니다. 어떤 방식이든 `uv run pytest -q`(확정 용어집 검사 포함)는 통과해야 합니다.

### 5. 로그인 툴 기준 맞추기

로그인 툴 `ko` 브랜치는 원본 `main`의 4.2 개발 중 커밋(`6c64791`) 위에 있습니다. 2026-11-07에 원본에 PR을 내려고 그 위로 정리했습니다. 원본 이슈는 Sku75/Sku-WoW-Addon-TBC#37이고, 인계 시점까지 답변이 없습니다.

원본은 2026-11-18에 4.2를 릴리스했습니다. 설치 프로그램은 이 4.2 릴리스를 설치한 뒤 `ko` 브랜치의 파일을 덮어씁니다. 그런데 `ko`에는 4.2 릴리스의 마지막 커밋 `f621e25`(Forever 클라이언트 강제 종료 수정, `logintool/v2/includes/forever.ahk`)가 없습니다. 그래서 지금 설치 프로그램은 그 수정을 되돌리는 셈입니다. `ko`에 원본 `main`을 병합하고 payload와 설치 프로그램을 다시 만듭니다(`docs/builds.md`). 4.1 기반의 옛 작업본은 아래 6번에 있습니다.

### 6. git 밖에 있는 파일 받기

아래 파일은 저장소에 없어서 이전 관리자에게 따로 받아야 합니다. 받지 못해도 작업은 할 수 있습니다.

- `WoW Login Tool Korean/_reset-backup-20261107/pre-4.2/`(wowwork 안): 로그인 툴 4.1 기반의 옛 한국어 작업본입니다.
- `wowvision-ko/tester/`: 마지막으로 테스터에게 배포한 파일(`WowVisionInstaller.exe`, `설치_안내.txt`, `tester.zip`)입니다. `docs/builds.md` `## 다시 만드는 법`으로 다시 만들 수 있습니다.
- `WoW Login Tool Korean/`의 나머지: 로그인 툴을 게임에서 시험하는 실행 폴더입니다. 원본 로그인 툴 릴리스를 풀고 그 위에 `ko` 브랜치의 파일을 복사해 만듭니다. 복사할 파일은 `CLAUDE.md` `## WoW Login Tool`에 있습니다.

## 설치 환경

Windows 기준입니다. 필요한 때를 기준으로 구분했습니다.

| 도구 | 필요한 때 | 용도 |
|------|-----------|------|
| Git, [GitHub CLI](https://cli.github.com/)(`gh`) | 항상 | 복제, 원본 PR, 설명서 배포, PR 브랜치 정리. 설치 뒤 `gh auth login`으로 로그인합니다 |
| [uv](https://docs.astral.sh/uv/)와 Python 3.14 | 항상 | 이 저장소의 도구와 테스트 |
| LuaJIT | 원본 병합 | WowVision 자체 테스트(`luajit tools/headless-tests.lua`). 공식 사이트는 소스만 배포하므로 Windows에서는 scoop(`scoop install luajit`) 같은 패키지 관리자로 설치합니다 |
| .NET SDK, PowerShell 7 | payload와 설치 프로그램 빌드 | 설치 프로그램 빌드와 자체 검사(`.\build.ps1 -RunTests`), 로그인 툴 도우미 빌드. `dotnet`이 PATH에 있어야 합니다 |
| Visual Studio 2022 Build Tools(C++) | payload와 설치 프로그램 빌드 | 센스 리더 연결 DLL 빌드(`korean\sense-reader-bridge\build.bat test`). payload를 만들 때 함께 실행됩니다 |
| 7-Zip | 테스터 배포 | 테스터 배포 파일 `tester.zip` |
| Vocalizer Expressive 음성 Yuna(SAPI), ffmpeg | 음성 팩 변경 | 한국어 음성 팩 녹음과 길이 측정(`tools/voice_pack.py`) |
| AutoHotkey v2 | 로그인 툴 시험 | 로그인 툴 화면 읽기 시험(`tools/logintool_bench`) |
| 센스 리더 | 센스 리더 연결 확인 | 센스 리더로 말하는지 실제로 확인할 때만 |

번역 검수 기록(`docs/review-process.md`, `reviews/`)에 나오는 Claude Code와 Codex CLI는 이전 관리자가 1.0 검수에 사용한 도구입니다. 검수 스크립트는 `docs/archive/review-pipeline/`에 기록으로만 남아 있고, 위 표의 어느 작업에도 필요하지 않습니다.

## 처음 받기

이 저장소와 복제본을 같은 상위 폴더에 둡니다. 도구는 이 저장소 옆의 `../wowvision-ko/`에서 복제본을 찾습니다.

    games/
      wowwork/
      wowvision-ko/
        vision-locale/            main
        WowVision/                ko, 서브모듈(audio, locale, mapdata) 포함. 약 530MB
        wowvision-installer/      ko, 서브모듈 korean 포함
        Sku-WoW-Addon-TBC/        ko, installer/와 logintool/만 sparse checkout
        tester/                   테스터 배포 파일(git 밖)

`wowvision-ko` 폴더에서 다음을 실행합니다. `<계정>`은 저장소를 넘겨받은 계정입니다.

    git clone -b main https://github.com/<계정>/vision-locale.git
    git clone -b ko --recurse-submodules https://github.com/<계정>/WowVision.git
    git clone -b ko --recurse-submodules https://github.com/<계정>/wowvision-installer.git
    git clone -b ko --filter=blob:none --sparse https://github.com/<계정>/Sku-WoW-Addon-TBC.git
    git -C Sku-WoW-Addon-TBC sparse-checkout set installer logintool
    git -C vision-locale remote add upstream https://github.com/wow-vision/vision-locale.git
    git -C WowVision remote add upstream https://github.com/wow-vision/WowVision.git
    git -C wowvision-installer remote add upstream https://github.com/wow-vision/wowvision-installer.git
    git -C Sku-WoW-Addon-TBC remote add upstream https://github.com/Sku75/Sku-WoW-Addon-TBC.git
    git -C vision-locale fetch upstream
    git -C WowVision fetch upstream --tags
    git -C wowvision-installer fetch upstream
    git -C Sku-WoW-Addon-TBC fetch upstream

WowVision 자체 테스트를 돌리기 전에는 WowVision 폴더에서 `luajit tools/wownav-pack.lua`를 실행합니다. 이유는 `CLAUDE.md` `### PR이 병합된 뒤` 2단계에 있습니다.

마지막으로 이 저장소(wowwork)에서 다음을 실행합니다. 개발 의존성(pytest, ruff, mypy)을 설치하고, 게임 용어 캐시를 만든 뒤, 테스트를 돌립니다. 게임 용어 캐시(`cache/`)는 git에 넣지 않는 폴더입니다. `tools.game_terms`가 wago.tools에서 게임 공식 문자열(영어, 한국어)을 내려받아 만듭니다.

    uv sync
    uv run python -m tools.game_terms
    uv run pytest -q

2026-11-19에 이 순서대로 새로 받아서 테스트 232개가 모두 통과하는 것을 확인했습니다.

## 문서

| 문서 | 내용 |
|------|------|
| `CLAUDE.md` | 작업 규칙 전체(원본 PR, 병합 뒤 절차, 로그인 툴 규약, 번역 수정 규칙). AI 도구(Claude Code)에 주는 지시문 형식이지만 사람이 읽는 규칙으로도 그대로 씁니다. 문서 속 "사용자"는 관리자를 뜻합니다 |
| `docs/translation-guide.md` | 번역 규칙 |
| `docs/glossary.tsv`, `docs/decisions.tsv` | 확정 용어와 결정 기록 |
| `docs/builds.md` | 설치 프로그램 빌드, 테스터 배포, 설명서 배포 |
| `docs/tester-guide.md` | 테스터 설치 안내. 배포할 때 `설치_안내.txt`로 복사합니다 |
| `docs/upstream-report.md` | 번역으로 고칠 수 없어 원본에 알릴 문제 |
| `plans/active/upstream-korean.md` | 원본에 한국어를 보내는 계획과 진행 상황 |
| `docs/review-process.md` | 1.0 때의 번역 검수 방식 기록 |
| `reviews/README.md` | 검수 회차 목록과 대표 사례, 지운 검수 파일을 꺼내는 법 |

## 자주 하는 작업

| 작업 | 명령 또는 문서 |
|------|----------------|
| 원본에 생긴 새 문자열 찾기와 번역 반영 | `uv run python -m tools.sync_locale`. 번역이 없는 키는 `cache/missing.tsv`에 모이므로, ko 열을 채운 뒤 `uv run python -m tools.sync_locale cache/missing.tsv`로 반영합니다 |
| koKR 번역 수정 | `tools.sync_locale`로만 수정(`CLAUDE.md` `## 번역을 고칠 때`) |
| 영어 설명서에서 바뀐 곳 보기 | `uv run python -m tools.manual diff <상대경로>`. 상대경로는 WowVision의 `docs/src/user/en` 기준입니다 |
| 설치 프로그램 payload 다시 만들기 | `uv run python -m tools.installer_loc payload` |
| 설치 프로그램 빌드부터 테스터 배포까지 | `docs/builds.md` `## 다시 만드는 법` |
| 병합된 원본 PR의 브랜치 정리 | `uv run python -m tools.pr_cleanup` |

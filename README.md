# wowwork

WowVision 한국어판을 만드는 작업 저장소입니다. 번역 도구, 검수 기록, 빌드 절차를 둡니다. 번역과 코드는 아래 저장소에 있습니다.

## 저장소

| 저장소 | 브랜치 | 내용 |
|--------|--------|------|
| [dnz3d4c/vision-locale](https://github.com/dnz3d4c/vision-locale) | `main` | koKR 번역 파일. 원본 `wow-vision/vision-locale`의 포크 |
| [dnz3d4c/WowVision](https://github.com/dnz3d4c/WowVision) | `ko` | 한국어 설명서와 애드온 수정. 원본 `wow-vision/WowVision`의 포크. 설명서는 이 저장소의 GitHub Pages로 배포 |
| [dnz3d4c/wowvision-installer](https://github.com/dnz3d4c/wowvision-installer) | `ko` | 한국어 설치 프로그램. 원본 `wow-vision/wowvision-installer`의 포크 |
| [dnz3d4c/wowvision-korean](https://github.com/dnz3d4c/wowvision-korean) | `main` | 한국어판 전용 기능(센스 리더 연결). 설치 프로그램의 서브모듈 `korean` |
| [dnz3d4c/Sku-WoW-Addon-TBC](https://github.com/dnz3d4c/Sku-WoW-Addon-TBC) | `ko` | WoW Login Tool 한국어판. 원본 `Sku75/Sku-WoW-Addon-TBC`의 포크 |

`WowVision-old`, `vision-locale-old`, `wowvision-installer-old`는 포크로 옮기기 전의 복제본입니다. 보관 처리되어 읽기만 할 수 있습니다.

## 넘겨받은 뒤 처음 할 일

1. 저장소 이전: 위 저장소를 GitHub의 Transfer ownership으로 넘겨받습니다. 받는 계정에 같은 이름의 저장소가 있거나, 포크 4개(vision-locale, WowVision, wowvision-installer, Sku-WoW-Addon-TBC)와 같은 원본의 포크가 이미 있으면 이전되지 않습니다. 그런 저장소가 있으면 먼저 지우거나 이름을 변경합니다. 이전 뒤 GitHub Pages 주소는 리디렉션되지 않습니다.
2. 설명서 사이트 켜기: WowVision 포크는 Actions가 꺼진 상태로 넘어갑니다. 저장소의 Actions 탭에서 워크플로 활성화 버튼을 누른 뒤, 원본 main 동기화 때 실행되는 `beta.yml`과 `release.yml`을 끕니다. 그다음 설명서를 배포하고 주소를 확인합니다.

        gh workflow disable beta.yml -R <계정>/WowVision
        gh workflow disable release.yml -R <계정>/WowVision
        gh workflow run docs.yml -R <계정>/WowVision --ref ko

   설명서 주소는 `https://<계정>.github.io/WowVision/user/ko/getting-started/introduction.html`이 됩니다. Pages 설정과 배포 허용 브랜치(ko, main)는 저장소와 함께 넘어갑니다.
3. 주소 업데이트: `docs/tester-guide.md`의 설명서 주소, 이 README의 저장소 링크, `.gitmodules`의 서브모듈 주소(wowvision-installer `ko`)를 새 계정으로 변경합니다.
4. 원본 V1.0.4 따라가기: 2026-11-19 기준 원본 안정판은 V1.0.4이고, 한국어판(koKR, 설명서)은 V1.0.3 기준입니다. `CLAUDE.md` `### PR이 병합된 뒤` 2~5단계(원본 병합, 새 키 번역과 검수, payload와 설치 프로그램, 설명서 배포)로 따라갑니다.
5. 로그인 툴 기준 버전 정하기: 로그인 툴 `ko` 브랜치는 원본 릴리스(4.1)가 아니라 아직 발표되지 않은 원본 `main`(4.2) 위에 있습니다. 원본에 PR을 내려고 2026-11-07에 `main` 위로 정리했기 때문입니다(원본 이슈 Sku75/Sku-WoW-Addon-TBC#37, 인계 시점까지 답변 없음). 설치 프로그램은 원본 4.1 릴리스 위에 이 브랜치의 파일을 덮어쓰므로, 원본 릴리스 기준으로 맞출지 4.2 릴리스를 기다릴지 정합니다. 4.1 기반의 옛 작업본은 `WoW Login Tool Korean/_reset-backup-20261107/pre-4.2/`(git 밖)에 있었습니다.

## 설치 환경

Windows 기준입니다. 모든 작업에 필요한 것과 특정 작업에만 필요한 것을 구분했습니다.

| 도구 | 용도 | 필요한 때 |
|------|------|-----------|
| Git, [GitHub CLI](https://cli.github.com/)(`gh`) | 복제, 원본 PR, 병합된 PR 브랜치 정리(`tools/pr_cleanup.py`) | 항상 |
| [uv](https://docs.astral.sh/uv/)와 Python 3.14 | 이 저장소의 도구와 테스트. `uv sync`로 개발 의존성(pytest, ruff, mypy)을 설치 | 항상 |
| [LuaJIT](https://luajit.org/) | 원본 병합 뒤 WowVision의 `luajit tools/headless-tests.lua` | 원본 병합 |
| .NET SDK, PowerShell 7 | 설치 프로그램 빌드와 자체 검사(`build.ps1 -RunTests`), 로그인 툴 도우미 빌드. `dotnet`이 PATH에 있어야 합니다 | 설치 프로그램 빌드 |
| Visual Studio 2022 Build Tools(C++) | 센스 리더 프록시 빌드(`korean\sense-reader-bridge\build.bat test`). payload를 만들 때 함께 실행됩니다 | 설치 프로그램 빌드 |
| 7-Zip | 테스터 배포 파일 `tester.zip` | 테스터 배포 |
| Vocalizer Expressive 음성 Yuna(SAPI), ffmpeg | 한국어 음성 팩 다시 녹음과 길이 측정(`tools/voice_pack.py`) | 음성 팩 변경 |
| AutoHotkey v2 | 로그인 툴 화면 읽기 시험(`tools/logintool_bench`) | 로그인 툴 시험 |

번역 검수 기록(`docs/review-process.md`, `reviews/`)에 나오는 Claude Code와 Codex CLI는 이전 관리자가 1.0 검수에 사용한 도구입니다. 그 스크립트는 `docs/archive/review-pipeline/`에 기록으로만 남아 있고, 위 표의 어느 작업에도 필요하지 않습니다.

## 처음 받기

이 저장소와 복제본을 같은 상위 폴더에 둡니다. 도구는 이 저장소 옆의 `../wowvision-ko/`에서 복제본을 찾습니다.

    games/
      wowwork/
      wowvision-ko/
        vision-locale/            main
        WowVision/                ko
        wowvision-installer/      ko, 서브모듈 korean 포함
        Sku-WoW-Addon-TBC/        ko, installer/와 logintool/만 sparse checkout
        tester/                   테스터 배포 파일(git 밖)

`wowvision-ko` 폴더에서 다음을 실행합니다. `<계정>`은 저장소를 넘겨받은 계정입니다.

    git clone -b main https://github.com/<계정>/vision-locale.git
    git clone -b ko https://github.com/<계정>/WowVision.git
    git clone -b ko --recurse-submodules https://github.com/<계정>/wowvision-installer.git
    git clone -b ko --filter=blob:none --sparse https://github.com/<계정>/Sku-WoW-Addon-TBC.git
    git -C Sku-WoW-Addon-TBC sparse-checkout set installer logintool
    git -C vision-locale remote add upstream https://github.com/wow-vision/vision-locale.git
    git -C WowVision remote add upstream https://github.com/wow-vision/WowVision.git
    git -C wowvision-installer remote add upstream https://github.com/wow-vision/wowvision-installer.git
    git -C Sku-WoW-Addon-TBC remote add upstream https://github.com/Sku75/Sku-WoW-Addon-TBC.git

WowVision의 테스트를 돌리기 전에 `git submodule update --init`과 `luajit tools/wownav-pack.lua`를 실행합니다(이유는 `CLAUDE.md` `### PR이 병합된 뒤`).

마지막으로 이 저장소에서 개발 의존성을 설치하고 테스트가 통과하는지 확인합니다.

    uv sync
    uv run pytest -q

## 문서

| 문서 | 내용 |
|------|------|
| `CLAUDE.md` | 작업 규칙 전체(원본 PR, 병합 뒤 절차, 로그인 툴 규약) |
| `docs/translation-guide.md` | 번역 규칙 |
| `docs/review-process.md` | 1.0 때의 번역 검수 방식 기록 |
| `reviews/README.md` | 검수 회차 목록과 대표 사례, 지운 원본을 꺼내는 법 |
| `docs/glossary.tsv`, `docs/decisions.tsv` | 확정 용어와 결정 기록 |
| `docs/builds.md` | 설치 프로그램 빌드, 테스터 배포, 설명서 배포 |
| `plans/active/upstream-korean.md` | 원본에 한국어를 보내는 계획과 진행 상황 |

## 자주 하는 작업

| 작업 | 명령 또는 문서 |
|------|----------------|
| 원본에 새 문자열이 생겼을 때 찾기 | `uv run python -m tools.sync_locale` |
| koKR 번역 수정 | `tools.sync_locale`로만 수정(`CLAUDE.md` `## 번역을 고칠 때`) |
| 설치 프로그램 payload 다시 만들기 | `uv run python -m tools.installer_loc payload` |
| 설치 프로그램 빌드부터 테스터 배포까지 | `docs/builds.md` `## 다시 만드는 법` |
| 병합된 원본 PR의 브랜치 정리 | `uv run python -m tools.pr_cleanup` |

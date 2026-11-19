# wowwork

WowVision 한국어판을 만드는 작업 폴더입니다. WowVision은 시각장애인이 World of Warcraft를 화면 낭독기로 플레이하게 돕는 애드온이고, 한국어판은 여기에 한국어 번역, 한국어 설치 프로그램, 한국어 설명서를 더한 것입니다.

이 폴더에는 번역을 돕는 도구, 지금까지의 작업 기록, 설치 프로그램을 만드는 절차가 있습니다. 실제 번역 파일과 프로그램은 아래 `## 함께 넘겨받는 저장소`의 다른 저장소에 있습니다.

## 이 문서에 나오는 말

GitHub와 git에서 쓰는 말이 많이 나옵니다. 화면과 명령에 그대로 나오는 말이라 다른 말로 바꾸지 않고, 여기서 뜻을 풀어 둡니다.

- 저장소: GitHub에 올려 둔 프로젝트 폴더입니다. 파일과 함께, 언제 무엇을 고쳤는지 기록이 남습니다.
- 원본: 한국어판이 바탕으로 삼는 원래 프로젝트입니다. WowVision은 `wow-vision`, 로그인 툴은 `Sku75`가 만듭니다.
- 포크: 원본 저장소를 내 계정으로 복사한 저장소입니다. 원본과 연결이 남아 있어서, 원본에 고친 내용을 보낼 수 있습니다.
- 복제: GitHub의 저장소를 내 컴퓨터로 내려받는 것입니다. 명령은 `git clone`입니다.
- 브랜치: 한 저장소 안에서 따로 관리하는 작업본입니다. 한국어 작업은 `ko` 브랜치에 있습니다(vision-locale만 `main` 브랜치).
- 커밋: 고친 내용을 저장소의 기록에 저장하는 것입니다.
- push: 내 컴퓨터에서 커밋한 내용을 GitHub에 올리는 것입니다.
- 병합: 다른 작업본의 변경을 내 작업본에 합치는 것입니다.
- PR(풀 리퀘스트): 원본 관리자에게 내가 고친 내용을 받아 달라고 보내는 요청입니다.
- 릴리스: 원본이 정식으로 발표한 버전입니다. 각 버전에는 `V1.0.4` 같은 이름표(태그)가 붙습니다.
- 서브모듈: 저장소 안에 다른 저장소를 통째로 끼워 넣은 폴더입니다.
- payload: 한국어 설치 프로그램 안에 넣는 한국어 파일 묶음입니다. 번역을 고치면 payload를 다시 만들어야 설치 프로그램에 반영됩니다.
- Actions: GitHub가 저장소에서 정해진 작업을 자동으로 실행하는 기능입니다. 여기서는 한국어 설명서 사이트를 만드는 데 사용합니다.

## 함께 넘겨받는 저장소

| 저장소 | 들어 있는 것 |
|--------|--------------|
| [dnz3d4c/wowwork](https://github.com/dnz3d4c/wowwork) | 이 폴더. 번역 도구, 작업 기록, 절차 문서 |
| [dnz3d4c/vision-locale](https://github.com/dnz3d4c/vision-locale) | 한국어 번역 파일(koKR). 원본 `wow-vision/vision-locale`의 포크 |
| [dnz3d4c/WowVision](https://github.com/dnz3d4c/WowVision) | 한국어 설명서. 원본 `wow-vision/WowVision`의 포크. 설명서 사이트도 이 저장소에서 만듭니다 |
| [dnz3d4c/wowvision-installer](https://github.com/dnz3d4c/wowvision-installer) | 한국어 설치 프로그램. 원본 `wow-vision/wowvision-installer`의 포크 |
| [dnz3d4c/wowvision-korean](https://github.com/dnz3d4c/wowvision-korean) | 한국어판에만 있는 기능(센스 리더로 말하기). 설치 프로그램 안에 서브모듈로 들어 있습니다 |
| [dnz3d4c/Sku-WoW-Addon-TBC](https://github.com/dnz3d4c/Sku-WoW-Addon-TBC) | WoW Login Tool(로그인 툴) 한국어판. 원본 `Sku75/Sku-WoW-Addon-TBC`의 포크 |

이름이 `-old`로 끝나는 저장소 3개는 포크로 옮기기 전의 옛 저장소입니다. 기록용이라 넘겨받지 않아도 됩니다.

## 넘겨받는 순서

1번은 저장소를 넘겨받으면서 합니다. 2번은 `## 설치할 프로그램`에서 GitHub CLI를 설치한 뒤에 합니다. 3번부터는 `## 처음 내려받기`까지 끝낸 뒤에 합니다.

### 1. 저장소 넘겨받기

이전 관리자가 위 표의 저장소 6개를 하나씩 GitHub의 Transfer ownership 기능으로 넘깁니다. 받는 사람에게 수락 메일이 오면, 메일에 적힌 기한 안에 수락합니다.

받는 계정에 다음 저장소가 있으면 넘겨받을 수 없습니다. 그런 저장소가 있으면 먼저 지우거나 이름을 변경합니다.

- 넘겨받을 저장소와 이름이 같은 저장소
- 같은 원본(`wow-vision/vision-locale`, `wow-vision/WowVision`, `wow-vision/wowvision-installer`, `Sku75/Sku-WoW-Addon-TBC`)의 포크

### 2. 설명서 사이트 켜기

넘겨받은 WowVision 저장소는 Actions가 꺼져 있습니다. 저장소 페이지의 Actions 탭에서 워크플로를 켜는 버튼을 누릅니다. 그다음 PowerShell 창에서 아래 명령을 차례로 실행합니다. `<계정>`은 넘겨받은 GitHub 계정 이름으로 바꿔 입력합니다.

    gh workflow disable beta.yml -R <계정>/WowVision
    gh workflow disable release.yml -R <계정>/WowVision
    gh workflow run docs.yml -R <계정>/WowVision --ref ko

앞의 두 줄은 한국어판에 필요 없는 원본의 자동 작업(베타 빌드, 릴리스)을 끕니다. 마지막 줄은 한국어 설명서 사이트를 만듭니다. 몇 분 뒤 아래 주소에서 설명서가 열리면 됩니다. 이전 관리자 계정의 옛 주소는 더는 열리지 않습니다.

    https://<계정>.github.io/WowVision/user/ko/getting-started/introduction.html

설명서를 만드는 자동 작업(`docs.yml`)은 켜 둡니다. 다만 이 작업은 원본의 것이기도 해서, WowVision 저장소의 `main` 브랜치에 원본의 설명서 변경이 올라오면 사이트를 영어판으로 덮어씁니다. 그러니 `main` 브랜치는 원본에 맞추지 않습니다. 맞춰야 할 때는 `docs/builds.md` `## 한국어 설명서 배포`의 절차를 따릅니다.

### 3. 계정 이름 바꾸기

문서와 설정에 이전 관리자의 계정 이름 `dnz3d4c`가 적혀 있습니다. 아래 파일에서 새 계정 이름으로 변경합니다. 빠진 곳이 있는지는 각 저장소 폴더에서 `git grep -n dnz3d4c`를 실행해 확인합니다.

- 이 README의 저장소 링크
- `CLAUDE.md`: 저장소 이름, PR 명령, 로그인 툴 포크 이름
- `docs/tester-guide.md`: 설명서 주소
- `docs/builds.md` `## 한국어 설명서 배포`: 설명서 주소와 배포 명령
- `docs/translation-guide.md`: 첫 단락의 포크 이름
- `plans/active/upstream-korean.md`: PR 명령
- wowvision-installer 저장소 `ko` 브랜치의 `.gitmodules` 파일: 서브모듈 `korean`의 주소. 고친 뒤 그 폴더에서 `git submodule sync`를 실행하고 커밋합니다.

`tools` 폴더의 파이썬 파일과 설치 프로그램의 `.csproj` 파일에도 이 이름이 있지만, 설명용 주석이라 동작과 관계없습니다. `reviews/`, `docs/archive/`, `docs/decisions.tsv`, `docs/builds.md`의 지난 배포 기록은 당시 사실을 적은 기록이므로 그대로 둡니다.

### 4. 원본 WowVision V1.0.4 따라가기

인계 시점(2026-11-19)에 원본 WowVision의 최신 정식 버전은 V1.0.4이고, 한국어판은 그 전 버전인 V1.0.3 기준입니다. 원본의 새 버전을 가져와 합치고, 새로 생긴 영어 문장을 번역하고, 설치 프로그램과 설명서를 다시 만들어야 합니다.

- 가져올 대상: WowVision 저장소에는 원본의 `V1.0.4`, vision-locale 저장소에는 원본 커밋 `3172cd5`(V1.0.4가 사용하는 번역 파일 버전)
- 명령과 순서: `docs/translation-guide.md` `## upstream 업데이트 절차`
- 설명서에서 영어가 바뀐 쪽을 따라가는 법: `docs/translation-guide.md` `### 원본이 바뀌었을 때`
- 전체 순서(테스트, 설치 프로그램 빌드, 설명서 배포 포함): `CLAUDE.md` `### PR이 병합된 뒤` 2~5단계

1.0 때는 번역마다 Claude와 GPT 두 AI로 교차 검수했습니다(`docs/review-process.md`). 그 도구는 기록으로만 남아 있으므로, 검수 방식은 넘겨받는 사람이 정합니다. 어떤 방식이든 마지막에 `uv run pytest -q`(확정 용어 검사 포함)는 통과해야 합니다.

### 5. 로그인 툴을 원본 4.2에 맞추기

로그인 툴 한국어판(`ko` 브랜치)은 원본이 4.2를 개발하던 도중의 상태(커밋 `6c64791`)를 바탕으로 합니다. 2026-11-07에 원본에 한국어를 보내려고(원본 이슈 Sku75/Sku-WoW-Addon-TBC#37) 그때의 최신 상태에 맞췄기 때문입니다. 이 이슈는 인계 시점까지 답변이 없습니다.

원본은 그 뒤 2026-11-18에 4.2를 정식으로 발표했습니다. 그런데 한국어판에는 4.2의 마지막 수정(커밋 `f621e25`, Forever 클라이언트에서 프로그램이 멈추던 문제 수정)이 빠져 있습니다. 한국어 설치 프로그램은 원본 4.2를 설치한 뒤 한국어판 파일을 덮어쓰기 때문에, 지금은 이 수정을 되돌리는 셈입니다.

할 일은 로그인 툴 저장소의 `ko` 브랜치에 원본 `main` 브랜치를 병합하고, payload와 설치 프로그램을 다시 만드는 것입니다(`docs/builds.md` `## 다시 만드는 법`). 로그인 툴 저장소는 원본의 작업 규칙을 그대로 따릅니다(`CLAUDE.md` `## WoW Login Tool`).

### 6. 저장소에 없는 파일 받기

아래 파일은 저장소에 올라가 있지 않아서, 이전 관리자에게 따로 받아야 합니다. 받지 못해도 작업은 할 수 있습니다.

- `wowwork\WoW Login Tool Korean\_reset-backup-20261107\pre-4.2\`: 로그인 툴 4.1을 바탕으로 했던 옛 한국어 작업본입니다.
- `wowwork\WoW Login Tool Korean\`의 나머지: 로그인 툴을 게임에서 시험하는 폴더입니다. 원본 로그인 툴을 풀고 그 위에 한국어판 파일을 복사해 만듭니다. 복사할 파일은 `CLAUDE.md` `## WoW Login Tool`에 있습니다.
- `wowvision-ko\tester\`: 마지막으로 테스터에게 보낸 파일(`WowVisionInstaller.exe`, `설치_안내.txt`, `tester.zip`)입니다. `docs/builds.md` `## 다시 만드는 법`으로 다시 만들 수 있습니다.

## 설치할 프로그램

모든 프로그램은 PowerShell 창에서 winget 명령으로 설치합니다. 설치를 마치면 PowerShell 창을 닫고 새로 열어야 새 프로그램을 찾습니다.

PowerShell 창을 여는 법: 파일 탐색기에서 원하는 폴더를 연 뒤 Alt+D로 주소 표시줄로 이동하고, `pwsh`를 입력하고 Enter를 누릅니다. 그 폴더에서 PowerShell 7 창이 열립니다. PowerShell 7을 설치하기 전에는 `pwsh` 대신 `powershell`을 입력합니다. 이 문서에서 "X 폴더에서 실행한다"는 X 폴더에서 이렇게 연 창에 입력한다는 뜻입니다.

### 꼭 필요한 것

이것만 있으면 번역 파일을 다루고 테스트를 돌릴 수 있습니다.

    winget install --id Git.Git -e
    winget install --id GitHub.cli -e
    winget install --id astral-sh.uv -e
    winget install --id Microsoft.PowerShell -e

- Git: 저장소를 내려받고, 고친 내용을 기록하고 올립니다.
- GitHub CLI(`gh`): GitHub 작업(설명서 배포, PR)을 명령으로 합니다. 설치한 뒤 새 창에서 `gh auth login`을 실행해 GitHub 계정으로 로그인합니다. 질문이 나오면 차례로 GitHub.com, HTTPS를 고르고, Git 인증 여부에는 Y를 입력하고, 웹 브라우저로 로그인하는 방법을 고릅니다.
- uv: 이 폴더의 파이썬 도구를 실행합니다. 필요한 파이썬 버전(3.14)도 uv가 알아서 설치합니다.
- PowerShell 7: 설치 프로그램을 만드는 스크립트가 사용합니다.

### 하는 일에 따라 필요한 것

| 하는 일 | 설치할 것 | 설치 명령 |
|---------|-----------|-----------|
| 원본 WowVision의 새 버전 가져오기(넘겨받는 순서 4번) | LuaJIT: 원본의 자체 테스트를 돌립니다 | `winget install --id DEVCOM.LuaJIT -e` |
| 설치 프로그램과 payload 만들기 | .NET SDK: 설치 프로그램과 로그인 툴 도우미를 만듭니다 | `winget install --id Microsoft.DotNet.SDK.11 -e` |
| 설치 프로그램과 payload 만들기 | Visual Studio 2022 Build Tools의 C++ 도구: 센스 리더 연결 파일을 만듭니다 | `winget install --id Microsoft.VisualStudio.2022.BuildTools -e --override "--wait --passive --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"` |
| 테스터에게 보낼 파일 묶기 | 7-Zip | `winget install --id 7zip.7zip -e` |
| 한국어 음성 팩 다시 녹음하기 | ffmpeg: 녹음 길이를 잽니다 | `winget install --id Gyan.FFmpeg -e` |
| 한국어 음성 팩 다시 녹음하기 | Vocalizer Expressive 한국어 음성 Yuna | winget으로 설치할 수 없어 따로 구해야 합니다 |
| 로그인 툴이 화면을 제대로 읽는지 시험하기 | AutoHotkey v2 | `winget install --id AutoHotkey.AutoHotkey -e` |
| 센스 리더로 말하는지 실제로 확인하기 | 센스 리더 | winget으로 설치할 수 없어 따로 구해야 합니다 |

작업 기록(`docs/review-process.md`, `reviews/`)에 나오는 Claude Code와 Codex는 이전 관리자가 번역 검수에 쓴 AI 도구입니다. 설치하지 않아도 됩니다.

## 처음 내려받기

### 폴더 배치

작업할 상위 폴더를 하나 정합니다(예: `C:\wowvision`). 그 안에 이 저장소와 `wowvision-ko` 폴더를 나란히 둡니다. 도구는 이 저장소 옆의 `wowvision-ko` 폴더에서 나머지 저장소를 찾으므로, 폴더 이름과 위치를 바꾸면 안 됩니다.

    상위 폴더
      wowwork              이 저장소
      wowvision-ko
        vision-locale        번역 파일
        WowVision            설명서. 끼워 넣은 저장소까지 받으면 약 530MB
        wowvision-installer  설치 프로그램
        Sku-WoW-Addon-TBC    로그인 툴. 필요한 폴더(installer, logintool)만 받습니다
        tester               테스터에게 보낼 파일(저장소에 없음)

### 내려받기 명령

상위 폴더에서 아래 명령을 한 줄씩 실행합니다. `<계정>`은 넘겨받은 GitHub 계정 이름으로 바꿉니다. 첫 묶음은 저장소를 내려받고 각 저장소의 작업 브랜치로 엽니다.

    git clone https://github.com/<계정>/wowwork.git
    mkdir wowvision-ko
    cd wowvision-ko
    git clone -b main https://github.com/<계정>/vision-locale.git
    git clone -b ko --recurse-submodules https://github.com/<계정>/WowVision.git
    git clone -b ko --recurse-submodules https://github.com/<계정>/wowvision-installer.git
    git clone -b ko --filter=blob:none --sparse https://github.com/<계정>/Sku-WoW-Addon-TBC.git
    git -C Sku-WoW-Addon-TBC sparse-checkout set installer logintool

다음 묶음은 각 저장소에 원본의 주소를 `upstream`이라는 이름으로 등록하고, 원본의 최신 기록과 버전 이름표를 가져옵니다. 원본의 새 버전을 가져올 때(넘겨받는 순서 4·5번) 필요합니다.

    git -C vision-locale remote add upstream https://github.com/wow-vision/vision-locale.git
    git -C WowVision remote add upstream https://github.com/wow-vision/WowVision.git
    git -C wowvision-installer remote add upstream https://github.com/wow-vision/wowvision-installer.git
    git -C Sku-WoW-Addon-TBC remote add upstream https://github.com/Sku75/Sku-WoW-Addon-TBC.git
    git -C vision-locale fetch upstream
    git -C WowVision fetch upstream --tags
    git -C wowvision-installer fetch upstream
    git -C Sku-WoW-Addon-TBC fetch upstream

### 확인하기

`wowwork` 폴더로 이동해 아래 명령을 실행합니다. 둘째 줄은 도구에 필요한 파이썬 부품을 설치합니다. 셋째 줄은 번역할 때 참고하는 게임 공식 용어(영어와 한국어)를 wago.tools 사이트에서 내려받아 `cache` 폴더에 둡니다. 넷째 줄은 번역 파일과 문서를 자동으로 검사합니다.

    cd ..\wowwork
    uv sync
    uv run python -m tools.game_terms
    uv run pytest -q

마지막 줄의 결과가 `232 passed`처럼 모두 통과로 끝나면 준비가 끝난 것입니다. 2026-11-19에 이 순서대로 새로 내려받아 232개가 모두 통과하는 것을 확인했습니다.

원본 WowVision의 자체 테스트(`luajit tools/headless-tests.lua`)를 돌릴 때는, 먼저 WowVision 폴더에서 `luajit tools/wownav-pack.lua`를 실행합니다. 이유는 `CLAUDE.md` `### PR이 병합된 뒤` 2단계에 있습니다.

## 문서 안내

| 문서 | 내용 |
|------|------|
| `CLAUDE.md` | 작업 규칙 전체(원본에 PR 보내기, 원본 새 버전 따라가기, 로그인 툴 규칙, 번역 고치는 규칙). AI 도구(Claude Code)에 주는 지시문 형식이지만 사람이 읽는 규칙으로도 그대로 씁니다. 문서 속 "사용자"는 관리자를 뜻합니다 |
| `docs/translation-guide.md` | 번역 규칙과 원본 새 버전을 따라가는 명령 |
| `docs/glossary.tsv` | 확정한 용어. 테스트가 모든 번역에 적용합니다 |
| `docs/decisions.tsv` | 지금까지 내린 결정과 이유 |
| `docs/builds.md` | 설치 프로그램 만들기, 테스터에게 보낼 파일 만들기, 설명서 배포 |
| `docs/tester-guide.md` | 테스터용 설치 안내. 테스터에게 보낼 때 `설치_안내.txt`로 복사합니다 |
| `docs/upstream-report.md` | 번역으로는 고칠 수 없어 원본에 알려야 할 문제 |
| `plans/active/upstream-korean.md` | 원본에 한국어를 보내는 계획과 진행 상황 |
| `docs/review-process.md` | 1.0 때 번역을 검수한 방식의 기록 |
| `reviews/README.md` | 검수 회차별 기록과, 지운 검수 파일을 다시 꺼내는 법 |

## 자주 하는 작업

모두 `wowwork` 폴더에서 실행합니다.

| 하는 일 | 명령 또는 문서 |
|---------|----------------|
| 원본에 생긴 새 영어 문장 찾기 | `uv run python -m tools.sync_locale`을 실행하면, 번역이 필요한 문장이 `cache\missing.tsv`에 모입니다 |
| 찾은 문장의 번역 넣기 | `cache\missing.tsv`의 ko 열에 번역을 채운 뒤 `uv run python -m tools.sync_locale cache\missing.tsv`를 실행합니다. 번역 파일은 이 방법으로만 고칩니다(`CLAUDE.md` `## 번역을 고칠 때`) |
| 영어 설명서에서 바뀐 곳 보기 | `uv run python -m tools.manual diff <쪽 경로>`. 쪽 경로는 WowVision의 `docs\src\user\en` 폴더 기준입니다(예: `basics/interface.md`) |
| 설치 프로그램에 넣을 한국어 파일 묶음(payload) 다시 만들기 | `uv run python -m tools.installer_loc payload` |
| 설치 프로그램 만들기부터 테스터에게 보낼 파일까지 | `docs/builds.md` `## 다시 만드는 법` |
| 원본에 받아들여진 PR의 작업 브랜치 정리 | `uv run python -m tools.pr_cleanup` |
| 번역 파일과 문서 검사 | `uv run pytest -q` |

# wowwork

WowVision 한국어판 작업 폴더입니다. WowVision은 시각장애인이 화면 낭독기로 World of Warcraft를 플레이할 수 있게 해 주는 애드온입니다. 한국어판에는 한국어 번역, 한국어 설치 프로그램, 한국어 설명서가 있습니다.

이 폴더에는 번역 도구, 작업 기록, 설치 프로그램 만드는 절차가 있습니다. 번역 파일과 프로그램은 다른 저장소에 있습니다(아래 `## 함께 넘겨받는 저장소`).

진행 순서: 저장소 넘겨받기, 프로그램 설치, 처음 내려받기, 내려받은 뒤 할 일.

## 용어

GitHub와 git에서 사용하는 용어입니다. 화면과 명령에는 아래 이름이 그대로 나옵니다.

- 저장소: GitHub에 있는 프로젝트 폴더. 파일과 수정 기록이 함께 있습니다.
- 원본: 한국어판의 바탕인 원래 프로젝트. WowVision은 `wow-vision`이 만들고, 로그인 툴은 `Sku75`가 만듭니다.
- 포크: 원본 저장소를 내 계정에 복사한 저장소. 원본과 연결되어 있어서 원본에 수정 제안을 보낼 수 있습니다.
- 복제: 저장소를 내 컴퓨터로 내려받기. 명령은 `git clone`입니다.
- 브랜치: 저장소 안의 작업본. 한국어 작업은 `ko` 브랜치에 있습니다. vision-locale만 `main` 브랜치입니다.
- 커밋: 수정한 내용을 기록에 저장하기.
- push: 커밋을 GitHub에 올리기.
- 병합: 다른 작업본의 변경을 내 작업본에 합치기.
- PR(풀 리퀘스트): 원본 관리자에게 내 수정을 받아 달라고 보내는 요청.
- 릴리스: 원본이 정식으로 낸 버전. 버전마다 `V1.0.4` 같은 이름표(태그)가 있습니다.
- 서브모듈: 다른 저장소의 특정 버전을 연결한 폴더. 안에서 고친 내용은 그 저장소에 따로 커밋합니다.
- payload: 한국어 설치 프로그램에 넣는 한국어 파일 묶음. 번역을 수정하면 payload를 다시 만들어야 설치 프로그램에 반영됩니다.
- Actions: GitHub가 저장소에서 정해진 작업을 자동으로 실행하는 기능. 여기서는 설명서 사이트를 만들 때 사용합니다.

## 함께 넘겨받는 저장소

모두 이전 관리자의 GitHub 계정에 있습니다.

| 저장소 | 내용 |
|--------|------|
| wowwork | 이 폴더. 번역 도구, 작업 기록, 절차 문서 |
| vision-locale | 한국어 번역 파일(koKR). 원본 `wow-vision/vision-locale`의 포크 |
| WowVision | 한국어 설명서와 설명서 사이트. 원본 `wow-vision/WowVision`의 포크 |
| wowvision-installer | 한국어 설치 프로그램. 원본 `wow-vision/wowvision-installer`의 포크 |
| wowvision-korean | 한국어판 전용 기능(센스 리더로 말하기). 설치 프로그램에 서브모듈로 연결되어 있습니다 |
| Sku-WoW-Addon-TBC | WoW Login Tool(로그인 툴) 한국어판. 원본 `Sku75/Sku-WoW-Addon-TBC`의 포크 |

이름이 `-old`로 끝나는 저장소 3개는 포크로 옮기기 전의 옛 저장소입니다. 넘겨받지 않아도 됩니다.

## 저장소 넘겨받기

이전 관리자가 위 저장소 6개를 GitHub의 Transfer ownership 기능으로 하나씩 넘깁니다. 수락 메일이 오면 메일에 적힌 기한 안에 수락합니다.

받는 계정에 아래 저장소가 있으면 넘겨받을 수 없습니다. 미리 지우거나 이름을 변경합니다.

- 넘겨받을 저장소와 이름이 같은 저장소
- 같은 원본(`wow-vision/vision-locale`, `wow-vision/WowVision`, `wow-vision/wowvision-installer`, `Sku75/Sku-WoW-Addon-TBC`)의 포크

## 프로그램 설치

### PowerShell 창 열기

명령은 모두 PowerShell 창에 입력합니다. 파일 탐색기에서 폴더를 연 뒤 Alt+D를 눌러 주소 표시줄로 이동합니다. `pwsh`를 입력하고 Enter를 누르면 그 폴더에서 PowerShell 창이 열립니다. PowerShell 7을 설치하기 전에는 `pwsh` 대신 `powershell`을 입력합니다.

이 문서에서 "X 폴더에서 실행"은 X 폴더에서 PowerShell 창을 열어 명령을 입력하라는 뜻입니다. 프로그램을 설치한 뒤에는 창을 닫고 새로 열어야 새 프로그램이 인식됩니다.

### 꼭 필요한 프로그램

아무 폴더에서 실행합니다.

    winget install --id Git.Git -e
    winget install --id GitHub.cli -e
    winget install --id astral-sh.uv -e
    winget install --id Microsoft.PowerShell -e

- Git: 저장소 내려받기, 커밋, push
- GitHub CLI(`gh`): 설명서 배포, PR 같은 GitHub 작업
- uv: 이 폴더의 파이썬 도구 실행. 필요한 파이썬(3.14)도 uv가 설치합니다
- PowerShell 7: 명령 창(`pwsh`). 설치 프로그램 빌드 스크립트도 여기서 실행합니다

설치가 끝나면 새 창에서 `gh auth login`을 실행해 GitHub에 로그인합니다. 질문에는 차례로 GitHub.com, HTTPS를 고르고, Git 인증 질문에는 Y, 로그인 방법은 웹 브라우저를 고릅니다.

### 작업에 따라 필요한 프로그램

| 작업 | 프로그램 | 설치 명령 |
|------|----------|-----------|
| 원본 WowVision 새 버전 가져오기 | LuaJIT(원본 자체 테스트) | `winget install --id DEVCOM.LuaJIT -e` |
| 설치 프로그램과 payload 만들기 | .NET SDK | `winget install --id Microsoft.DotNet.SDK.11 -e` |
| 설치 프로그램과 payload 만들기 | Visual Studio 2022 Build Tools의 C++ 도구(센스 리더 연결 파일) | `winget install --id Microsoft.VisualStudio.2022.BuildTools -e --override "--wait --passive --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"` |
| 테스터 배포 파일 묶기 | 7-Zip | `winget install --id 7zip.7zip -e` |
| 한국어 음성 팩 다시 녹음 | ffmpeg(녹음 길이 측정) | `winget install --id Gyan.FFmpeg -e` |
| 한국어 음성 팩 다시 녹음 | Vocalizer Expressive 한국어 음성 Yuna | winget에 없어서 따로 구해야 합니다 |
| 로그인 툴 화면 읽기 시험 | AutoHotkey v2 | `winget install --id AutoHotkey.AutoHotkey -e` |
| 센스 리더 동작 확인 | 센스 리더 | winget에 없어서 따로 구해야 합니다 |

작업 기록(`docs/archive/review-pipeline/review-process.md`, `reviews/`)에 나오는 Claude Code와 Codex는 이전 관리자가 번역 검수에 사용한 AI 도구입니다. 설치하지 않아도 됩니다.

## 처음 내려받기

### 폴더 배치

파일 탐색기에서 작업 폴더를 하나 만듭니다(예: `C:\wowvision`). 그 안에 이 저장소와 `wowvision-ko` 폴더를 나란히 둡니다. 도구가 이 저장소 옆의 `wowvision-ko`에서 나머지 저장소를 찾기 때문에, 폴더 이름과 위치를 변경하면 안 됩니다.

    작업 폴더
      wowwork              이 저장소
      wowvision-ko
        vision-locale        번역 파일
        WowVision            설명서. 연결된 저장소까지 약 530MB
        wowvision-installer  설치 프로그램
        Sku-WoW-Addon-TBC    로그인 툴. installer, logintool 폴더만 받습니다
        tester               테스터 배포 파일(저장소에 없음)

### 내려받기

작업 폴더에서 창을 열고 한 줄씩 실행합니다. `<계정>`은 넘겨받은 GitHub 계정 이름으로 변경합니다.

    git clone https://github.com/<계정>/wowwork.git
    mkdir wowvision-ko
    cd wowvision-ko
    git clone -b main https://github.com/<계정>/vision-locale.git
    git clone -b ko --recurse-submodules https://github.com/<계정>/WowVision.git
    git clone -b ko --recurse-submodules https://github.com/<계정>/wowvision-installer.git
    git clone -b ko --filter=blob:none --sparse https://github.com/<계정>/Sku-WoW-Addon-TBC.git
    git -C Sku-WoW-Addon-TBC sparse-checkout set installer logintool

이어서 원본 주소를 `upstream`으로 등록한 뒤 원본의 최신 기록과 버전 이름표를 받습니다. 원본 새 버전을 가져올 때 필요합니다. 창을 닫았다면 `wowvision-ko` 폴더에서 새로 열고 실행합니다.

    git -C vision-locale remote add upstream https://github.com/wow-vision/vision-locale.git
    git -C WowVision remote add upstream https://github.com/wow-vision/WowVision.git
    git -C wowvision-installer remote add upstream https://github.com/wow-vision/wowvision-installer.git
    git -C Sku-WoW-Addon-TBC remote add upstream https://github.com/Sku75/Sku-WoW-Addon-TBC.git
    git -C vision-locale fetch upstream
    git -C WowVision fetch upstream --tags
    git -C wowvision-installer fetch upstream
    git -C Sku-WoW-Addon-TBC fetch upstream

### 확인

`wowwork` 폴더에서 실행합니다.

    uv sync
    uv run python -m tools.game_terms
    uv run pytest -q

- `uv sync`: 도구에 필요한 파이썬 패키지를 설치합니다.
- `tools.game_terms`: 번역에 참고하는 게임 공식 용어(영어, 한국어)를 wago.tools에서 받아 `cache` 폴더에 저장합니다.
- `pytest`: 번역 파일과 문서를 검사합니다. `232 passed`처럼 모두 통과하면 준비가 끝났습니다. 2026-11-19에 이 순서로 새로 받아 232개 통과를 확인했습니다.

`failed`나 `error`가 나오면 폴더 배치와 내려받기 명령부터 다시 확인합니다. 저장소가 빠졌거나 폴더 이름이 다르면 검사가 한꺼번에 실패합니다. 그래도 실패하면 출력 전체를 저장해 이전 관리자에게 보냅니다.

## 수정한 내용 올리기

파일을 고친 뒤 그 저장소 폴더에서 실행합니다. push하지 않으면 내 컴퓨터에만 남습니다.

    git add -A
    git commit -m "무엇을 왜 고쳤는지 한 줄"
    git push

커밋 메시지 규칙은 저장소마다 다릅니다. 로그인 툴 저장소는 원본 규칙(영어)을 따릅니다(`CLAUDE.md` `## WoW Login Tool`).

## 내려받은 뒤 할 일

### 1. 설명서 사이트 켜기

넘겨받은 WowVision 저장소는 Actions가 꺼져 있습니다. 웹 브라우저로 저장소의 Actions 탭을 열고 "I understand my workflows, go ahead and enable them" 버튼을 누릅니다. 그다음 아무 폴더에서 실행합니다.

    gh workflow disable beta.yml -R <계정>/WowVision
    gh workflow disable release.yml -R <계정>/WowVision
    gh workflow run docs.yml -R <계정>/WowVision --ref ko

앞의 두 명령은 한국어판에 필요 없는 원본 자동 작업인 베타 빌드와 릴리스를 끕니다. 마지막 명령은 설명서 사이트를 만듭니다. `404` 오류가 나면 버튼을 아직 누르지 않은 상태입니다. 몇 분 뒤 아래 주소가 열리면 성공입니다. 이전 관리자 계정의 옛 주소는 더 이상 열리지 않습니다.

    https://<계정>.github.io/WowVision/user/ko/getting-started/introduction.html

설명서 사이트를 만드는 `docs.yml`은 켜 둡니다. 다만 원본에도 있는 작업이라, 내 WowVision 저장소의 `main` 브랜치에서 `docs` 폴더를 변경한 커밋을 push하면 사이트가 영어판으로 바뀝니다. `main` 브랜치는 원본과 맞출 필요가 없습니다. 원본에 보낼 PR은 원본의 `main`에서 새로 만들기 때문입니다. 꼭 맞춰야 한다면 `docs/builds.md` `## 한국어 설명서 배포`의 절차를 따릅니다.

### 2. 테스터 안내의 설명서 주소 변경

`docs/tester-guide.md` 첫머리에는 이전 관리자 계정의 설명서 주소가 있습니다. 1번에서 확인한 새 주소로 변경하고 커밋합니다. 다른 문서와 설정에는 계정 이름이 없어서 고칠 필요가 없습니다.

### 3. 원본 WowVision V1.0.4 반영

인계 시점(2026-11-19)의 원본 최신 버전은 V1.0.4이고, 한국어판은 V1.0.3 기준입니다. 원본 새 버전을 병합하고, 새 영어 문장을 번역하고, 설치 프로그램과 설명서를 다시 만들어야 합니다.

- 병합 대상: WowVision 저장소는 원본 `V1.0.4`, vision-locale 저장소는 원본 커밋 `3172cd5`(V1.0.4에서 사용하는 번역 파일 버전)
- 전체 순서: `CLAUDE.md` `## 원본 새 릴리스 따라가기`
- 명령: `docs/translation-guide.md` `## upstream 업데이트 절차`, `### 원본이 바뀌었을 때`

1.0 때는 Claude와 GPT 두 AI로 번역을 교차 검수했습니다(`docs/archive/review-pipeline/review-process.md`). 그 도구는 기록으로만 남아 있으니 검수 방식은 새 관리자가 정합니다. 어떤 방식이든 마지막에 `uv run pytest -q`(확정 용어 검사 포함)는 통과해야 합니다.

### 4. 로그인 툴을 원본 4.2에 맞추기

로그인 툴 한국어판(`ko` 브랜치)은 원본 4.2 개발 도중의 커밋 `6c64791`을 기준으로 합니다. 원본에 한국어를 보내려고(원본 이슈 Sku75/Sku-WoW-Addon-TBC#37) 당시 최신 상태에 맞췄습니다. 이 이슈는 인계 시점까지 답이 없습니다.

원본은 2026-11-18에 4.2를 정식으로 출시했습니다. 하지만 한국어판에는 4.2의 마지막 수정인 커밋 `f621e25`(`logintool/v2/includes/forever.ahk`)가 없습니다. Forever 클라이언트에서 로그인 툴이 강제 종료되던 문제를 고친 수정입니다. 한국어 설치 프로그램은 원본 4.2를 설치한 뒤 한국어판 파일을 덮어쓰기 때문에, 지금은 이 수정이 사라집니다.

로그인 툴 저장소의 `ko` 브랜치에 원본 `main`을 병합하고, payload와 설치 프로그램을 다시 만듭니다(`docs/builds.md` `## 다시 만드는 법`). 로그인 툴 저장소는 원본 작업 규칙을 따릅니다(`CLAUDE.md` `## WoW Login Tool`).

### 5. 저장소에 없는 파일 받기

아래 파일은 저장소에 없어서 이전 관리자에게 따로 받아야 합니다. 없어도 작업은 할 수 있습니다.

- `wowwork\WoW Login Tool Korean\_reset-backup-20261107\pre-4.2\`: 로그인 툴 4.1 기준의 옛 한국어 작업본
- `wowwork\WoW Login Tool Korean\`의 나머지: 로그인 툴을 게임에서 시험하는 폴더. 원본 로그인 툴을 풀고 한국어판 파일을 복사해 만듭니다. 복사할 파일은 `CLAUDE.md` `## WoW Login Tool`에 있습니다
- `wowvision-ko\tester\`: 마지막으로 테스터에게 보낸 파일(`WowVisionInstaller.exe`, `설치_안내.txt`, `tester.zip`). `docs/builds.md` `## 다시 만드는 법`으로 다시 만들 수 있습니다

## 문서

| 문서 | 내용 |
|------|------|
| `CLAUDE.md` | 작업 규칙(저장소 구성, 원본 새 릴리스 반영, PR, 로그인 툴, 번역 수정). AI 도구인 Claude Code용 지시 파일이지만 사람이 읽는 규칙으로도 사용합니다. 문서의 "사용자"는 관리자입니다 |
| `docs/translation-guide.md` | 번역 규칙, 원본 새 버전 반영 명령 |
| `docs/glossary.tsv` | 확정 용어. 테스트가 모든 번역에 적용합니다 |
| `docs/decisions.tsv` | 지금까지의 결정과 이유 |
| `docs/builds.md` | 설치 프로그램 만들기, 테스터 배포, 설명서 배포 |
| `docs/tester-guide.md` | 테스터용 설치 안내. 배포할 때 `설치_안내.txt`로 복사합니다 |
| `docs/upstream-report.md` | 번역으로 고칠 수 없어 원본에 알릴 문제 |
| `plans/active/upstream-korean.md` | 원본에 한국어를 보내는 계획과 진행 상황 |
| `docs/archive/review-pipeline/review-process.md` | 1.0 번역 검수 방식 기록 |
| `reviews/README.md` | 검수 회차별 기록, 지운 검수 파일 꺼내는 법 |

## 자주 하는 작업

모두 `wowwork` 폴더에서 실행합니다.

| 작업 | 방법 |
|------|------|
| 새 영어 문장 찾기 | 원본 새 버전을 병합한 뒤(내려받은 뒤 할 일 3번) `uv run python -m tools.sync_locale` 실행. 번역할 문장이 `cache\missing.tsv`에 모입니다 |
| 찾은 문장 번역 넣기 | `cache\missing.tsv`를 메모장으로 열어 ko 열을 채우고 저장한 뒤 `uv run python -m tools.sync_locale cache\missing.tsv` 실행. Excel로 저장하면 파일 형식이 바뀌어 읽지 못할 수 있습니다 |
| 기존 번역 고치기 | 열이 `file`, `key`, `en`, `ko`인 파일을 만들어 `uv run python -m tools.sync_locale <파일>` 실행. 번역 파일을 직접 고치지 않습니다(`CLAUDE.md` `## 번역을 고칠 때`) |
| 영어 설명서 변경 확인 | `uv run python -m tools.manual diff <쪽 경로>`. 쪽 경로는 WowVision `docs\src\user\en` 폴더 기준입니다(예: `basics/interface.md`) |
| payload 다시 만들기 | `uv run python -m tools.installer_loc payload` |
| 설치 프로그램 빌드부터 테스터 배포까지 | `docs/builds.md` `## 다시 만드는 법` |
| 원본에 반영된 PR의 브랜치 정리 | `uv run python -m tools.pr_cleanup` |
| 번역 파일과 문서 검사 | `uv run pytest -q` |

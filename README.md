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

## 폴더 배치

도구는 이 저장소 옆 폴더 `../wowvision-ko/`에 위 저장소가 복제되어 있다고 가정합니다.

    games/
      wowwork/
      wowvision-ko/
        vision-locale/
        WowVision/
        wowvision-installer/      (서브모듈 korean 포함)
        Sku-WoW-Addon-TBC/        (logintool/ 만 sparse checkout)

각 복제본의 `origin`은 위 포크이고, `upstream`은 원본입니다.

## 문서

| 문서 | 내용 |
|------|------|
| `CLAUDE.md` | 작업 규칙 전체(원본 PR, 병합 뒤 절차, 로그인 툴 규약) |
| `docs/translation-guide.md` | 번역 규칙 |
| `docs/review-process.md` | 번역 검수 절차 |
| `docs/glossary.tsv`, `docs/decisions.tsv` | 확정 용어와 결정 기록 |
| `docs/builds.md` | 설치 프로그램 빌드와 설명서 배포 |
| `plans/active/upstream-korean.md` | 원본에 한국어를 보내는 계획과 진행 상황 |

## 실행

Python 도구는 [uv](https://docs.astral.sh/uv/)로 실행합니다.

    uv run pytest -q
    uv run python -m tools.sync_locale

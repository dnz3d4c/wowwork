# 테스터 배포 빌드 기록

| 빌드 | 날짜 | 원본 기준 | 내 저장소 커밋 | SHA-256 |
|------|------|-----------|----------------|---------|
| WowVision-V1.0.0-ko1.zip | 2026-11-05 | wow-vision/WowVision 397ffc3 (V1.0.0 + 문서 커밋 2개) | dnz3d4c/WowVision ko dcab996, dnz3d4c/vision-locale main f36a084 | ed157b9455d5cc69229954e89bc625e66184c4427c31acb5de9069875fa0a67f |
| WowVisionInstaller.exe 1.6 (한국어 추가) | 2026-11-05 | wow-vision/wowvision-installer ef7bb8f (1.6) | dnz3d4c/wowvision-installer ko 6ee4711 | 463bbd1e99b45f34c6460c750f45ec97b34abf74749b3d177f0e873efd79fbf9 |

## 만든 방법 (원본 절차와 같게)

- 애드온: 원본 `.github/workflows/beta.yml`과 같은 순서. `luajit tools/wownav-pack.lua` → `git add -f mapdata/WowNavPacked`(커밋하지 않음) → 태그 `V1.0.0-ko1`(로컬, push하지 않음) → BigWigs packager v2 `release.sh -d`(업로드 생략). 비공개 서브모듈을 Actions가 읽을 수 없어서 이 PC에서 실행했다.
- 원본 V1.0.0 릴리스 zip과 비교: 원본에만 있는 파일 0개, 추가 23개(전부 `locale/koKR/`), 바뀐 파일은 TOC의 `## Version` 줄, `locale/modules.xml`의 koKR 포함 줄, 기준 커밋 차이로 인한 문서 4개뿐.
- 버전 `V1.0.0-ko1`은 릴리스 번호 형식이 아니라서 설치 프로그램이 테스트 빌드로 보고 교체하지 않는다(wowvision-installer `AddonInstaller.cs:242`).
- 설치 프로그램: 원본 `build.ps1 -RunTests`(PowerShell 7, scoop .NET SDK). 오프라인 자체 검사 전부 통과(`loc`: Ko 키 집합·자리표시자 일치). 버전은 1.6 그대로.

## 원본 워크플로 주의

복제 저장소의 `main`에 push하면 원본 워크플로가 내 저장소에서 실행된다(2026-11-05 확인: WowVision `beta.yml`이 내 저장소에 beta 프리릴리스를 만들었고, 설치 프로그램 `Release`도 실행됐다). 그래서 한국어 작업은 `ko` 브랜치에 둔다. `V*` 태그를 push하면 `release.yml`이 돌다가 비공개 서브모듈에서 실패한다.

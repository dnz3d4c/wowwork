# 테스터 배포 빌드 기록

## 현재 배포 (테스터 폴더: games/wowvision-ko/tester)

| 빌드 | 날짜 | 원본 기준 | 내 저장소 커밋 | SHA-256 |
|------|------|-----------|----------------|---------|
| WowVisionInstaller.exe 1.6 (한국어 화면 + koKR 덮어쓰기) | 2026-11-05 | wow-vision/wowvision-installer ef7bb8f (1.6) | dnz3d4c/wowvision-installer ko 1d22719, koKR은 dnz3d4c/vision-locale main f36a084 | a77f6c3ef0bd6d6aa8ba42d9c484b7024986272b01af41303c226a75a234b824 |

설치 프로그램은 원본 릴리스(wow-vision/WowVision)를 그대로 설치한 뒤, exe에 넣은 koKR(`payload/koKR.zip`)을 클라이언트마다 `WowVision/locale/koKR`에 쓰고 `locale/modules.xml`에 포함 줄을 한 번 더한다(`KoreanLocale.cs`). 매 실행마다 하므로 원본 업데이트로 폴더가 교체돼도 다시 들어간다.

## 다시 만드는 법

1. koKR이 바뀌면 payload를 다시 만든다: `uv run python -m tools.installer_loc payload`
2. 설치 프로그램 빌드와 원본 자체 검사: wowvision-installer 폴더에서 `build.ps1 -RunTests` (PowerShell 7, PATH 앞에 scoop .NET SDK)
3. 실제 흐름 검사(실제 릴리스를 내려받는다): `WowVisionSelfTest.exe fullinstall` — 안정판 설치 뒤와 베타 전환 뒤 모든 클라이언트에 koKR이 있는지 확인한다

## 검증 이력

- 2026-11-05: 원본 자체 검사 offline 전부 통과(kolocale 12개 포함). fullinstall 전부 통과(안정판 V1.0.0 5개 클라이언트, 베타 전환 뒤 5개 클라이언트 모두 koKR 있음).
- fullinstall이 처음에는 실패했다: 릴리스 파일이 CRLF라서 포함 줄 정규식이 맞지 않았다. 부품 검사는 LF만 써서 못 잡았다. CRLF 사례를 검사에 넣고 고쳤다.

## 이전 방식 (폐기)

애드온 테스트 빌드 zip(WowVision-V1.0.0-ko1.zip, packager로 생성, 버전 V1.0.0-ko1)을 테스터가 손으로 덮어쓰는 방식이었다. 설치 프로그램이 직접 koKR을 넣게 되면서 쓰지 않는다. 그 빌드에 쓴 WowVision ko 브랜치(dcab996)는 남아 있다.

## 원본 워크플로 주의

복제 저장소의 `main`에 push하면 원본 워크플로가 내 저장소에서 실행된다(2026-11-05 확인). 그래서 한국어 작업은 `ko` 브랜치에 둔다.

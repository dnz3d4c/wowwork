# 테스터 배포 빌드 기록

## 현재 배포 (테스터 폴더: games/wowvision-ko/tester)

| 빌드 | 날짜 | 원본 기준 | 내 저장소 커밋 | SHA-256 |
|------|------|-----------|----------------|---------|
| WowVisionInstaller.exe 1.6 (한국어 화면 + koKR 덮어쓰기, 1.0 최종 검수 반영) | 2026-11-06 | wow-vision/wowvision-installer ef7bb8f (1.6) | dnz3d4c/wowvision-installer ko 702f903, koKR은 dnz3d4c/vision-locale main bff9930 | e4a73d96698b5fecf5059966acae4bbfa3ccc7ed6a854adf265e538164d16ecc |

이전 배포: 2026-11-05, ko a948d1a, koKR f36a084, SHA-256 1f3401c1733f9591f878c307041c50679b0e3f28576729b13a55daf33911ad47.

설치 프로그램은 원본 릴리스(wow-vision/WowVision)를 그대로 설치한 뒤, exe에 넣은 koKR(`payload/koKR.zip`)을 클라이언트마다 `WowVision/locale/koKR`에 쓰고 `locale/modules.xml`에 포함 줄을 한 번 더한다(`KoreanLocale.cs`). 매 실행마다 하므로 원본 업데이트로 폴더가 교체돼도 다시 들어간다.

## 다시 만드는 법

1. koKR이 바뀌면 payload를 다시 만든다: `uv run python -m tools.installer_loc payload`
2. 설치 프로그램 빌드와 원본 자체 검사: wowvision-installer 폴더에서 `build.ps1 -RunTests` (PowerShell 7, PATH 앞에 scoop .NET SDK)
3. 실제 흐름 검사(실제 릴리스를 내려받는다): `WowVisionSelfTest.exe fullinstall` — 안정판 설치 뒤와 베타 전환 뒤 모든 클라이언트에 koKR이 있는지 확인한다
4. 테스터 폴더에 exe와 함께 `docs/tester-guide.md`를 `설치_안내.txt`로 복사한다. 먼저 `uv run pytest -q tests/test_tester_guide.py`로 안내가 설치 프로그램의 모든 옵션을 담고 있는지 확인한다(2026-11-06 NVDA 브리지 누락의 재발 방지)

## 검증 이력

- 2026-11-06("찾지 못함" 상태 줄 수정): Loc.cs 문구 하나만 바뀌고 payload는 그대로라 `build.ps1 -RunTests`만 다시 돌려 통과. `fullinstall`은 다시 돌리지 않았다(koKR과 설치 흐름이 바뀌지 않음). 이전 판 ko d7c6c7c, SHA-256 58051f1d….

- 2026-11-06(최종 검수 반영): payload 재생성 뒤 `build.ps1 -RunTests` 전부 통과(kolocale 포함), `fullinstall` 전부 통과(안정판과 베타 전환 뒤 5개 클라이언트 모두 koKR 덮어쓰기 확인). 새 exe 안에 "WoW에서 NVDA를 음성으로 사용"과 이번 검수의 새 문구가 들어 있는 것을 확인했다. 테스터 폴더에 exe와 `설치_안내.txt`(= `docs/tester-guide.md`)를 넣었다.

- 2026-11-05: 원본 자체 검사 offline 전부 통과(kolocale 16개 포함, 깨진 payload 실패 경로 포함). fullinstall 전부 통과(안정판 V1.0.0 5개 클라이언트, 베타 전환 뒤 5개 클라이언트 모두 koKR 있음).
- fullinstall이 처음에는 실패했다: 릴리스 파일이 CRLF라서 포함 줄 정규식이 맞지 않았다. 부품 검사는 LF만 써서 못 잡았다. CRLF 사례를 검사에 넣고 고쳤다.

## 이전 방식 (폐기)

애드온 테스트 빌드 zip(WowVision-V1.0.0-ko1.zip, packager로 생성, 버전 V1.0.0-ko1)을 테스터가 손으로 덮어쓰는 방식이었다. 설치 프로그램이 직접 koKR을 넣게 되면서 쓰지 않는다. 그 빌드에 쓴 WowVision ko 브랜치(dcab996)는 남아 있다.

## 원본 워크플로 주의

복제 저장소의 `main`에 push하면 원본 워크플로가 내 저장소에서 실행된다(2026-11-05 확인). 그래서 한국어 작업은 `ko` 브랜치에 둔다.

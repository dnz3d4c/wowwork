# 테스터 배포 빌드 기록

## 현재 배포 (테스터 폴더: games/wowvision-ko/tester)

| 빌드 | 날짜 | 원본 기준 | 내 저장소 커밋 | SHA-256 |
|------|------|-----------|----------------|---------|
| WowVisionInstaller.exe 1.6 (한국어 화면 + koKR 덮어쓰기, NVDA 브리지 기본 설치, 한국어 음성 팩 Yuna 설치) | 2026-11-08 | wow-vision/wowvision-installer ef7bb8f (1.6), 설치되는 애드온은 원본 안정판 V1.0.1 | dnz3d4c/wowvision-installer ko 92a8c86, koKR은 dnz3d4c/vision-locale main a78f05a, 음성 팩은 wowwork assets/voice/Yuna | a36ddb23ae6aa203585d5ed578df1bc453acc507ac4f6f448bba37dc43574779 |

이전 배포: 2026-11-08, ko 5acdf8b, SHA-256 5cc1d57293de5ed32765d084baef014e0ed8cf23adb336bff5f8f795eacd6278(음성 팩 다시 녹음). 그 전: 2026-11-07, ko c3ec7a7, SHA-256 fe5ce7adc6f9312a007960083ae8a8b9b916e62140ecb1ff549fa5e765071a26(음성 팩 첫 판, 속도 0·볼륨 100). 그 전: 2026-11-07, ko d0bb60a, SHA-256 acc3aed69eb47d4fc1a9e9aacd1962cba1e0b405297a080ab038c6f62986b116(V1.0.1 새 문자열). 그 전: 2026-11-07, ko b7177f6, koKR 980fdb5, SHA-256 3157ea4c206c6e674a0ef0a324de29c894e6cc17fd4a9079156f2cac4f37c142(설명서 다듬기의 koKR 변경). 그 전: 2026-11-06, ko accab35, koKR bff9930, SHA-256 ad48ba89b5e3272afd6e6745fa6575c6e3e1e51c354d47827a797a2864dc546a. 그 전: 2026-11-06, ko 702f903, SHA-256 e4a73d96698b5fecf5059966acae4bbfa3ccc7ed6a854adf265e538164d16ecc. 그 전: 2026-11-05, ko a948d1a, koKR f36a084, SHA-256 1f3401c1733f9591f878c307041c50679b0e3f28576729b13a55daf33911ad47.

원본과 다른 기본값: NVDA 음성 브리지(`InstallRunner.cs`의 `InstallSapi2Sr`)가 켜져 있다. 원본은 꺼 둔다. "지금 설치", "지금 업데이트", 구성 요소 페이지가 모두 이 기본값으로 시작하므로 모든 설치 경로에서 브리지가 설치된다. 구성 요소 페이지에서는 여전히 해제할 수 있다(2026-11-06 사용자 지시).

설치 프로그램은 원본 릴리스(wow-vision/WowVision)를 그대로 설치한 뒤, exe에 넣은 koKR(`payload/koKR.zip`)을 클라이언트마다 `WowVision/locale/koKR`에 쓰고 `locale/modules.xml`에 포함 줄을 한 번 더한다(`KoreanLocale.cs`). 매 실행마다 하므로 원본 업데이트로 폴더가 교체돼도 다시 들어간다.

## 다시 만드는 법

1. koKR이나 음성 팩이 바뀌면 payload를 다시 만든다: `uv run python -m tools.installer_loc payload` (koKR.zip과 koVoice.zip). 음성 팩 자체는 `uv run python -m tools.voice_pack build`로 다시 녹음한다(Vocalizer Expressive Yuna, SAPI COM)
2. 설치 프로그램 빌드와 원본 자체 검사: wowvision-installer 폴더에서 `build.ps1 -RunTests` (PowerShell 7, PATH 앞에 scoop .NET SDK)
3. 실제 흐름 검사(실제 릴리스를 내려받는다): `WowVisionSelfTest.exe fullinstall` — 안정판 설치 뒤와 베타 전환 뒤 모든 클라이언트에 koKR이 있는지 확인한다
4. 테스터 폴더에 exe와 함께 `docs/tester-guide.md`를 `설치_안내.txt`로 복사한다. 먼저 `uv run pytest -q tests/test_tester_guide.py`로 안내가 설치 프로그램의 모든 옵션을 담고 있는지 확인한다(2026-11-06 NVDA 브리지 누락의 재발 방지)

## 검증 이력

- 2026-11-08(첫 화면 버튼 이름): 사용자 결정으로 "지금 설치"를 "권장 구성으로 설치"로 바꿨다. "WowVision 새로 설치, 또는 다른 게임 버전에 설치"와 이름만으로 구분되지 않았기 때문이다. 업데이트 버튼은 현재 설정을 유지하므로(설명 문구 update.explainUpdate) "현재 설정으로 업데이트"로 했다. 설명 문구와 스크린리더 이름(update.installAcc, update.updateAcc)도 맞췄다. `uv run pytest -q` 233개 통과, `build.ps1 -RunTests` PASS 207개·FAIL 0, exe 안에 새 이름이 있고 옛 이름이 없는 것을 확인했다. 설치 흐름은 바뀌지 않아 `fullinstall`은 다시 돌리지 않았다. 테스터 폴더의 exe, `설치_안내.txt`, `tester.zip`을 교체했다.

- 2026-11-08(음성 팩 다시 녹음): 사용자가 속도 샘플(0, 3, 5) 가운데 5를 골랐다. 볼륨 100 녹음은 SAPI wav 단계에서 이미 0 dBFS로 잘려 있었다("동쪽" 한 단어에 최대값 샘플 147개, 108개 중 77개 파일 피크 -0.1 dB 이상). SAPI 볼륨 60으로 녹음해 원본 팩 수준에 맞췄다(Yuna 평균 -22.2 dB·최대 피크 -8.3 dB, Matthew -24.1 dB·-6.3 dB). 빌드는 피크가 -1 dB를 넘는 파일이 있으면 실패한다(`too_loud`). payload 재생성 뒤 `uv run pytest -q` 231개 통과, `build.ps1 -RunTests` PASS 207개·FAIL 0. 설치 흐름은 바뀌지 않아 `fullinstall`은 다시 돌리지 않았다. 테스터 폴더의 exe와 `tester.zip`을 교체했다.

- 2026-11-07(한국어 음성 팩 Yuna): 나침반 방향 8개와 숫자 1~100을 Vocalizer Expressive Yuna로 녹음(`tools/voice_pack.py`, 잘린 녹음은 음절당 0.09초 기준으로 실패 처리). 설치 프로그램이 `audio/voice/Yuna`를 쓰고 `audio/voice.lua`에 등록 줄을 더한다(`KoreanVoice.cs`). 자체 검사 kovoice 18개 포함 `build.ps1 -RunTests` 전부 통과, `fullinstall` 전부 통과(5개 클라이언트, 안정판과 베타 전환 뒤 모두 Yuna 확인). 등록 줄을 원본 voice.lua 뒤에 붙여 luajit으로 실행해 세 팩 등록을 확인(`tests/test_voice_registration.py`). 실패 문구와 안내는 Claude·GPT 평가, 판정, 회귀 확인을 거쳤다(`reviews/2026-11-07-ko-voice`). 테스터 폴더 교체.

- 2026-11-07(V1.0.1 새 문자열 66개): payload 재생성 뒤 `build.ps1 -RunTests` 전부 통과(FAIL 0), `fullinstall` 전부 통과(안정판 V1.0.1과 베타 전환 뒤 5개 클라이언트 모두 koKR 덮어쓰기 확인). payload를 풀어 "경로 역방향 전환, %s까지 돌아감", "대상의 대상 없음", "자리 비움 (AFK)", "파티 초대 수락"이 들어 있는 것을 확인했다. 안내는 바뀌지 않았다. 테스터 폴더의 exe, `설치_안내.txt`, `tester.zip`을 교체했다. 번역 평가 기록: `reviews/2026-11-07-ui-v1.0.1`.

- 2026-11-07(설명서 다듬기의 koKR 변경 29건): payload 재생성 뒤 `build.ps1 -RunTests` 전부 통과(FAIL 0), `fullinstall` 전부 통과(안정판과 베타 전환 뒤 5개 클라이언트 모두 koKR 덮어쓰기 확인). payload를 풀어 "알림 편집기", "모아 말하기", "죽음", "핵심 능력 또는 보조 능력 없음"이 들어 있고 "경보"가 없는 것을 확인했다. 안내(`docs/tester-guide.md`)는 바뀌지 않았고 `tests/test_tester_guide.py` 통과. 테스터 폴더의 exe, `설치_안내.txt`, `tester.zip`(파일 이름 UTF-8 표시)을 교체했다.

- 2026-11-06(NVDA 브리지 기본 설치): 자체 검사 kolocale에 "NVDA bridge ticked by default"를 넣고 수정 전 실패를 확인한 뒤, 기본값을 바꾸고 `build.ps1 -RunTests` 전부 통과. 안내 기본값 검사(`test_guide_states_voice_bridge_default`) 추가, `uv run pytest -q` 166개 통과. koKR과 설치 흐름은 바뀌지 않아 `fullinstall`은 다시 돌리지 않았다(그 검사는 `SkipMachineWide`로 브리지 단계를 건너뛰므로 이번 변경을 확인하지도 못한다). 실제 PC에서 브리지 설치를 확인하는 것은 테스터 설치로 한다.

- 2026-11-06("찾지 못함" 상태 줄 수정): Loc.cs 문구 하나만 바뀌고 payload는 그대로라 `build.ps1 -RunTests`만 다시 돌려 통과. `fullinstall`은 다시 돌리지 않았다(koKR과 설치 흐름이 바뀌지 않음). 이전 판 ko d7c6c7c, SHA-256 58051f1d….

- 2026-11-06(최종 검수 반영): payload 재생성 뒤 `build.ps1 -RunTests` 전부 통과(kolocale 포함), `fullinstall` 전부 통과(안정판과 베타 전환 뒤 5개 클라이언트 모두 koKR 덮어쓰기 확인). 새 exe 안에 "WoW에서 NVDA를 음성으로 사용"과 이번 검수의 새 문구가 들어 있는 것을 확인했다. 테스터 폴더에 exe와 `설치_안내.txt`(= `docs/tester-guide.md`)를 넣었다.

- 2026-11-05: 원본 자체 검사 offline 전부 통과(kolocale 16개 포함, 깨진 payload 실패 경로 포함). fullinstall 전부 통과(안정판 V1.0.0 5개 클라이언트, 베타 전환 뒤 5개 클라이언트 모두 koKR 있음).
- fullinstall이 처음에는 실패했다: 릴리스 파일이 CRLF라서 포함 줄 정규식이 맞지 않았다. 부품 검사는 LF만 써서 못 잡았다. CRLF 사례를 검사에 넣고 고쳤다.

## 이전 방식 (폐기)

애드온 테스트 빌드 zip(WowVision-V1.0.0-ko1.zip, packager로 생성, 버전 V1.0.0-ko1)을 테스터가 손으로 덮어쓰는 방식이었다. 설치 프로그램이 직접 koKR을 넣게 되면서 쓰지 않는다. 그 빌드에 쓴 WowVision ko 브랜치(dcab996)는 남아 있다.

## 한국어 설명서 배포

- 주소: https://gong.aheu.org/WowVision/user/ko/getting-started/introduction.html (`dnz3d4c/WowVision` 공개, GitHub Pages는 Actions 방식). 설치 프로그램에는 넣지 않는다(`docs/decisions.tsv` 2026-11-06).
- ko 브랜치에 push해도 자동 배포되지 않는다(원본 `docs.yml`은 main push에만 돈다). 설명서를 고친 뒤 `gh workflow run docs.yml -R dnz3d4c/WowVision --ref ko`로 다시 배포한다.
- main에 push하면 원본 `docs.yml`(영어판으로 Pages를 덮어씀)과 `beta.yml`(beta 프리릴리스 생성)이 돈다. main을 원본에 맞출 때는 `gh workflow disable`로 두 워크플로를 끄고 push한 뒤 다시 켠다. 원본 태그(V*)는 push하지 않는다(`release.yml`).

## 원본 워크플로 주의

복제 저장소의 `main`에 push하면 원본 워크플로가 내 저장소에서 실행된다(2026-11-05 확인). 그래서 한국어 작업은 `ko` 브랜치에 둔다.

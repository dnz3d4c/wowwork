# 1.0 최종 번역 검수 진행 기록

계획: `docs/final-review.md`. 시간순으로 적는다.

## 2026-11-06

### 권한 확인 창

- 확인 창의 출처를 조사했다. 저장소 경계 훅(`~/.claude/hooks/repo_boundary.py`)은 세션마다 저장소별로 한 번만 묻고 기억한다(`cache/sessions/<세션>.granted`). 2026-11-05~06 차단 기록(`cache/blocks/blocks-2026-11.jsonl`)에서 경계 훅이 물은 것은 3번뿐이었다.
- 경계 훅에 "작업 저장소가 선언한 동반 저장소는 묻지 않는다" 기능을 넣으려 했다. 자동 모드 분류기가 안전 훅 수정을 자기 수정(Self-Modification)으로 거부했다. 우회하지 않고 되돌렸다. 훅 파일은 수정 전과 같다(동기화 저장소 `c9b0aad~1` 판과 diff 없음). 테스트 46개 통과.
- 남은 확인 창은 Claude Code 자체의 권한 확인이며, 설정은 사용자가 직접 바꿔야 한다(보고에 방법 적음).

### NVDA 브리지 누락 조사

- 실행 파일에는 옵션이 있다. 테스터 실행 파일 SHA-256 `1f3401c1…`(`docs/builds.md`와 같음) 안에 `opt.sapi2sr.label`과 한국어 "WoW에서 NVDA를 음성으로 사용"이 들어 있다. 소스 `ComponentsForm.cs:103`은 조건 없이 옵션을 추가한다. 원본 1.6 태그와 ko 브랜치의 차이에서 지운 줄은 언어 목록 한 줄(Ko 추가)뿐이다.
- 빠진 곳은 테스터 안내(`docs/tester-guide.md` = `설치_안내.txt`)다. 안내는 "평소처럼 설치합니다"라고만 했다. 첫 화면의 "지금 업데이트"는 권장 기본값으로 설치하므로 브리지가 들어가지 않는다(`InstallRunner.cs:21` `InstallSapi2Sr = false`). 원본 설명서(`en/getting-started/installer.md:31~46`)는 "새로 설치, 또는 다른 게임 버전에 설치" 경로의 구성 요소 페이지에서 "Enable NVDA as a voice in WoW (not ticked)"를 고르라고 안내한다.
- 원인: 2026-11-05 `fca7ed7`에서 안내를 처음 쓸 때, 원본 설명서의 설치 절차에서 출발하지 않고 "원본과 다른 점(한국어)"만 적었다. 원본 기능 목록과 대조하는 검사가 없어서 빠진 것이 드러나지 않았다.
- 수정: `docs/tester-guide.md` `## 설치`를 원본 설명서의 첫 화면 선택지와 "직접 고르기" 세 페이지 흐름으로 다시 썼다. 구성 요소 페이지의 모든 옵션과 기본 체크 상태, "지금 업데이트"는 음성 옵션을 실행하지 않는다는 원본 설명을 옮겼다. 테스터 폴더 `설치_안내.txt`에도 복사했다.
- 방지책 1(기계 검사): `tests/test_tester_guide.py`. `ComponentsForm.cs`의 `SetOptionText` 호출에서 옵션 키를 뽑아, 그 한국어 이름과 "새로 설치" 버튼, "추가 권장 애드온"이 안내에 모두 있는지 확인한다. 수정 전 안내로 실패(red)를 확인했고, 수정 후 통과했다.
- 방지책 2(규칙): 프로젝트 `CLAUDE.md` `## 원본 기능을 빼지 않는다`. 안내는 원본 절차에서 출발하고, 원본 태그 대비 지운 코드 줄은 모두 이유가 있어야 한다.
- 방지책 3(절차): `docs/builds.md` 다시 만드는 법 4단계에 안내 복사와 검사 실행을 넣었다.
- 방지책 4(메모리): `localized-fork-keep-upstream-features`.

### 페르소나 평가 시작

- 페르소나 파일: `tools/review/prompts/persona-base.md`(공통), `lens-persona-sr-gamer.md`, `lens-persona-wow-veteran.md`, `lens-persona-editor.md`, `lens-persona-ux-writer.md`, `lens-persona-newcomer.md`, 설치 프로그램용 `lens-persona-windows-user.md`(WoW 플레이어 대신).
- `full.js`가 `lenses` 인자로 페르소나 목록을 받도록 고쳤다(평가자 실패 수 계산도 목록 길이 기준으로).
- 묶음: UI 1,363개 → `reviews/2026-11-06-final-ui/batches` 10개(140개씩), 설치 프로그램 205개 → `reviews/2026-11-06-final-installer/batches` 3개.
- Workflow: UI `wf_8b3afc4d-887`, 설치 프로그램 `wf_ebfe4c7f-b61`. 묶음마다 Claude 5 + GPT 5 → 번역자 반박 → 두 회사 판정.
- 1차 실행이 사용량 한도(05:20 초기화)에 걸렸다. 설치 프로그램은 판정자 5명, UI는 평가자·번역자 55명이 실패했다(UI 묶음 7~10은 평가 전부 미실행). 10:23에 같은 Run ID로 이어서 실행했다(UI `wpupjxhvs`, 설치 프로그램 `wsegvmyj7`). 끝난 에이전트는 캐시를 쓴다.

### 설치 프로그램 결과 (`reviews/2026-11-06-final-installer/result.json`)

- 평가자 30명 모두 성공, 지적 144건. 항목 기준 확정 48건(두 회사 합의 22, 번역자 수용 16, 반박 인정 10), 판정 갈림 3건.
- 판정 갈림 3건(`selfupdate.restarting`, `selfupdate.done`, `selfupdate.working`)은 모두 어순 문제다. `docs/decisions.tsv` 2026-11-06 기준(근거가 글자 그대로 확인되는 것만 반영)에 따라 현재 번역을 유지했다.
- 실제로 바뀐 항목은 38개다. 원문과 전·후 대조는 `changes.md`. 직접 확인해서 뜻 변경과 자리표시자 오류가 없는 것을 확인했다. `update.heading.available`은 같은 화면의 다른 제목과 같은 명사형으로 맞춰졌다.
- 반영: `tools.installer_loc apply ko.tsv`, wowvision-installer ko 브랜치에 커밋.
- 함께 발견: `status.koreanFailed` 문구가 바뀌어 테스터 안내의 인용이 옛 문구가 됐다. 안내를 고치고, 안내의 따옴표 인용이 설치 프로그램 Ko 표에 실제로 있는지 보는 검사(`test_guide_quotes_match_installer_text`)를 추가했다. 옛 문구로 실패하는 것을 확인했다.
- 빌드는 UI 검수 반영 뒤 한 번에 한다(설치 프로그램에 koKR이 들어가므로).

### UI 결과 (`reviews/2026-11-06-final-ui/result.json`)

- 평가자 100명 모두 성공(묶음별 실패 0), 지적 297건. 항목 기준 확정 119건(합의 14, 수용 41, 반박 인정 64), 판정 갈림 7건.
- 판정 갈림 7건(`colors.lua::grayish`, `violet`, `minimap.lua::turned`, `navigation.lua::trainer`, `quests.lua::Questie is not loaded`, `ui.lua::controlled` 등)은 2026-11-06 기준으로 현재 번역 유지. `violet`의 GPT 근거 "보라색"은 주택 외관 색상(다른 문맥)이고 같은 목록의 `purple`이 이미 "보라색"이라 두 색이 같아진다.
- 번역 변경 55건(`apply.tsv`, 전·후 `changes.txt`). 직접 대조 결과 1건 제외: `navigation.lua` 카메라 안내의 "카메라 따라가기 방식"은 게임 공식 `CAMERA_FOLLOWING_STYLE`="시점 전환 방식"(`cache/gs_koKR.csv:4018`)과 다르다. `docs/review-process.md` 5단계에 이미 같은 회귀가 기록되어 있다. 54건만 `apply-final.tsv`로 반영(`tools.sync_locale`, koKR 17개 파일).
- 코드 리터럴 문제(번역으로 못 고침, upstream 보고 대상): `tbc/auction/ScanSession.lua:147`의 `" in "`, `tbc/auction/module.lua:80-93`의 `" min "`, `" sec"`가 `L[]` 밖이라 한국어로 읽히지 않는다.
- 주의 항목: `ui.lua::Disabled`가 "사용 안 함"으로 바뀌었다. 공식 근거는 애드온 목록 문맥(`ADDON_DISABLED`)인데 코드는 비활성 컨트롤 상태로 읽는다(`core/graph/nodes.lua:210`). 회귀 확인에서 판단한다.
- 회귀 확인 시작: UI 54건 `wf_0a408d9f-d0d`, 설치 프로그램 38건 `wf_5c90d183-7bc` (Claude 1 + GPT 1, 네 관점).
- `test_installer_payload_matches_current_kokr` 실패는 예상된 것(koKR이 바뀌어 payload가 낡음). 회귀 확인 뒤 payload를 다시 만든다.

### 설치 프로그램 회귀 확인 1회차 (`wf_5c90d183-7bc`)

- 중대 1건: `managed.notForClient` "{0}: 사용할 수 없는 게임 버전({1}), 건너뜀."이 "게임 버전 자체를 쓸 수 없다"로 들린다(GPT major, Claude 같은 항목 minor). 두 회사가 같은 항목을 지적했으므로 절차 2단계대로 반박 없이 수용: "{0}: {1}에서 사용할 수 없어 건너뜀." (`에서`는 받침과 무관한 조사)
- 경미(보고만): `logs.btnAcc` 수식 관계, `opt.windowsVoices.desc`의 newer.
- codex [자동수정] "낡은 payload": UI 회귀 확인 반영 뒤 payload를 다시 만들 때 처리한다(빌드 단계).

### UI 회귀 확인 1회차 (`wf_0a408d9f-d0d`)

- 중대 1건(GPT): `bindings.lua::Roll Bonus` "추가 전리품 주사위"는 공식 용어와 다르다. 한 회사 지적이라 반박과 두 회사 판정을 다시 거쳤다(`regression-1/judge-*.json`). 두 판정자 모두 지적 인정: 영어 bonus roll은 공식 문자열 세 곳(ERR_BONUS_ROLL_EMPTY, NO_TRADE_FROM_BONUS_ROLL, ORDER_HALL_MISSION_BONUS_ROLL)에서 "보너스 주사위"이고, "추가 전리품"은 Bonus Loot의 번역이다. 원래 번역 "보너스 주사위"로 되돌렸다. 최종 반영은 53건.
- `ui.lua::Disabled` "사용 안 함"은 두 회귀 평가자 모두 지적하지 않았다.
- 경미(보고만): `windows.lua` 행동 단축바 안내의 "끌 수 있도록"이 '끄다'로도 들림, 차원문 안내 두 키의 동사 불일치("선택하고"/"잡고"), "이동 수단 이용이 너무 오래 걸림; 경로 종료"의 인과 문형.
- koKR은 vision-locale main에 커밋.

### 설명서 인용 맞추기

- 설명서는 이번 검수 범위가 아니지만, 설명서는 koKR 값을 화면 문구로 인용하므로(`docs/manual-plan.md` `### 용어` 1번) 바뀐 값을 따라야 한다.
- 기준: 따옴표 안에 옛 값 전체가 인용된 곳, 또는 8자 이상인 옛 값이 나오는 곳만 바꾼다. 짧은 일반 낱말이 본문 문장에 쓰인 곳은 건드리지 않는다. 61곳 변경(`manual-sync.log`).
- 같은 옛 값을 쓰는 다른 키가 남은 경우를 원문과 대조했다: `world/combat.md`의 "제어됨" 3곳은 원문이 `"controlled"`(`ui.lua` 키, 값 유지)라서 되돌렸다. "사용 안 함"으로 바꾼 곳은 원문이 모두 `"Disabled"`다.
- 설명서 기계 검사 51/51 통과. WowVision ko 브랜치에 커밋.

### 설치 프로그램 회귀 확인 2회차

- `managed.notForClient` 1건만 다시 평가 중(`wf_7d160cc5-3af`). 순환 2회째.
- 2회차 결과: 두 평가자 모두 지적 없음(통과).

### 빌드와 배포

- payload 재생성(codex [자동수정] "낡은 payload" 처리), 테스트 154개 통과.
- `build.ps1 -RunTests` 전부 통과, `fullinstall` 전부 통과(5개 클라이언트 × 안정판·베타 전환 뒤 koKR 덮어쓰기 확인).
- 새 exe SHA-256 `58051f1d…`, NVDA 브리지 옵션 문구와 이번 검수 문구 포함 확인. 테스터 폴더에 exe와 `설치_안내.txt` 교체. `docs/builds.md` 업데이트.
- 원본 1.6 대비 지운 줄 점검(`CLAUDE.md` 규칙): 6줄 모두 Ko 추가로 바뀐 줄이며 기능 제거 없음.

### 요구사항 대조 (`docs/final-review.md` `## 요구사항`)

1. GPT 포함: 평가(페르소나 5 × Claude·GPT), 판정(두 회사), 회귀 확인(Claude 1 + GPT 1) 모두 GPT가 들어갔다. 완료.
2. 치우치지 않는 페르소나: 페르소나마다 빠지기 쉬운 쪽과 견제 관계를 정했다(`persona-base.md`, `lens-persona-*.md`). 완료.
3. 말투·문법·종류별 문체: `persona-base.md`가 AI가 쓴 티, 문구 종류별 말투, 문법을 지정했다. UI 53건, 설치 프로그램 39건 변경. 완료.
4. 기록: 이 파일과 `reviews/2026-11-06-final-*`. 완료.
5. NVDA 브리지 누락: 원인 조사와 방지책 4가지. 완료.
6. 확인 창: 안전 훅 수정은 분류기가 거부했다. 남은 설정은 사용자가 `/permissions`에서 해야 한다. 부분 완료.

### 재발 방지 조치 (사용자 지시: 배운 것을 적용)

| 배운 것 | 장치 | 종류 |
|---------|------|------|
| 원본 기능을 안내에서 빠뜨림(NVDA 브리지) | `tests/test_tester_guide.py` 옵션 대조, 프로젝트 `CLAUDE.md`, `docs/builds.md` 4단계, 메모리 `localized-fork-keep-upstream-features` | 기계 검사 + 규칙 |
| 설치 프로그램 문구가 바뀌어 안내 인용이 낡음 | `test_guide_quotes_match_installer_text` | 기계 검사 |
| 되돌린 번역이 다시 들어옴("카메라 따라가기 방식", "추가 전리품 주사위") | `docs/glossary.tsv`에 camera following style, roll bonus, bonus roll 추가, `test_glossary_blocks_reverted_translations`(넣기 전 실패 확인), `review-process.md` 원칙 6 | 기계 검사 |
| 다른 영어의 공식 번역을 근거로 씀 | `common.md`, `rebut.md`, `judge.md`, `manual-review.md`에 "공식 문자열의 영어가 같아야 근거" 규칙 | 프롬프트 |
| koKR 변경 뒤 설명서 인용 맞추기를 임시 스크립트로 하다 같은 값의 다른 키를 잘못 바꿈 | `tools/manual_sync.py` + `tests/test_manual_sync.py` 7개(키 충돌, 대소문자, 두 번 돌려도 같음). 이번 실제 사례를 맞추기 전 판에 돌려 확정 결과와 51개 파일 모두 같음을 확인. `translation-guide.md` 업데이트 절차 5·6단계, `review-process.md` 원칙 8 | 도구 + 기계 검사 |
| 대량 작업 뒤에 방침이 정해져 다시 고침(원문 충실 113건) | `review-process.md` 원칙 7 | 절차 |
| 순환 상한 뒤 처리 기준이 없었음 | `decisions.tsv` 2026-11-06, `review-process.md` 5단계 | 결정 기록 |
| 재처리 도구 결함(반박 파일 형식, 반영 실패 집계) | `refix_input.py load_rebut` + 테스트, `manual-refix.js` | 도구 + 테스트 |
| `cd`로 작업 폴더가 다른 저장소로 넘어감 | 메모리 `shell-cd-subshell` | 메모리 |
| `python -I`가 `PYTHONIOENCODING`을 무시 | `~/.claude/CLAUDE.md` 환경 표 "Python 한글 출력" | 환경 사실 |
| Workflow가 사용량 한도에 걸려 판정 누락 | 메모리 `workflow-usage-limit-resume` | 메모리 |
| 번역으로 못 고치는 것이 흩어져 있음 | `docs/upstream-report.md`(설명서 차이 13건, 코드 문자열 2건) | 목록 |

- codex [자동수정] 2건 처리: 위 표(UI·설명서 교훈의 재발 방지), `final-review.md` 상태를 "요구사항 6 부분 완료"로 정정.

## 2026-11-06 테스터 설치 안내 다듬기 (사용자 지시, 모든 과정 GPT 포함)

- 수정 전: `reviews/2026-11-06-tester-guide/before.md`. 작성자(Claude)가 수정안을 먼저 썼다(`docs/tester-guide.md`).
- 수정안에서 바꾼 것: 문서 종류를 How-to로 정하고 실행 순서대로 다시 배치. 자체 업데이트 질문을 첫 화면 앞으로 옮김(원본 `installer.md`도 그 순서). 완료 화면과 "설치 프로그램 닫기" 단계 추가. 원본 `installation.md`의 두 사실 추가: 새 애드온은 게임을 시작할 때만 인식되어 /reload로 부족함, 로드되지 않으면 /enableaddons. 기본 체크 상태를 "(기본 체크됨)"으로 명확히 함. "그 뒤에 알아 둘 것"을 "업데이트"와 "문제가 생기면"으로 나눔.
- 평가: 관점 3개(처음 설치하는 테스터, 사실 검증, 한국어 편집) × Claude·GPT = 6명, 서로 비공개(`tools/review/workflows/guide-review.js`, `wf_b46e4095-792`). 이후 작성자 반박 → 반박된 지적은 두 회사 판정 → 반영 → 회귀 확인(Claude 1 + GPT 1).
- 참고: 수정안의 "직접 고르기" 인용은 절 이름인데, 설치 프로그램 문구 "버전과 구성 요소 직접 고르기"에 포함되어 인용 검사를 우연히 통과한다.

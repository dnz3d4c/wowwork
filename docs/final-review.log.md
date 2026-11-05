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

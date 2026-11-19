# 1.0 번역 검수 파이프라인(기록)

2026-11-05부터 11-14까지 WowVision 한국어판 1.0을 검수한 스크립트와 프롬프트입니다. 2026-11-19에 `tools/review/`에서 이 폴더로 옮겼습니다. 방식 설명은 `docs/review-process.md`, 회차별 결과는 `reviews/README.md`에 있습니다.

이 폴더는 실행용이 아니라 기록용입니다. 이전 관리자의 환경을 전제하므로 그대로는 동작하지 않습니다.

`tools-review/` 안의 구성은 다음과 같습니다.

- `workflows/*.js`: Claude Code의 Workflow 스크립트입니다. 평가자, 번역자 반박, 판정자를 차례로 실행합니다. 스크립트에는 저장소 위치가 `C:/project/games/wowwork`로 적혀 있습니다.
- `gpt_review.py`: Codex CLI(`codex exec`)로 GPT 평가자를 실행합니다. 이전 관리자의 Codex 프로필 `review_strict`를 사용합니다.
- `prompts/`: 평가자, 번역자 반박, 판정자에게 준 지시와 관점별 프롬프트입니다.
- `build_batch.py`: 평가 묶음을 만듭니다.
- `decisions.py`: 판정 결과로 반영 목록을 만듭니다.
- `seed.py`, `score.py`: 검증용 오류를 만들고, 평가자가 찾은 오류 수를 채점합니다.
- `sandbox.py`: 평가자가 정답을 볼 수 없도록 격리 폴더를 만듭니다.
- `guard.py`: 판정 근거가 원문, 코드, 용어집 같은 1차 자료인지 검사합니다.
- `audit.py`: 평가자가 격리 폴더 밖의 파일에 접근했는지 기록을 점검합니다.

이 폴더 바로 아래의 `tests/`는 코드를 옮기기 전에 사용한 테스트입니다. `uv run pytest`는 이 폴더의 테스트를 실행하지 않습니다.

다시 사용하려면 `tools/` 아래로 옮기고, 경로와 평가자 실행 방식을 사용할 환경에 맞게 변경합니다. 이 폴더를 옮길 때 삭제한 하위 명령(`tools.installer_loc batch`, `tools.logintool_loc export·decide·sandbox`)은 옮기기 직전 커밋 `0b39d28^`에서 볼 수 있습니다.

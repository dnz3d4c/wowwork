# 1.0 번역 검수 파이프라인(기록)

2026-11-05부터 11-14까지 WowVision 한국어판 1.0을 검수한 스크립트와 프롬프트입니다. 2026-11-19에 `tools/review/`에서 이 폴더로 옮겼습니다. 방식 설명은 `docs/review-process.md`, 회차별 결과는 `reviews/README.md`에 있습니다.

이 폴더는 실행하지 않는 기록입니다. 이전 관리자의 환경을 전제하므로 그대로는 동작하지 않습니다.

- `workflows/*.js`: Claude Code의 Workflow 스크립트입니다. 저장소 위치를 `C:/project/games/wowwork`로 적고 있습니다.
- `gpt_review.py`: Codex CLI(`codex exec`)로 GPT 평가자를 실행합니다. 이전 관리자의 Codex 프로필 `review_strict`를 사용합니다.
- `prompts/`: 평가자, 번역자 반박, 판정자에게 준 지시와 관점별 프롬프트입니다.
- 나머지 `.py`: 평가 묶음 만들기(`build_batch.py`), 판정 결과로 반영 목록 만들기(`decisions.py`), 오류 심기와 채점(`seed.py`, `score.py`), 격리 폴더(`sandbox.py`), 판정 근거 검사(`guard.py`), 접근 감사(`audit.py`)입니다.
- `tests/`: 옮기기 전에 이 코드를 검사하던 테스트입니다. `uv run pytest`는 이 폴더를 실행하지 않습니다.

다시 사용하려면 `tools/` 아래로 옮기고, 경로와 평가자 실행 방식을 자기 환경에 맞게 고칩니다. 함께 지운 하위 명령(`tools.installer_loc batch`, `tools.logintool_loc export·decide·sandbox`)은 이 폴더를 옮기기 직전 커밋에서 볼 수 있습니다.

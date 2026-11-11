# 오류 심기 검증 (2026-11-11)

- 대상: V1.0.1 새 키 66개(평가를 마친 번역)에 Claude 10개, GPT 10개를 심었다. 평가 지시는 2026-11-09 정확성 항목(의미 강도·시제)을 더한 판이다.
- 점수(`score.json`): Claude 16/20, GPT 15/20, 심지 않은 항목 지적 1건(GPT, `navigation.lua::Reverse Route`). 격리 폴더 밖 접근 0건(`tools.review.audit`).
- 무효로 본 문제 2개: `targeting.lua::Do Not Disturb`(GPT)와 `targeting.lua::Do Not Disturb (DND)`(Claude). 두 회사가 짝인 키에 같은 "방해 금지"를 각각 심어 격리 폴더 안에서는 서로 일치했고, "기존 번역과 불일치"가 존재하지 않았다. 게임 공식 문자열도 영어가 "Busy"·"DND"라 근거가 되지 않는다. 이 둘을 빼면 Claude 16/18, GPT 15/18로 둘 다 80% 이상이어서 평가 지시를 고치지 않고 실제 평가에 들어갔다.
- 두 회사가 모두 놓친 유효 문제: `targeting.lua::Quest Target` "퀘스트 목표"(퀘스트 관련 유닛 표시를 퀘스트 목표로 바꿈), `navigation.lua::Announce Remaining Waypoints` "남은 경유지 알림"(수 누락). GPT만 놓친 것: `targeting.lua::Free-for-All PvP` "개인 전투".
- 다음 검증 때 고칠 점: 두 회사의 심을 목록이 짝 키(같은 영어 구절을 공유하는 related)를 함께 고르지 않게 한다.

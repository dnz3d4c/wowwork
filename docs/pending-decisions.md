# 사용자 판단 대기

평가 절차에서 두 판정자의 결론이 갈렸거나, 번역 하나로 해결할 수 없어 사용자 결정이 필요한 항목입니다. 결정이 나면 `docs/decisions.tsv`에 옮기고 여기서 지웁니다. 결정 전까지는 괄호 안의 현재 번역을 유지합니다.

## A. 서식 문자열 안의 `of`

- `controller.lua::Page %d of %d` (현재 "%2$d페이지 중 %1$d페이지")
- `navigation.lua::Floor %d of %d` (현재 "%2$d개 층 중 %1$d층". 평가에서 두 회사가 "층 %d of %d"로 바꾸자고 합의했지만, 규칙을 잘못 적용한 것이라 보류)

2026-11-03 결정이 바꾼 것은 `L["of"]` 키 하나입니다(커밋 d5377cc). Claude 판정자는 서식 문자열은 대상이 아니라고 보고, GPT 판정자는 숫자 사이 `of`는 모두 영어로 둔다고 봅니다. 결정 목록의 범위 문구는 Claude가 커밋을 근거로 정정해 두었고, 사용자 확인이 필요합니다.

## B. 영어 복합어의 하이픈

- `navigation.lua::Auto-move to Interact Target` (현재 "상호작용 대상에게 자동 이동", GPT 판정자 제안 "자동-이동")

원문 기호 보존 규칙이 영어 철자의 하이픈에도 적용되는지의 문제입니다.

## C. 마침표로 끝나는 완결 문장 상태 알림의 문체

- `navigation.lua::The height is not confirmed. ` (현재 합니다체, 제안 "높이 확인되지 않음. ")
- `navigation.lua::Map change after the activation area; route ended. The destination is not confirmed.` (제안 "활성화 구역 이후 지도 변경; 경로 종료. 목적지 미확인.")
- `navigation.lua::The entrance has no valid proof.` (제안 "입구에 유효한 근거 없음.")
- `navigation.lua::Route ended outside the network's zones.` (제안 "네트워크 지역 밖에서 경로 종료.")

지침은 "상태 문구는 명사형, 안내 문장은 합니다체"입니다. 원문이 마침표로 끝나는 완결 문장인 상태 알림을 어느 쪽으로 볼지 갈렸습니다.

## D. `windows.lua::Picked up`

현재 "집음", GPT 판정자 제안 "집어 듦". 표현 선택입니다.

## E. 같은 키를 두 기능이 공유해서 번역 하나로 맞출 수 없는 것

AceLocale은 키 하나에 번역이 하나입니다. 다른 기능에서 같은 영어 키를 쓰면 한쪽에만 맞는 번역이 됩니다. 해결은 둘 중 하나입니다. 우선할 기능을 정하거나, 원본 코드가 키를 나누도록 upstream에 요청합니다.

- `Friends`: 친구 창 제목(공식 "친구")과 소프트 대상 강제 설정의 선택지("적/아군"). 현재 "친구"
- `Direct`: 음성 방식 선택지와 길 안내 창의 직선 경로 체크 상자. 현재 "직접"
- `Duration`: 경매 기간, 오라 지속시간, 재사용 대기 시간. 현재 "기간"(경미 지적)

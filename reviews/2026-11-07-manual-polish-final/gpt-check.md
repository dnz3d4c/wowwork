# 요청: 설명서 다듬기 마지막 반영분 대조

작업 폴더는 `C:/project/games`다. 읽기만 한다.

`wowvision-ko/WowVision` 저장소에서 `git diff 8e3a8a6 bca1778 -- docs/src/user/ko`를 실행해 바뀐 줄(36줄, 16개 파일)을 본다. 이 변경은 회귀 확인 2회차 지적 가운데 근거가 글자 그대로 확인된 것을 반영한 마지막 수정과, "알림(켬)와"처럼 괄호 뒤 조사가 어긋난 곳을 고친 것이다. 반영 근거 목록: `wowwork/reviews/2026-11-07-manual-polish-regression2/final-apply.json`.

바뀐 줄마다 다음을 확인한다.
1. 영어 원문(`docs/src/user/en`의 같은 파일)과 뜻이 같은가. 정보·조건·한정어가 빠지거나 더해지지 않았는가.
2. 화면 문구 인용은 `wowvision-ko/vision-locale/koKR`의 값과 글자가 같은가. 게임 용어는 같은 문맥의 게임 공식 문자열(`wowwork/cache/gs_enUS.csv`·`gs_koKR.csv`, 같은 ID)과 맞는가. 영어만 같고 문맥이 다른 공식 문자열은 근거가 아니다.
3. 조사, 어미, 띄어쓰기가 맞는가.
4. `wowwork/docs/decisions.tsv`의 사용자 결정과 어긋나지 않는가(특히 2026-11-07의 alert=알림은 WowVision 기능에 대한 결정이고, 게임 자체 기능의 공식 이름 "경보"는 해당하지 않는다).

스크린리더 낭독 방식은 판단하지 않는다. 취향 차이는 지적하지 않는다.

출력은 한국어로, 문제마다 (파일:줄, 현재 문장, 문제, 근거, 고칠 문장, 심각도 critical/major/minor)를 적는다. 문제가 없으면 "문제 없음"과 확인한 줄 수를 적는다.

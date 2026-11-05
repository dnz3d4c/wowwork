# 회귀 확인 (설명서)

입력 파일은 평가, 반박, 두 회사 판정을 거쳐 방금 수정된 번역이다. 이번 평가자는 관점 하나가 아니라 위 관점 목록의 네 가지(`accuracy`, `terminology`, `style`, `context`)를 **모두** 적용해 처음부터 다시 평가한다. `category`는 결함에 맞는 것을 쓴다.

추가로 반드시 확인할 것:

1. **수정 때문에 생긴 결함.** 고친 문장이 앞뒤 문장과 이어지지 않거나, 같은 문단에서 한 번은 고치고 한 번은 그대로 둔 경우.
2. **다른 설명서 파일과의 일관성.** 이 파일의 화면 문구·용어가 `wowvision-ko/WowVision/docs/src/user/ko` 아래 다른 파일과 다르면, Grep으로 다른 파일의 표기를 찾아 `evidence`에 경로와 표기를 적는다. 어느 쪽이 맞는지는 `terms`와 `wowvision-ko/vision-locale/koKR`을 기준으로 판단한다.
3. **사용자 결정 위반.** `wowwork/docs/decisions.tsv`의 결정과 어긋나는 번역.

통과 기준은 치명(critical)·중대(major) 0건이다. 경미는 보고만 한다. 취향 차이는 결함이 아니다.

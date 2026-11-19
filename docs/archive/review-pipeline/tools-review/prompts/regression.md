# 회귀 확인

입력 항목은 평가와 판정을 거쳐 방금 수정된 번역이다. 위의 네 관점(정확성, 용어, 코드 맥락, 청취와 문체)을 모두 적용해 수정 결과를 처음부터 다시 평가한다. category는 결함에 맞는 것을 쓴다.

추가로 반드시 확인할 것: **수정 때문에 기존 번역과 어긋나지 않았는지.** `wowvision-ko/vision-locale/koKR/*.lua` 전체를 Grep으로 검색해서, 같은 영어 표현이나 같은 기능을 가리키는 기존 번역과 용어·문형이 일치하는지 본다. 예: 영어 `the route goes on after it`이 들어간 다른 키들, `Stable`·`Pet` 계열, `Group Health`·`Health Monitor` 계열, `Crowd Control` 계열. 어긋나면 어느 쪽에 맞출지 `evidence`에 기존 키와 값을 적는다.

통과 기준은 치명(critical)·중대(major) 0건이다. 경미는 보고만 한다.

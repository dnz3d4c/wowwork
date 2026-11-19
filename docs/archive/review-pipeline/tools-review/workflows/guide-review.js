export const meta = {
  name: 'ko-guide-review',
  description: '테스터 설치 안내를 관점마다 Claude 1명 + GPT 1명이 서로 결과를 보지 않고 평가한다',
  phases: [{ title: 'Review', detail: '관점 3개 × Claude·GPT' }],
}

const W = 'C:/project/games/wowwork'
const P = `${W}/tools/review/prompts`
const LENSES = (args && args.lenses) || ['tester', 'facts', 'editor']
const input = `${W}/${args.input}`
const out = `${W}/${args.out}`
const FINDINGS = {
  type: 'object', required: ['findings'],
  properties: { findings: { type: 'array', items: { type: 'object',
    required: ['id', 'category', 'severity', 'quote', 'suggestion', 'problem', 'evidence'],
    properties: { id: { type: 'string' }, category: { type: 'string', enum: ['accuracy', 'terminology', 'style', 'context'] },
      severity: { type: 'string', enum: ['critical', 'major', 'minor'] }, quote: { type: 'string' },
      suggestion: { type: 'string' }, problem: { type: 'string' }, evidence: { type: 'string' } } } } },
}
const withOk = s => ({ ...s, required: [...s.required, 'ok'], properties: { ...s.properties, ok: { type: 'boolean' } } })

const claude = lens => agent(
  `너는 평가자다. ${P}/guide-review.md 와 ${P}/guide-lens-${lens}.md 를 Read로 읽고 따른다. 입력은 ${input}.\n` +
  `작업 폴더 C:/project/games 아래 wowwork와 wowvision-ko는 Read/Grep 가능. 단 wowwork/reviews 폴더는 입력 파일 외에 열지 않는다.\n` +
  `결과를 ${out}/claude-${lens}.json 에 Write로 저장하고 구조화 출력으로도 돌려준다.`,
  { label: `claude:${lens}`, phase: 'Review', schema: FINDINGS })

const gpt = lens => agent(
  `다음 명령을 Bash로 한 번 실행한다(timeout 600000).\n\n` +
  `cd ${W} && uv run python -m tools.review.gpt_review --prompt tools/review/prompts/guide-review.md --prompt tools/review/prompts/guide-lens-${lens}.md ` +
  `--batch ${input} --schema tools/review/docs-findings.schema.json --out ${out}/gpt-${lens}.json\n\n` +
  `성공하면 ${out}/gpt-${lens}.json 을 Read로 읽어 그 내용을 한 글자도 바꾸지 않고 구조화 출력으로 돌려주고 ok=true. ` +
  `실패하면 한 번만 다시 실행하고, 그래도 실패하면 ok=false, 배열은 비운다. 판단을 직접 하지 않는다.`,
  { label: `gpt:${lens}`, phase: 'Review', schema: withOk(FINDINGS), effort: 'low' }).then(r => (r && r.ok === true ? r : null))

phase('Review')
const runs = await parallel(LENSES.flatMap(l => [
  () => claude(l).then(r => r && { by: `claude-${l}`, findings: r.findings }),
  () => gpt(l).then(r => r && { by: `gpt-${l}`, findings: r.findings }),
]))
const ok = runs.filter(Boolean)
return { failedReviewers: LENSES.length * 2 - ok.length, findings: ok.flatMap(r => r.findings.map((f, i) => ({ ref: `${r.by}-${i}`, by: r.by, ...f }))) }

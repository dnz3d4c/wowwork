export const meta = {
  name: 'ko-manual-polish-calibrate',
  description: '격리 폴더에서 오류를 심은 설명서 한 파일에 다듬기 페르소나 3명 × (Claude, GPT)를 돌려 검출률과 오탐을 잰다',
  phases: [{ title: 'Review', detail: '페르소나 3 × (Claude, GPT), 격리 폴더만 사용' }],
}
const SB = args.sandbox
const W = 'C:/project/games/wowwork'
const OUT = args.outDir
if (!/^[A-Za-z]:\/[A-Za-z0-9._\/-]+$/.test(SB) || !/^[A-Za-z]:\/[A-Za-z0-9._\/-]+$/.test(OUT)) throw new Error('경로 형식 오류')
const PERSONAS = ['wow-veteran', 'manual-editor', 'newcomer']
const FINDINGS = {
  type: 'object', required: ['findings'],
  properties: { findings: { type: 'array', items: { type: 'object',
    required: ['id', 'category', 'severity', 'scope', 'quote', 'source_quote', 'suggestion', 'problem', 'evidence'],
    properties: { id: { type: 'string' }, category: { type: 'string', enum: ['accuracy', 'terminology', 'style', 'context'] },
      severity: { type: 'string', enum: ['critical', 'major', 'minor'] }, scope: { type: 'string', enum: ['file', 'kokr', 'global'] },
      quote: { type: 'string' }, source_quote: { type: 'string' }, suggestion: { type: 'string' }, problem: { type: 'string' }, evidence: { type: 'string' } } } } },
}
const claude = p => agent(
  `너는 설명서 평가자다. 작업 폴더는 ${SB} 이고, 이 폴더 밖의 파일은 절대 열거나 검색하지 않는다. 프롬프트에 나오는 상대 경로(wowwork/..., wowvision-ko/...)는 모두 ${SB} 기준이다.\n` +
  `다음 파일을 Read로 읽고 지시를 그대로 따른다.\n1. ${SB}/wowwork/tools/review/prompts/polish-base.md\n2. ${SB}/wowwork/tools/review/prompts/polish-persona-${p}.md\n3. ${SB}/batch.json (평가할 입력)\n\n` +
  `파일을 쓰지 않는다. 결과는 구조화 출력으로만 돌려준다.`,
  { label: `claude:${p}`, phase: 'Review', schema: FINDINGS })
const gpt = p => agent(
  `다음 명령을 Bash로 한 번 실행한다(timeout 600000).\n\n` +
  `cd ${W} && uv run python -m tools.review.gpt_review --prompt "${SB}/wowwork/tools/review/prompts/polish-base.md" --prompt "${SB}/wowwork/tools/review/prompts/polish-persona-${p}.md" --batch "${SB}/batch.json" --schema tools/review/polish-findings.schema.json --out "${OUT}/gpt-${p}.json" --cwd "${SB}" --events "${OUT}/gpt-${p}.events.jsonl"\n\n` +
  `성공하면 ${OUT}/gpt-${p}.json 을 Read로 읽고 내용을 한 글자도 바꾸지 않고 구조화 출력으로 돌려준다. 성공했으면 ok를 true로 한다. 실패하면 한 번만 다시 실행하고, 그래도 실패하면 ok를 false로 하고 배열은 비운다. 판단을 직접 하지 않는다.`,
  { label: `gpt:${p}`, phase: 'Review', schema: { ...FINDINGS, required: ['findings', 'ok'], properties: { ...FINDINGS.properties, ok: { type: 'boolean' } } }, effort: 'low' })
  .then(r => (r && r.ok === true ? r : null))

phase('Review')
const runs = (await parallel([
  ...PERSONAS.map(p => () => claude(p).then(r => r && { provider: 'claude', persona: p, findings: r.findings })),
  ...PERSONAS.map(p => () => gpt(p).then(r => r && { provider: 'gpt', persona: p, findings: r.findings })),
])).filter(Boolean)
const failed = PERSONAS.length * 2 - runs.length
if (failed) log(`평가자 실패 ${failed}명: 이 검증은 무효다`)
return { failedReviewers: failed, result: runs }

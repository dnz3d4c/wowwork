export const meta = {
  name: 'ko-manual-regression',
  description: '설명서 파일마다 처음 보는 Claude 1명 + GPT 1명이 네 관점 전부로 다시 평가한다 (절차 5단계)',
  phases: [{ title: 'Regression', detail: '파일마다 Claude 1 + GPT 1, 서로 결과 비공개' }],
}

const W = 'C:/project/games/wowwork'
const P = `${W}/tools/review/prompts`
const PROMPTS = ['manual-review.md', 'manual-regression.md']
const OUT = args.outDir
const dirOf = rel => `${W}/${OUT}/${rel.replace(/\.md$/, '')}`
const BATCH = (rel, who) => `cd ${W} && uv run python -m tools.manual batch ${rel} ${dirOf(rel)}/${who}-input.json`

const FINDINGS = {
  type: 'object', required: ['findings'],
  properties: { findings: { type: 'array', items: { type: 'object',
    required: ['id', 'category', 'severity', 'quote', 'suggestion', 'problem', 'evidence'],
    properties: { id: { type: 'string' }, category: { type: 'string', enum: ['accuracy', 'terminology', 'style', 'context'] },
      severity: { type: 'string', enum: ['critical', 'major', 'minor'] }, quote: { type: 'string' },
      suggestion: { type: 'string' }, problem: { type: 'string' }, evidence: { type: 'string' } } } } },
}
const withOk = s => ({ ...s, required: [...s.required, 'ok'], properties: { ...s.properties, ok: { type: 'boolean' } } })

const claude = rel => agent(
  `너는 번역 평가자다. 다음 파일을 순서대로 Read로 읽고 따른다.\n` + PROMPTS.map((f, i) => `${i + 1}. ${P}/${f}`).join('\n') + `\n` +
  `입력은 Bash로 \`${BATCH(rel, 'claude')}\` 를 실행해 만든 뒤 Read로 읽는다. ` +
  `wowwork/reviews 폴더는 열지 않는다. 결과를 ${dirOf(rel)}/claude.json 에 Write로 저장하고 구조화 출력으로도 돌려준다.`,
  { label: `claude:${rel}`, phase: 'Regression', schema: FINDINGS })

const gpt = rel => agent(
  `먼저 Bash로 \`${BATCH(rel, 'gpt')}\` 를 실행한다. 그다음 다음 명령을 Bash로 한 번 실행한다(timeout 600000).\n\n` +
  `cd ${W} && uv run python -m tools.review.gpt_review ${PROMPTS.map(f => `--prompt tools/review/prompts/${f}`).join(' ')} ` +
  `--batch ${dirOf(rel)}/gpt-input.json --schema tools/review/docs-findings.schema.json --out ${dirOf(rel)}/gpt.json\n\n` +
  `성공하면 ${dirOf(rel)}/gpt.json 을 Read로 읽어 그 내용을 한 글자도 바꾸지 않고 구조화 출력으로 돌려주고 ok=true. ` +
  `실패하면 한 번만 다시 실행하고, 그래도 실패하면 ok=false, 배열은 비운다. 판단을 직접 하지 않는다.`,
  { label: `gpt:${rel}`, phase: 'Regression', schema: withOk(FINDINGS), effort: 'low' }).then(r => (r && r.ok === true ? r : null))

async function check(rel) {
  const [c, g] = await parallel([() => claude(rel), () => gpt(rel)])
  const all = [...((c && c.findings) || []).map(f => ({ by: 'claude', ...f })), ...((g && g.findings) || []).map(f => ({ by: 'gpt', ...f }))]
  // 평가자 하나라도 실패하면 통과가 아니다.
  return { file: rel, passed: !!c && !!g && all.every(f => f.severity === 'minor'), claudeOk: !!c, gptOk: !!g,
    blocking: all.filter(f => f.severity !== 'minor'), minor: all.filter(f => f.severity === 'minor').length }
}

phase('Regression')
const results = (await parallel(args.files.map(rel => () => check(rel)))).filter(Boolean)
const failed = results.filter(r => !r.passed)
log(`통과 ${results.length - failed.length}/${args.files.length}, 중대 이상 ${failed.reduce((n, r) => n + r.blocking.length, 0)}건`)
return { total: args.files.length, passed: results.length - failed.length, failed }

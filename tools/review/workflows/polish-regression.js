export const meta = {
  name: 'ko-manual-polish-regression',
  description: '다듬기를 거친 설명서 파일마다 처음 보는 Claude 1명 + GPT 1명이 바뀐 줄을 중심으로 다시 평가한다 (절차 5단계)',
  phases: [{ title: 'Regression', detail: '파일마다 Claude 1 + GPT 1, 서로 결과 비공개' }],
}

const W = 'C:/project/games/wowwork'
const P = `${W}/tools/review/prompts`
const PROMPTS = ['polish-base.md', 'polish-regression.md']
const OUT = args.outDir
const BASE = args.base
if (!/^reviews\/[A-Za-z0-9._-]+$/.test(OUT)) throw new Error(`outDir 형식 오류: ${OUT}`)
if (!/^[0-9a-f]{7,40}(~[0-9]+)?$/.test(BASE)) throw new Error(`base 형식 오류: ${BASE}`)
for (const f of args.files) if (!/^[a-z0-9][a-z0-9_-]*(\/[a-z0-9_-]+)*\.md$/.test(f)) throw new Error(`파일 형식 오류: ${f}`)
const dirOf = rel => `${W}/${OUT}/${rel.replace(/\.md$/, '')}`
const INPUT = (rel, who) => `cd ${W} && uv run python -m tools.review.polish_regression_input ${rel} ${BASE} ${dirOf(rel)}/${who}-input.json`

const FINDINGS = {
  type: 'object', required: ['findings'],
  properties: { findings: { type: 'array', items: { type: 'object',
    required: ['id', 'category', 'severity', 'scope', 'quote', 'source_quote', 'suggestion', 'problem', 'evidence'],
    properties: { id: { type: 'string' }, category: { type: 'string', enum: ['accuracy', 'terminology', 'style', 'context'] },
      severity: { type: 'string', enum: ['critical', 'major', 'minor'] }, scope: { type: 'string', enum: ['file', 'kokr', 'global'] },
      quote: { type: 'string' }, source_quote: { type: 'string' }, suggestion: { type: 'string' }, problem: { type: 'string' }, evidence: { type: 'string' } } } } },
}
const withOk = s => ({ ...s, required: [...s.required, 'ok'], properties: { ...s.properties, ok: { type: 'boolean' } } })

const claude = rel => agent(
  `너는 설명서 회귀 확인 평가자다. 다음 파일을 순서대로 Read로 읽고 따른다.\n` + PROMPTS.map((f, i) => `${i + 1}. ${P}/${f}`).join('\n') + `\n` +
  `입력은 Bash로 \`${INPUT(rel, 'claude')}\` 를 실행해 만든 뒤 Read로 읽는다. ` +
  `wowwork/reviews 폴더는 열지 않는다. 결과를 ${dirOf(rel)}/claude.json 에 Write로 저장하고 구조화 출력으로도 돌려준다.`,
  { label: `claude:${rel}`, phase: 'Regression', schema: FINDINGS })

const gpt = rel => agent(
  `먼저 Bash로 \`${INPUT(rel, 'gpt')}\` 를 실행한다. 그다음 다음 명령을 Bash로 한 번 실행한다(timeout 600000).\n\n` +
  `cd ${W} && uv run python -m tools.review.gpt_review ${PROMPTS.map(f => `--prompt tools/review/prompts/${f}`).join(' ')} ` +
  `--batch ${dirOf(rel)}/gpt-input.json --schema tools/review/polish-findings.schema.json --out ${dirOf(rel)}/gpt.json\n\n` +
  `성공하면 ${dirOf(rel)}/gpt.json 을 Read로 읽어 그 내용을 한 글자도 바꾸지 않고 구조화 출력으로 돌려주고 ok=true. ` +
  `실패하면 한 번만 다시 실행하고, 그래도 실패하면 ok=false, 배열은 비운다. 판단을 직접 하지 않는다.`,
  { label: `gpt:${rel}`, phase: 'Regression', schema: withOk(FINDINGS), effort: 'low' }).then(r => (r && r.ok === true ? r : null))

async function check(rel) {
  const [c, g] = await parallel([() => claude(rel), () => gpt(rel)])
  const all = [...((c && c.findings) || []).map(f => ({ by: 'claude', ...f })), ...((g && g.findings) || []).map(f => ({ by: 'gpt', ...f }))]
  const fileScope = all.filter(f => f.scope === 'file')
  // 평가자 하나라도 실패하면 통과가 아니다. koKR·전체 용어 지적은 사용자 결정 목록으로 간다.
  return { file: rel, passed: !!c && !!g && fileScope.every(f => f.severity === 'minor'), claudeOk: !!c, gptOk: !!g,
    blocking: fileScope.filter(f => f.severity !== 'minor'), minor: fileScope.filter(f => f.severity === 'minor'),
    proposals: all.filter(f => f.scope !== 'file') }
}

phase('Regression')
const results = (await parallel(args.files.map(rel => () => check(rel)))).filter(Boolean)
const failed = results.filter(r => !r.passed)
const broken = results.filter(r => !r.claudeOk || !r.gptOk).map(r => r.file)
if (broken.length) log(`평가자 실패로 미완료: ${broken.join(', ')}`)
log(`통과 ${results.length - failed.length}/${args.files.length}, 중대 이상 ${failed.reduce((n, r) => n + r.blocking.length, 0)}건`)
return { total: args.files.length, passed: results.length - failed.length, broken, failed, passedFiles: results.filter(r => r.passed).map(r => ({ file: r.file, minor: r.minor, proposals: r.proposals })) }

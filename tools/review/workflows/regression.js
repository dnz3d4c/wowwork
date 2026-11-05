export const meta = {
  name: 'ko-review-regression',
  description: '수정된 번역을 처음 보는 Claude 1명 + GPT 1명이 전 관점과 기존 번역 일관성으로 다시 평가한다',
  phases: [{ title: 'Regression', detail: 'Claude 1 + GPT 1, 서로 결과 비공개' }],
}
const W = 'C:/project/games/wowwork'
const P = `${W}/tools/review/prompts`
// 대상별 추가 규칙(예: installer.md)은 공통 규칙 바로 다음에 읽는다.
const FILES = ['common.md', ...((args && args.extraPrompts) || []), 'lens-accuracy.md', 'lens-terminology.md', 'lens-context.md', 'lens-listening.md', 'regression.md']
const FINDINGS = {
  type: 'object', required: ['findings'],
  properties: { findings: { type: 'array', items: { type: 'object',
    required: ['id', 'category', 'severity', 'problem', 'evidence', 'suggestion'],
    properties: { id: { type: 'string' }, category: { type: 'string', enum: ['accuracy', 'terminology', 'context', 'listening', 'style'] },
      severity: { type: 'string', enum: ['critical', 'major', 'minor'] }, problem: { type: 'string' },
      evidence: { type: 'string' }, suggestion: { type: 'string' } } } } },
}
const batch = `${W}/${args.batch}`
const out = `${W}/${args.out}`
phase('Regression')
const [c, g] = await parallel([
  () => agent(
    `너는 번역 평가자다. 다음 파일을 순서대로 Read로 읽고 지시를 따른다. 공통 규칙은 첫 파일이고, 이번에는 관점 하나가 아니라 모든 관점을 적용한다.\n` +
    FILES.map((f, i) => `${i + 1}. ${P}/${f}`).join('\n') + `\n입력: ${batch}\n\n` +
    `작업 폴더 C:/project/games 아래 wowwork와 wowvision-ko는 Read/Grep 가능. 단 wowwork/reviews 폴더는 열지 않는다.\n` +
    `결과 JSON을 ${out}/claude.json 에 Write로 저장하고 같은 내용을 구조화 출력으로 돌려준다.`,
    { label: 'claude:regression', phase: 'Regression', schema: FINDINGS }),
  () => agent(
    `다음 명령을 Bash로 한 번 실행한다(timeout 600000).\n\n` +
    `cd ${W} && uv run python -m tools.review.gpt_review ` + FILES.map(f => `--prompt tools/review/prompts/${f}`).join(' ') +
    ` --batch ${batch} --schema tools/review/findings.schema.json --out ${out}/gpt.json\n\n` +
    `성공하면 ${out}/gpt.json 을 Read로 읽고 내용을 한 글자도 바꾸지 않고 구조화 출력으로 돌려준다. 성공했으면 ok를 true로 한다. 실패하면 한 번만 다시 실행하고, 그래도 실패하면 ok를 false로 하고 배열은 비운다. 판단을 직접 하지 않는다.`,
    { label: 'gpt:regression', phase: 'Regression', schema: { ...FINDINGS, required: ['findings', 'ok'], properties: { ...FINDINGS.properties, ok: { type: 'boolean' } } }, effort: 'low' })
    .then(r => (r && r.ok === true ? r : null)),
])
const all = [...((c && c.findings) || []).map(f => ({ by: 'claude', ...f })), ...((g && g.findings) || []).map(f => ({ by: 'gpt', ...f }))]
// 평가자 하나라도 실패하면 통과가 아니다(passed=false).
return { passed: !!c && !!g && all.every(f => f.severity === 'minor'), claudeOk: !!c, gptOk: !!g, blocking: all.filter(f => f.severity !== 'minor'), minor: all.filter(f => f.severity === 'minor').map(f => `${f.by} ${f.id.split('::')[1].slice(0, 40)}: ${f.problem.slice(0, 120)}`) }

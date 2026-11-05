export const meta = {
  name: 'ko-review-full',
  description: '번역 묶음마다 Claude 4 + GPT 4 블라인드 평가 → 번역자 반박 → 교차 회사 판정을 돌려 확정 번역을 만든다',
  phases: [
    { title: 'Review', detail: '묶음마다 Claude 4 lens + GPT 4 lens' },
    { title: 'Rebut', detail: '번역자가 지적마다 수용 또는 반박' },
    { title: 'Judge', detail: 'Claude 지적은 GPT가, GPT 지적은 Claude가 판정' },
  ],
}

const W = 'C:/project/games/wowwork'
const P = `${W}/tools/review/prompts`
const LENSES = ['accuracy', 'terminology', 'context', 'listening']
const FINDINGS = {
  type: 'object', required: ['findings'],
  properties: { findings: { type: 'array', items: { type: 'object',
    required: ['id', 'category', 'severity', 'problem', 'evidence', 'suggestion'],
    properties: { id: { type: 'string' }, category: { type: 'string', enum: ['accuracy', 'terminology', 'context', 'listening', 'style'] },
      severity: { type: 'string', enum: ['critical', 'major', 'minor'] }, problem: { type: 'string' },
      evidence: { type: 'string' }, suggestion: { type: 'string' } } } } },
}
const REBUT = {
  type: 'object', required: ['responses'],
  properties: { responses: { type: 'array', items: { type: 'object', required: ['id', 'action', 'final_ko', 'reason'],
    properties: { id: { type: 'string' }, action: { type: 'string', enum: ['accept', 'dispute'] },
      final_ko: { type: 'string' }, reason: { type: 'string' } } } } },
}
const VERDICTS = {
  type: 'object', required: ['verdicts'],
  properties: { verdicts: { type: 'array', items: { type: 'object', required: ['ref', 'uphold', 'final_ko', 'reason', 'evidence_sources'],
    properties: { ref: { type: 'string' }, uphold: { type: 'boolean' }, final_ko: { type: 'string' }, reason: { type: 'string' },
      evidence_sources: { type: 'array', items: { type: 'string' } } } } } },
}
// 판정 근거 검사(허용 자료인지)는 tools/review/decisions.py 의 split_invalid 가 한다. 여기서는 근거를 기록으로 넘기기만 한다.

function claudeReviewer(batch, out, lens) {
  return agent(
    `너는 번역 평가자다. 다음 파일을 Read로 읽고 그 지시를 그대로 따른다.\n` +
    `1. ${P}/common.md (역할과 규칙)\n2. ${P}/lens-${lens}.md (네 관점)\n3. ${batch} (평가할 입력, items 배열)\n\n` +
    `작업 폴더: C:/project/games (wowwork, wowvision-ko 아래 파일은 근거 확인용으로 Read/Grep 가능). ` +
    `reviews 폴더의 다른 평가 결과 파일은 열지 않는다.\n` +
    `평가가 끝나면 결과 JSON({"findings": [...]})을 ${out}/claude-${lens}.json 에 Write로 저장하고, 같은 내용을 구조화 출력으로 돌려준다.`,
    { label: `claude:${lens}`, phase: 'Review', schema: FINDINGS })
}

// GPT 실행 에이전트는 성공 여부를 따로 돌려준다. 빈 결과를 성공으로 오인하지 않기 위해서다.
function withOk(schema) {
  return { ...schema, required: [...schema.required, 'ok'], properties: { ...schema.properties, ok: { type: 'boolean' } } }
}

function gptRun(promptFiles, inputPath, schemaFile, outPath, schema, label, phaseName, writePayload) {
  const pre = writePayload
    ? `먼저 아래 JSON을 ${inputPath} 에 Write로 그대로 저장한다(한 글자도 바꾸지 않는다).\n\n${writePayload}\n\n그다음 `
    : ''
  const prompts = promptFiles.map(f => `--prompt tools/review/prompts/${f}`).join(' ')
  return agent(
    pre + `다음 명령을 Bash로 한 번 실행한다(timeout 600000). GPT를 실행하고 결과를 파일로 남긴다.\n\n` +
    `cd ${W} && uv run python -m tools.review.gpt_review ${prompts} --batch ${inputPath} --schema tools/review/${schemaFile} --out ${outPath}\n\n` +
    `성공하면 ${outPath} 를 Read로 읽고 그 내용을 한 글자도 바꾸지 않고 구조화 출력으로 돌려준다. ` +
    `성공했으면 ok를 true로 한다. 실패하면 한 번만 다시 실행하고, 그래도 실패하면 ok를 false로 하고 배열은 비운다. 판단을 직접 하지 않는다.`,
    { label, phase: phaseName, schema: withOk(schema), effort: 'low' })
    .then(r => (r && r.ok === true ? r : null)) // 실패는 빈 결과가 아니라 null(평가자 실패)
}

async function runBatch(b) {
  const batch = `${W}/${b.path}`
  const out = `${W}/${b.out}`
  const runs = (await parallel([
    ...LENSES.map(l => () => claudeReviewer(batch, out, l).then(r => r && { provider: 'claude', lens: l, findings: r.findings })),
    ...LENSES.map(l => () => gptRun(['common.md', `lens-${l}.md`], batch, 'findings.schema.json', `${out}/gpt-${l}.json`,
      FINDINGS, `gpt:${l}`, 'Review', null).then(r => r && { provider: 'gpt', lens: l, findings: r.findings })),
  ])).filter(Boolean)
  const failed = 8 - runs.length

  // 항목별로 묶는다
  const groups = {}
  for (const r of runs) for (const f of r.findings) {
    const g = groups[f.id] || (groups[f.id] = { id: f.id, providers: [], findings: [] })
    if (!g.providers.includes(r.provider)) g.providers.push(r.provider)
    g.findings.push({ by: `${r.provider}-${r.lens}`, ...f })
  }
  const list = Object.values(groups).map(g => ({ ...g, consensus: g.providers.length === 2 }))
  if (!list.length) return { batch: b.path, failedReviewers: failed, decisions: [], escalations: [] }

  const rebut = await agent(
    `너는 이 번역의 번역자다. ${P}/rebut.md 를 Read로 읽고 따른다. 번역 지침은 ${W}/docs/translation-guide.md, 원문·번역·코드 사용처는 ${batch} 에 있다.\n\n` +
    `아래는 항목별로 묶은 평가자 지적이다. 항목(id)마다 응답 하나를 낸다. consensus=true인 항목은 두 회사 평가자가 모두 지적한 것이므로 반드시 accept하고, 지적들을 반영한 가장 좋은 번역을 final_ko로 확정한다. ` +
    `consensus=false인 항목은 지적이 맞으면 accept, 틀리면 dispute(final_ko는 현재 번역 그대로)한다. 같은 항목의 지적이 여럿이면 함께 고려해 최종 번역 하나로 정한다.\n\n` +
    `결과를 ${out}/rebut.json 에 Write로 저장하고 구조화 출력으로도 돌려준다.\n\n` + JSON.stringify(list, null, 1),
    { label: 'translator', phase: 'Rebut', schema: REBUT })
  const resp = Object.fromEntries((rebut ? rebut.responses : []).map(r => [r.id, r]))

  const disputed = list.filter(g => resp[g.id] && resp[g.id].action === 'dispute')
  const escalations = disputed.filter(g => g.consensus).map(g => ({ id: g.id, why: '두 회사가 모두 지적했는데 번역자가 반박', reason: resp[g.id].reason }))
  const toGpt = disputed.filter(g => !g.consensus && g.providers[0] === 'claude')
  const toClaude = disputed.filter(g => !g.consensus && g.providers[0] === 'gpt')
  const payload = gs => gs.map(g => ({ ref: g.id, findings: g.findings, translator: resp[g.id] }))

  const [gj, cj] = await parallel([
    () => toGpt.length ? gptRun(['common.md', 'judge.md'], `${out}/judge-gpt-input.json`, 'verdicts.schema.json', `${out}/judge-gpt.json`,
      VERDICTS, 'gpt:judge', 'Judge', JSON.stringify({ batch_file: b.path, items: payload(toGpt) }, null, 1)) : Promise.resolve({ verdicts: [] }),
    () => toClaude.length ? agent(
      `${P}/common.md 와 ${P}/judge.md 를 Read로 읽고 판정자로서 따른다. 원문·번역·코드 사용처는 ${batch}. 아래 각 항목(ref=항목 id)에 대해 판정한다.\n` +
      `결과를 ${out}/judge-claude.json 에 Write로 저장하고 구조화 출력으로도 돌려준다.\n\n` + JSON.stringify(payload(toClaude), null, 1),
      { label: 'claude:judge', phase: 'Judge', schema: VERDICTS }) : Promise.resolve({ verdicts: [] }),
  ])
  const verdict = Object.fromEntries([...((gj && gj.verdicts) || []), ...((cj && cj.verdicts) || [])].map(v => [v.ref, v]))

  const decisions = []
  for (const g of list) {
    const r = resp[g.id]
    if (!r) { escalations.push({ id: g.id, why: '번역자 응답 없음' }); continue }
    if (r.action === 'accept') { decisions.push({ id: g.id, final_ko: r.final_ko, how: g.consensus ? 'consensus' : 'accepted', sev: g.findings.map(f => f.severity) }); continue }
    if (g.consensus) continue
    const v = verdict[g.id]
    if (!v) { escalations.push({ id: g.id, why: '판정 없음' }); continue }
    decisions.push({ id: g.id, final_ko: v.uphold ? v.final_ko : r.final_ko, how: v.uphold ? `upheld-by-${g.providers[0] === 'claude' ? 'gpt' : 'claude'}` : 'dispute-won', reason: v.reason, evidence: v.evidence_sources || [], sev: g.findings.map(f => f.severity) })
  }
  return { batch: b.path, failedReviewers: failed, findings: runs.reduce((n, r) => n + r.findings.length, 0), decisions, escalations }
}

phase('Review')
const results = await parallel(args.batches.map(b => () => runBatch(b)))
return results

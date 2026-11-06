export const meta = {
  name: 'ko-manual-polish',
  description: '설명서 파일마다 게임 설명서 적합성 페르소나 3명을 Claude·GPT가 따로 평가 → 편집자 반영·반박 → 두 회사 판정 → 반영. 화면 문구·전체 용어 지적은 모아서 사용자 결정으로 넘긴다',
  phases: [
    { title: 'Review', detail: '파일마다 페르소나 3 × (Claude, GPT)' },
    { title: 'Fix', detail: '편집자 반영·반박, 두 회사 판정, 판정 반영' },
  ],
}

const W = 'C:/project/games/wowwork'
const P = `${W}/tools/review/prompts`
const EN = 'C:/project/games/wowvision-ko/WowVision/docs/src/user/en'
const KO = 'C:/project/games/wowvision-ko/WowVision/docs/src/user/ko'
const PERSONAS = ['wow-veteran', 'manual-editor', 'newcomer']
const OUT = args.outDir
const dirOf = rel => `${W}/${OUT}/${rel.replace(/\.md$/, '')}`
const CHECK = rel => `cd ${W} && uv run python -m tools.manual check ${rel}`
const BATCH = (rel, who) => `cd ${W} && uv run python -m tools.manual batch ${rel} ${dirOf(rel)}/${who}-input.json`

const FINDINGS = {
  type: 'object', required: ['findings'],
  properties: { findings: { type: 'array', items: { type: 'object',
    required: ['id', 'category', 'severity', 'scope', 'quote', 'suggestion', 'problem', 'evidence'],
    properties: { id: { type: 'string' }, category: { type: 'string', enum: ['accuracy', 'terminology', 'style', 'context'] },
      severity: { type: 'string', enum: ['critical', 'major', 'minor'] }, scope: { type: 'string', enum: ['file', 'kokr', 'global'] },
      quote: { type: 'string' }, suggestion: { type: 'string' }, problem: { type: 'string' }, evidence: { type: 'string' } } } } },
}
const withOk = s => ({ ...s, required: [...s.required, 'ok'], properties: { ...s.properties, ok: { type: 'boolean' } } })
const DONE = { type: 'object', required: ['ok', 'remaining'], properties: { ok: { type: 'boolean' }, remaining: { type: 'array', items: { type: 'string' } } } }
const RESP = {
  type: 'object', required: ['responses'],
  properties: { responses: { type: 'array', items: { type: 'object', required: ['ref', 'action', 'reason'],
    properties: { ref: { type: 'string' }, action: { type: 'string', enum: ['applied', 'dispute'] }, reason: { type: 'string' } } } } },
}
const VERDICTS = {
  type: 'object', required: ['verdicts'],
  properties: { verdicts: { type: 'array', items: { type: 'object', required: ['ref', 'uphold', 'final_ko', 'reason', 'evidence_sources'],
    properties: { ref: { type: 'string' }, uphold: { type: 'boolean' }, final_ko: { type: 'string' }, reason: { type: 'string' },
      evidence_sources: { type: 'array', items: { type: 'string' } } } } } },
}

const promptFiles = persona => ['polish-base.md', `polish-persona-${persona}.md`]

// ── 평가 ────────────────────────────────────────────────────────────────
const claudeReview = (rel, persona) => agent(
  `너는 설명서 평가자다. 다음 파일을 순서대로 Read로 읽고 따른다.\n` +
  promptFiles(persona).map((f, i) => `${i + 1}. ${P}/${f}`).join('\n') + `\n` +
  `입력은 Bash로 \`${BATCH(rel, `claude-${persona}`)}\` 를 실행해 만든 뒤 Read로 읽는다. ` +
  `wowwork/reviews 폴더는 열지 않는다. 결과를 ${dirOf(rel)}/claude-${persona}.json 에 Write로 저장하고 구조화 출력으로도 돌려준다.`,
  { label: `claude:${persona}:${rel}`, phase: 'Review', schema: FINDINGS })

const gptRun = (label, phaseName, pre, prompts, input, schemaFile, out, schema) => agent(
  pre + `다음 명령을 Bash로 한 번 실행한다(timeout 600000).\n\n` +
  `cd ${W} && uv run python -m tools.review.gpt_review ${prompts.map(f => `--prompt tools/review/prompts/${f}`).join(' ')} ` +
  `--batch ${input} --schema tools/review/${schemaFile} --out ${out}\n\n` +
  `성공하면 ${out} 을 Read로 읽어 그 내용을 한 글자도 바꾸지 않고 구조화 출력으로 돌려주고 ok=true. ` +
  `실패하면 한 번만 다시 실행하고, 그래도 실패하면 ok=false, 배열은 비운다. 판단을 직접 하지 않는다.`,
  { label, phase: phaseName, schema: withOk(schema), effort: 'low' }).then(r => (r && r.ok === true ? r : null))

const gptReview = (rel, persona) => gptRun(`gpt:${persona}:${rel}`, 'Review',
  `먼저 Bash로 \`${BATCH(rel, `gpt-${persona}`)}\` 를 실행한다. 그다음 `,
  promptFiles(persona), `${dirOf(rel)}/gpt-${persona}-input.json`, 'polish-findings.schema.json',
  `${dirOf(rel)}/gpt-${persona}.json`, FINDINGS)

const norm = s => s.replace(/\s+/g, ' ').trim()
const overlaps = (a, b) => { const x = norm(a), y = norm(b); return x.length > 0 && y.length > 0 && (x.includes(y) || y.includes(x)) }

async function reviewAndFix(rel) {
  const runs = (await parallel([
    ...PERSONAS.map(p => () => claudeReview(rel, p).then(r => r && { provider: 'claude', persona: p, findings: r.findings })),
    ...PERSONAS.map(p => () => gptReview(rel, p).then(r => r && { provider: 'gpt', persona: p, findings: r.findings })),
  ])).filter(Boolean)
  const failed = PERSONAS.length * 2 - runs.length
  const every = runs.flatMap(r => r.findings.map((f, i) => ({ ...f, by: `${r.provider}-${r.persona}`, provider: r.provider, ref: `${rel}#${r.provider}-${r.persona}-${i}` })))
  // 화면 문구(koKR)·전체 용어 방침은 이 파일에서 고치지 않는다. 모아서 사용자 결정으로 넘긴다.
  const proposals = every.filter(f => f.scope !== 'file')
  const all = every.filter(f => f.scope === 'file')
  for (const f of all) f.consensus = all.some(g => g.provider !== f.provider && overlaps(f.quote, g.quote))
  const base = { file: rel, failedReviewers: failed, findings: all.length, proposals }
  if (!all.length) return { ...base, applied: 0, upheld: 0, disputeWon: 0, escalations: [] }

  // 편집자: 두 회사 합의 지적은 반드시 반영, 나머지는 반영하거나 반박
  const resp = await agent(
    `너는 이 설명서 파일의 편집자다. ${P}/polish-base.md 와 ${P}/rebut.md 를 Read로 읽는다. polish-base.md의 "바꾸지 않는 것"을 지킨다. ` +
    `번역문은 ${KO}/${rel}, 원문은 ${EN}/${rel}.\n` +
    `아래 지적마다 판단한다. consensus=true인 것은 두 회사 평가자가 모두 지적한 곳이므로 반드시 반영한다(수정안은 지적들을 보고 가장 나은 것으로 정한다). ` +
    `나머지는 지적이 맞으면 반영하고(action=applied), 틀렸거나 취향 차이거나 뜻을 바꾸면 고치지 않고 근거를 든다(action=dispute). ` +
    `반영은 Edit로 quote를 suggestion(또는 지적들을 반영한 더 나은 문장)으로 바꾼다. 같은 곳을 가리키는 지적이 여럿이면 함께 반영한다. ` +
    `화면 문구 인용(따옴표 안 문구, 메뉴·설정 이름)은 koKR 값과 글자가 같아야 하므로 바꾸지 않는다.\n` +
    `끝나면 \`${CHECK(rel)}\` 로 기계 검사를 통과하는지 확인하고, 깨졌으면 고친다. ` +
    `결과를 ${dirOf(rel)}/rebut.json 에 Write로 저장하고 구조화 출력으로도 돌려준다.\n\n` +
    JSON.stringify(all.map(({ ref, consensus, category, severity, quote, suggestion, problem, evidence, by }) => ({ ref, consensus, by, category, severity, quote, suggestion, problem, evidence })), null, 1),
    { label: `editor:${rel}`, phase: 'Fix', schema: RESP })
  const byRef = Object.fromEntries(((resp && resp.responses) || []).map(r => [r.ref, r]))
  const disputed = all.filter(f => byRef[f.ref] && byRef[f.ref].action === 'dispute' && !f.consensus)
  const escalations = all.filter(f => (byRef[f.ref] && byRef[f.ref].action === 'dispute' && f.consensus) || !byRef[f.ref])
    .map(f => ({ ref: f.ref, why: !byRef[f.ref] ? '편집자 응답 없음' : '합의 지적을 편집자가 반박', quote: f.quote, suggestion: f.suggestion }))
  const applied = Object.values(byRef).filter(r => r.action === 'applied').length
  if (!disputed.length) return { ...base, applied, upheld: 0, disputeWon: 0, escalations }

  // 두 회사 판정 (서로의 결론 비공개)
  const payload = disputed.map(f => ({ ref: f.ref, file: rel, finding: { category: f.category, severity: f.severity, quote: f.quote, suggestion: f.suggestion, problem: f.problem, evidence: f.evidence }, editor: byRef[f.ref] }))
  const [gj, cj] = await parallel([
    () => gptRun(`gpt:judge:${rel}`, 'Fix',
      `먼저 아래 JSON을 ${dirOf(rel)}/judge-gpt-input.json 에 Write로 그대로 저장한다.\n\n${JSON.stringify({ file: rel, en_path: `wowvision-ko/WowVision/docs/src/user/en/${rel}`, ko_path: `wowvision-ko/WowVision/docs/src/user/ko/${rel}`, items: payload }, null, 1)}\n\n그다음 `,
      ['polish-base.md', 'judge.md'], `${dirOf(rel)}/judge-gpt-input.json`, 'verdicts.schema.json', `${dirOf(rel)}/judge-gpt.json`, VERDICTS),
    () => agent(
      `${P}/polish-base.md 와 ${P}/judge.md 를 Read로 읽고 판정자로서 따른다. 원문 ${EN}/${rel}, 번역문 ${KO}/${rel}. ` +
      `아래 항목마다 판정한다. uphold=true면 final_ko에 quote를 대신할 문장을 적는다. 결과를 ${dirOf(rel)}/judge-claude.json 에 Write로 저장하고 구조화 출력으로도 돌려준다.\n\n` +
      JSON.stringify(payload, null, 1),
      { label: `claude:judge:${rel}`, phase: 'Fix', schema: VERDICTS }),
  ])
  const gv = Object.fromEntries(((gj && gj.verdicts) || []).map(v => [v.ref, v]))
  const cv = Object.fromEntries(((cj && cj.verdicts) || []).map(v => [v.ref, v]))
  const upheld = []
  let disputeWon = 0
  for (const f of disputed) {
    const a = gv[f.ref], c = cv[f.ref]
    if (!a || !c) { escalations.push({ ref: f.ref, why: `판정 누락 (gpt ${!!a}, claude ${!!c})`, quote: f.quote, suggestion: f.suggestion }); continue }
    if (a.uphold !== c.uphold) { escalations.push({ ref: f.ref, why: '두 판정자의 결론이 다름', quote: f.quote, suggestion: f.suggestion, gpt: a.reason, claude: c.reason }); continue }
    // 지적한 회사가 아닌 쪽 판정자의 문장을 쓴다
    if (a.uphold) upheld.push({ ref: f.ref, quote: f.quote, final_ko: (f.provider === 'claude' ? a : c).final_ko, evidence: [...(a.evidence_sources || []), ...(c.evidence_sources || [])] })
    else disputeWon++
  }
  if (upheld.length) {
    await agent(
      `${KO}/${rel} 에서 아래 각 항목의 quote를 final_ko로 Edit로 바꾼다. quote가 정확히 보이지 않으면 가장 가까운 부분을 찾아 같은 뜻으로 고친다. ` +
      `끝나면 \`${CHECK(rel)}\` 를 통과하는지 확인하고, 깨졌으면 원문 구조에 맞게 고친다. ok와 remaining을 돌려준다.\n\n` + JSON.stringify(upheld, null, 1),
      { label: `fixer:${rel}`, phase: 'Fix', schema: DONE })
  }
  return { ...base, applied, upheld: upheld.length, disputeWon, escalations, upheldItems: upheld }
}

phase('Review')
const reviewed = (await pipeline(args.files, rel => reviewAndFix(rel))).filter(Boolean)
log(`파일 ${reviewed.length}/${args.files.length}, 지적 ${reviewed.reduce((n, r) => n + r.findings, 0)}건, 사용자 결정 후보 ${reviewed.reduce((n, r) => n + r.proposals.length, 0)}건`)
return { reviewed }

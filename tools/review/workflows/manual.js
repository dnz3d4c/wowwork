export const meta = {
  name: 'ko-manual',
  description: '설명서 파일마다 번역 → 앵커 정리 → Claude 4 + GPT 4 블라인드 평가 → 번역자 반영·반박 → 두 회사 판정 → 수정과 기계 검사',
  phases: [
    { title: 'Translate', detail: '파일마다 번역자 1명, 기계 검사 통과까지' },
    { title: 'Anchors', detail: '모든 번역이 끝난 뒤 남은 앵커 고치기' },
    { title: 'Review', detail: '파일마다 Claude 4 + GPT 4' },
    { title: 'Fix', detail: '번역자 반영·반박, 두 회사 판정, 판정 반영' },
  ],
}

const W = 'C:/project/games/wowwork'
const P = `${W}/tools/review/prompts`
const EN = 'C:/project/games/wowvision-ko/WowVision/docs/src/user/en'
const KO = 'C:/project/games/wowvision-ko/WowVision/docs/src/user/ko'
const LENSES = ['accuracy', 'terminology', 'style', 'context']
const OUT = args.outDir
// 번역한 원문 커밋(WowVision). 파일 첫 줄 source 주석에 적는다. 2026-11-08까지 프롬프트에 397ffc3이 박혀 있어 V1.0.1 재번역에 옛 커밋이 기록될 뻔했다.
const SOURCE = args.source
if (!SOURCE) throw new Error('args.source(원문 커밋)가 필요하다')
const dirOf = rel => `${W}/${OUT}/${rel.replace(/\.md$/, '')}`

const FINDINGS = {
  type: 'object', required: ['findings'],
  properties: { findings: { type: 'array', items: { type: 'object',
    required: ['id', 'category', 'severity', 'quote', 'suggestion', 'problem', 'evidence'],
    properties: { id: { type: 'string' }, category: { type: 'string', enum: LENSES },
      severity: { type: 'string', enum: ['critical', 'major', 'minor'] }, quote: { type: 'string' },
      suggestion: { type: 'string' }, problem: { type: 'string' }, evidence: { type: 'string' } } } } },
}
const withOk = s => ({ ...s, required: [...s.required, 'ok'], properties: { ...s.properties, ok: { type: 'boolean' } } })
const DONE = { type: 'object', required: ['ok', 'remaining'], properties: { ok: { type: 'boolean' }, remaining: { type: 'array', items: { type: 'string' } } } }
const FIXED = { type: 'object', required: ['ok', 'remaining', 'escalations'],
  properties: { ...DONE.properties, escalations: { type: 'array', items: { type: 'object', required: ['ref', 'why'],
    properties: { ref: { type: 'string' }, why: { type: 'string' }, quote: { type: 'string' } } } } } }
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
const CHECK = rel => `cd ${W} && uv run python -m tools.manual check ${rel}`

// ── 1. 번역 ─────────────────────────────────────────────────────────────
const translate = rel => agent(
  `너는 설명서 번역자다. ${P}/manual-translate.md 를 Read로 읽고 그대로 따른다. 원문 커밋: ${SOURCE}\n` +
  `원문: ${EN}/${rel}\n번역문을 쓸 곳: ${KO}/${rel} (폴더가 없으면 만든다)\n` +
  `용어표: Bash로 \`cd ${W} && uv run python -m tools.manual terms ${rel}\` 를 실행해 받는다.\n` +
  `번역을 Write로 저장한 뒤 \`${CHECK(rel)}\` 를 실행한다. "앵커 없음" 외의 문제가 있으면 고치고 다시 검사한다(최대 3번). ` +
  `다른 파일을 가리키는 "앵커 없음"은 그 파일이 아직 번역되지 않았을 수 있으므로 남겨 둔다.\n` +
  `끝나면 ok(앵커 외 문제 없음 여부)와 remaining(남은 문제 줄)을 돌려준다.`,
  { label: `translate:${rel}`, phase: 'Translate', schema: DONE })

// ── 2. 앵커 ─────────────────────────────────────────────────────────────
const fixAnchors = rel => agent(
  `\`${CHECK(rel)}\` 를 실행한다. 문제가 없으면 ok=true로 끝낸다.\n` +
  `"앵커 없음"이 있으면 대상 번역 파일(${KO} 아래)의 제목을 Read로 확인해, 링크의 #앵커를 그 제목에서 만든 앵커로 고친다 ` +
  `(mdBook 규칙: 문자·숫자·_·-만 남기고 영문은 소문자, 공백은 -). 파일은 ${KO}/${rel}. 링크 글자나 다른 내용은 바꾸지 않는다. ` +
  `다른 문제가 보이면 그것도 원문(${EN}/${rel})과 맞게 고친다. 고친 뒤 다시 검사하고 ok와 remaining을 돌려준다.`,
  { label: `anchors:${rel}`, phase: 'Anchors', schema: DONE })

// ── 3. 평가 ─────────────────────────────────────────────────────────────
const claudeReview = (rel, lens) => agent(
  `너는 번역 평가자다. ${P}/manual-review.md 와 ${P}/manual-lens-${lens}.md 를 Read로 읽고 따른다.\n` +
  `입력은 Bash로 \`cd ${W} && uv run python -m tools.manual batch ${rel} ${dirOf(rel)}/claude-input-${lens}.json\` 를 실행해 만든 뒤 Read로 읽는다. ` +
  `${OUT} 폴더의 다른 평가 결과 파일은 열지 않는다. 결과를 ${dirOf(rel)}/claude-${lens}.json 에 Write로 저장하고 구조화 출력으로도 돌려준다.`,
  { label: `claude:${lens}:${rel}`, phase: 'Review', schema: FINDINGS })

const gptRun = (label, phaseName, pre, prompts, input, schemaFile, out, schema) => agent(
  pre + `다음 명령을 Bash로 한 번 실행한다(timeout 600000).\n\n` +
  `cd ${W} && uv run python -m tools.review.gpt_review ${prompts.map(f => `--prompt tools/review/prompts/${f}`).join(' ')} ` +
  `--batch ${input} --schema tools/review/${schemaFile} --out ${out}\n\n` +
  `성공하면 ${out} 을 Read로 읽어 그 내용을 한 글자도 바꾸지 않고 구조화 출력으로 돌려주고 ok=true. ` +
  `실패하면 한 번만 다시 실행하고, 그래도 실패하면 ok=false, 배열은 비운다. 판단을 직접 하지 않는다.`,
  { label, phase: phaseName, schema: withOk(schema), effort: 'low' }).then(r => (r && r.ok === true ? r : null))

const gptReview = (rel, lens) => gptRun(`gpt:${lens}:${rel}`, 'Review',
  `먼저 Bash로 \`cd ${W} && uv run python -m tools.manual batch ${rel} ${dirOf(rel)}/gpt-input-${lens}.json\` 를 실행한다. 그다음 `,
  ['manual-review.md', `manual-lens-${lens}.md`], `${dirOf(rel)}/gpt-input-${lens}.json`, 'docs-findings.schema.json',
  `${dirOf(rel)}/gpt-${lens}.json`, FINDINGS)

const norm = s => s.replace(/\s+/g, ' ').trim()
const overlaps = (a, b) => { const x = norm(a), y = norm(b); return x.length > 0 && y.length > 0 && (x.includes(y) || y.includes(x)) }

async function reviewAndFix(rel) {
  const runs = (await parallel([
    ...LENSES.map(l => () => claudeReview(rel, l).then(r => r && { provider: 'claude', lens: l, findings: r.findings })),
    ...LENSES.map(l => () => gptReview(rel, l).then(r => r && { provider: 'gpt', lens: l, findings: r.findings })),
  ])).filter(Boolean)
  const failed = 8 - runs.length
  const all = runs.flatMap(r => r.findings.map((f, i) => ({ ...f, by: `${r.provider}-${r.lens}`, provider: r.provider, ref: `${rel}#${r.provider}-${r.lens}-${i}` })))
  for (const f of all) f.consensus = all.some(g => g.provider !== f.provider && overlaps(f.quote, g.quote))
  if (!all.length) return { file: rel, failedReviewers: failed, findings: 0, applied: 0, upheld: 0, disputeWon: 0, escalations: [] }

  // 4. 번역자: 합의 지적은 반드시 반영, 나머지는 반영하거나 반박
  const resp = await agent(
    `너는 이 파일의 번역자다. ${P}/manual-translate.md 와 ${P}/rebut.md 를 Read로 읽고 따른다. 번역문은 ${KO}/${rel}, 원문은 ${EN}/${rel}.\n` +
    `아래 지적마다 판단한다. consensus=true인 것은 두 회사 평가자가 모두 지적한 것이므로 반드시 반영한다. ` +
    `나머지는 지적이 맞으면 반영하고(action=applied), 틀렸으면 고치지 않고 근거를 든다(action=dispute). ` +
    `반영은 Edit로 quote를 suggestion(또는 지적들을 반영한 더 나은 문장)으로 바꾼다. 같은 곳을 가리키는 지적이 여럿이면 함께 반영한다.\n` +
    `끝나면 \`${CHECK(rel)}\` 로 기계 검사를 통과하는지 확인하고, 깨졌으면 고친다. ` +
    `결과를 ${dirOf(rel)}/rebut.json 에 Write로 저장하고 구조화 출력으로도 돌려준다.\n\n` +
    JSON.stringify(all.map(({ ref, consensus, category, severity, quote, suggestion, problem, evidence, by }) => ({ ref, consensus, by, category, severity, quote, suggestion, problem, evidence })), null, 1),
    { label: `translator:${rel}`, phase: 'Fix', schema: RESP })
  const byRef = Object.fromEntries(((resp && resp.responses) || []).map(r => [r.ref, r]))
  const disputed = all.filter(f => byRef[f.ref] && byRef[f.ref].action === 'dispute' && !f.consensus)
  const escalations = all.filter(f => (byRef[f.ref] && byRef[f.ref].action === 'dispute' && f.consensus) || !byRef[f.ref])
    .map(f => ({ ref: f.ref, why: !byRef[f.ref] ? '번역자 응답 없음' : '합의 지적을 번역자가 반박', quote: f.quote }))
  if (!disputed.length) return { file: rel, failedReviewers: failed, findings: all.length, applied: all.length - escalations.length, upheld: 0, disputeWon: 0, escalations }

  // 5. 두 회사 판정 (서로의 결론 비공개)
  const payload = disputed.map(f => ({ ref: f.ref, file: rel, finding: { category: f.category, severity: f.severity, quote: f.quote, suggestion: f.suggestion, problem: f.problem, evidence: f.evidence }, translator: byRef[f.ref] }))
  const [gj, cj] = await parallel([
    () => gptRun(`gpt:judge:${rel}`, 'Fix',
      `먼저 아래 JSON을 ${dirOf(rel)}/judge-gpt-input.json 에 Write로 그대로 저장한다.\n\n${JSON.stringify({ file: rel, en_path: `wowvision-ko/WowVision/docs/src/user/en/${rel}`, ko_path: `wowvision-ko/WowVision/docs/src/user/ko/${rel}`, items: payload }, null, 1)}\n\n그다음 `,
      ['manual-review.md', 'judge.md'], `${dirOf(rel)}/judge-gpt-input.json`, 'verdicts.schema.json', `${dirOf(rel)}/judge-gpt.json`, VERDICTS),
    () => agent(
      `${P}/manual-review.md 와 ${P}/judge.md 를 Read로 읽고 판정자로서 따른다. 원문 ${EN}/${rel}, 번역문 ${KO}/${rel}. ` +
      `아래 항목마다 판정한다. uphold=true면 final_ko에 quote를 대신할 문장을 적는다. 결과를 ${dirOf(rel)}/judge-claude.json 에 Write로 저장하고 구조화 출력으로도 돌려준다.\n\n` +
      JSON.stringify(payload, null, 1),
      { label: `claude:judge:${rel}`, phase: 'Fix', schema: VERDICTS }),
  ])
  // 무엇을 고칠지는 tools/review/decisions.py 가 정한다(판정자마다 근거 검사, 두 판정 일치).
  const items = disputed.map(f => ({ ref: f.ref, provider: f.provider, quote: f.quote }))
  const judged = JSON.stringify({ items, gpt: gj ? gj.verdicts : null, claude: cj ? cj.verdicts : null }, null, 1)
  const fix = await agent(
    `먼저 아래 JSON을 ${dirOf(rel)}/judged.json 에 Write로 그대로 저장한다(한 글자도 바꾸지 않는다).\n\n${judged}\n\n` +
    `그다음 Bash로 \`cd ${W} && uv run python -m tools.review.decisions manual ${dirOf(rel)}/judged.json ${dirOf(rel)}/fix.json\` 를 실행하고 ${dirOf(rel)}/fix.json 을 Read로 읽는다. ` +
    `그 upheld 배열의 각 항목에 대해 ${KO}/${rel} 에서 quote를 final_ko로 Edit로 바꾼다. quote가 정확히 보이지 않으면 가장 가까운 부분을 찾아 같은 뜻으로 고친다. ` +
    `upheld가 비어 있으면 파일을 고치지 않는다. 끝나면 \`${CHECK(rel)}\` 를 통과하는지 확인하고, 깨졌으면 원문 구조에 맞게 고친다. ` +
    `ok와 remaining을 돌려주고, fix.json 의 escalations 배열(사용자 판단 목록)을 한 글자도 바꾸지 않고 escalations로 돌려준다. 판정을 직접 하지 않는다.`,
    { label: `fixer:${rel}`, phase: 'Fix', schema: FIXED })
  // 판정에서 생긴 사용자 판단 항목도 결과에 싣는다. 수정 에이전트가 실패하면 알 수 없으므로 그 사실을 남긴다(codex 2026-11-08).
  if (fix && fix.escalations) escalations.push(...fix.escalations)
  else escalations.push({ ref: rel, why: `수정 에이전트 실패: 판정 결과는 ${dirOf(rel)}/fix.json 을 직접 확인` })
  return { file: rel, failedReviewers: failed, findings: all.length, applied: Object.values(byRef).filter(r => r.action === 'applied').length,
    fixOk: !!(fix && fix.ok), decisions: `${dirOf(rel)}/fix.json`, escalations }
}

// ── 실행 ────────────────────────────────────────────────────────────────
const files = args.files
phase('Translate')
const translated = await parallel(files.map(rel => () => translate(rel).then(r => ({ rel, r }))))
log(`번역 끝: ${translated.filter(Boolean).filter(t => t.r && t.r.ok).length}/${files.length} 앵커 외 문제 없음`)
phase('Anchors')
const anchored = await parallel(files.map(rel => () => fixAnchors(rel).then(r => ({ rel, r }))))
const notClean = anchored.filter(Boolean).filter(a => !a.r || !a.r.ok).map(a => ({ file: a.rel, remaining: a.r ? a.r.remaining : ['응답 없음'] }))
if (notClean.length) log(`기계 검사 미통과 ${notClean.length}개: 평가는 진행하되 결과에 표시`)
phase('Review')
const reviewed = await pipeline(files, rel => reviewAndFix(rel))
return { notClean, reviewed }

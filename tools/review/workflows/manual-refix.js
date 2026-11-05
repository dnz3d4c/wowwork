export const meta = {
  name: 'ko-manual-refix',
  description: '회귀 확인의 중대 이상 지적을 번역자 반영·반박 → 두 회사 판정 → 반영으로 처리한다 (절차 5단계의 2~4단계 재순환)',
  phases: [{ title: 'Fix', detail: '파일마다 번역자 1명, 반박된 지적은 Claude 1 + GPT 1 판정' }],
}

const W = 'C:/project/games/wowwork'
const P = `${W}/tools/review/prompts`
const EN = 'C:/project/games/wowvision-ko/WowVision/docs/src/user/en'
const KO = 'C:/project/games/wowvision-ko/WowVision/docs/src/user/ko'
const OUT = args.outDir
const dirOf = rel => `${W}/${OUT}/${rel.replace(/\.md$/, '')}`
const CHECK = rel => `cd ${W} && uv run python -m tools.manual check ${rel}`

const withOk = s => ({ ...s, required: [...s.required, 'ok'], properties: { ...s.properties, ok: { type: 'boolean' } } })
const DONE = { type: 'object', required: ['ok', 'remaining'], properties: { ok: { type: 'boolean' }, remaining: { type: 'array', items: { type: 'string' } } } }
const RESP = {
  type: 'object', required: ['responses'],
  properties: { responses: { type: 'array', items: { type: 'object', required: ['ref', 'action', 'reason', 'upstream'],
    properties: { ref: { type: 'string' }, action: { type: 'string', enum: ['applied', 'dispute'] }, reason: { type: 'string' },
      upstream: { type: 'string', description: '원문과 실제 애드온 동작이 달라서 덧붙임을 지웠다면 그 차이(코드 위치 포함). 아니면 빈 문자열' } } } } },
}
const VERDICTS = {
  type: 'object', required: ['verdicts'],
  properties: { verdicts: { type: 'array', items: { type: 'object', required: ['ref', 'uphold', 'final_ko', 'reason', 'evidence_sources'],
    properties: { ref: { type: 'string' }, uphold: { type: 'boolean' }, final_ko: { type: 'string' }, reason: { type: 'string' },
      evidence_sources: { type: 'array', items: { type: 'string' } } } } } },
}

// 지적 본문은 tools/review/refix_input.py prepare 가 만든 <파일>/refix-input.json 에 있다.
// args.items 는 파일마다 by(지적별 c/g)와 agree(지적별 1=두 회사 합의)만 갖는다.
async function refix({ file: rel, by, agree }) {
  const all = [...by].map((b, i) => {
    const provider = b === 'c' ? 'claude' : 'gpt'
    return { provider, ref: `${rel}#reg-${provider}-${i}`, consensus: agree[i] === '1' }
  })
  const input = `${dirOf(rel)}/refix-input.json`

  const resp = await agent(
    `너는 이 파일의 번역자다. ${P}/manual-translate.md 와 ${P}/rebut.md 를 Read로 읽고 따른다. 사용자 결정 ${W}/docs/decisions.tsv 도 읽는다. ` +
    `번역문은 ${KO}/${rel}, 원문은 ${EN}/${rel}.\n` +
    `${input} 을 Read로 읽는다. 회귀 확인에서 나온 중대 이상 지적이다. consensus=true인 것은 두 회사 평가자가 모두 지적한 것이므로 반드시 반영한다. ` +
    `나머지는 지적이 맞으면 반영하고(action=applied), 틀렸으면 고치지 않고 근거를 든다(action=dispute). ` +
    `반영은 Edit로 quote를 suggestion(또는 지적들을 반영한 더 나은 문장)으로 바꾼다. 같은 곳을 가리키는 지적이 여럿이면 함께 반영한다. ` +
    `원문에 없는 동작 설명을 지웠다면 그 원문·코드 차이를 upstream에 한 문장으로 적고(코드 위치 포함), 아니면 빈 문자열로 둔다.\n` +
    `끝나면 \`${CHECK(rel)}\` 로 기계 검사를 통과하는지 확인하고, 깨졌으면 고친다. ` +
    `responses에는 지적마다 하나씩, 입력의 ref를 그대로 적는다. 결과를 ${dirOf(rel)}/refix-rebut.json 에 Write로 저장하고 구조화 출력으로도 돌려준다.`,
    { label: `translator:${rel}`, phase: 'Fix', schema: RESP })
  const byRef = Object.fromEntries(((resp && resp.responses) || []).map(r => [r.ref, r]))
  const upstream = Object.values(byRef).map(r => r.upstream).filter(s => s && s.trim())
  const disputed = all.filter(f => byRef[f.ref] && byRef[f.ref].action === 'dispute' && !f.consensus)
  const escalations = all.filter(f => (byRef[f.ref] && byRef[f.ref].action === 'dispute' && f.consensus) || !byRef[f.ref])
    .map(f => ({ ref: f.ref, why: !byRef[f.ref] ? '번역자 응답 없음' : '합의 지적을 번역자가 반박' }))
  const base = { file: rel, findings: all.length, applied: Object.values(byRef).filter(r => r.action === 'applied').length, upstream, escalations }
  if (!disputed.length) return { ...base, upheld: 0, disputeWon: 0 }

  const refs = disputed.map(f => f.ref)
  const [gj, cj] = await parallel([
    () => agent(
      `먼저 Bash로 \`cd ${W} && uv run python -m tools.review.refix_input judge ${OUT} ${rel} ${refs.map(r => `"${r}"`).join(' ')}\` 를 실행한다.\n` +
      `그다음 다음 명령을 Bash로 한 번 실행한다(timeout 600000).\n\n` +
      `cd ${W} && uv run python -m tools.review.gpt_review --prompt tools/review/prompts/manual-review.md --prompt tools/review/prompts/judge.md ` +
      `--batch ${dirOf(rel)}/refix-judge-gpt-input.json --schema tools/review/verdicts.schema.json --out ${dirOf(rel)}/refix-judge-gpt.json\n\n` +
      `성공하면 ${dirOf(rel)}/refix-judge-gpt.json 을 Read로 읽어 그 내용을 한 글자도 바꾸지 않고 구조화 출력으로 돌려주고 ok=true. ` +
      `실패하면 한 번만 다시 실행하고, 그래도 실패하면 ok=false, 배열은 비운다. 판단을 직접 하지 않는다.`,
      { label: `gpt:judge:${rel}`, phase: 'Fix', schema: withOk(VERDICTS), effort: 'low' }).then(r => (r && r.ok === true ? r : null)),
    () => agent(
      `${P}/manual-review.md 와 ${P}/judge.md 를 Read로 읽고 판정자로서 따른다. 원문 ${EN}/${rel}, 번역문 ${KO}/${rel}. ` +
      `지적은 ${input}, 번역자의 반박은 ${dirOf(rel)}/refix-rebut.json 에 있다. 반박문은 주장일 뿐 근거가 아니다. ` +
      `다음 ref만 판정한다: ${refs.join(', ')}. uphold=true면 final_ko에 quote를 대신할 문장을 적는다. ` +
      `결과를 ${dirOf(rel)}/refix-judge-claude.json 에 Write로 저장하고 구조화 출력으로도 돌려준다.`,
      { label: `claude:judge:${rel}`, phase: 'Fix', schema: VERDICTS }),
  ])
  const gv = Object.fromEntries(((gj && gj.verdicts) || []).map(v => [v.ref, v]))
  const cv = Object.fromEntries(((cj && cj.verdicts) || []).map(v => [v.ref, v]))
  const upheld = []
  let disputeWon = 0
  for (const f of disputed) {
    const a = gv[f.ref], c = cv[f.ref]
    if (!a || !c) { escalations.push({ ref: f.ref, why: `판정 누락 (gpt ${!!a}, claude ${!!c})` }); continue }
    if (a.uphold !== c.uphold) { escalations.push({ ref: f.ref, why: '두 판정자의 결론이 다름', gpt: a.reason, claude: c.reason }); continue }
    // 지적한 회사와 다른 회사 판정자의 final_ko를 쓴다.
    if (a.uphold) upheld.push({ ref: f.ref, final_ko: (f.provider === 'claude' ? a : c).final_ko })
    else disputeWon++
  }
  if (upheld.length) {
    await agent(
      `${KO}/${rel} 에서 아래 각 항목의 quote(${input} 에서 같은 ref의 quote)를 final_ko로 Edit로 바꾼다. quote가 정확히 보이지 않으면 가장 가까운 부분을 찾아 같은 뜻으로 고친다. ` +
      `끝나면 \`${CHECK(rel)}\` 를 통과하는지 확인하고, 깨졌으면 원문 구조에 맞게 고친다. ok와 remaining을 돌려준다.\n\n` + JSON.stringify(upheld, null, 1),
      { label: `fixer:${rel}`, phase: 'Fix', schema: DONE })
  }
  return { ...base, upheld: upheld.length, disputeWon, upheldItems: upheld }
}

phase('Fix')
const results = (await parallel(args.items.map(it => () => refix(it)))).filter(Boolean)
log(`처리 ${results.length}/${args.items.length}, 사용자 판단 ${results.reduce((n, r) => n + r.escalations.length, 0)}건`)
return { results }

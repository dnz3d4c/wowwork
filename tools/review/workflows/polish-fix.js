export const meta = {
  name: 'ko-manual-polish-fix',
  description: '다듬기 회귀 확인에서 남은 지적과 판정이 갈린 건을 파일별로 처리한다. 회귀 지적은 편집자 반영·반박 후 두 회사 판정, 갈린 건은 두 회사가 근거를 글자 그대로 확인할 때만 반영. Targeting 모듈 이름을 koKR 값에 맞춘다',
  phases: [
    { title: 'Edit', detail: '파일마다 편집자 1명' },
    { title: 'Judge', detail: '반박된 회귀 지적과 갈린 건: Claude 판정자 + GPT 판정자' },
    { title: 'Apply', detail: '두 판정이 일치한 것만 반영' },
  ],
}

const W = 'C:/project/games/wowwork'
const P = `${W}/tools/review/prompts`
const EN = 'C:/project/games/wowvision-ko/WowVision/docs/src/user/en'
const KO = 'C:/project/games/wowvision-ko/WowVision/docs/src/user/ko'
const OUT = args.outDir
if (!/^reviews\/[A-Za-z0-9._-]+$/.test(OUT)) throw new Error(`outDir 형식 오류: ${OUT}`)
for (const f of args.files) if (!/^[a-z0-9][a-z0-9_-]*(\/[a-z0-9_-]+)*\.md$/.test(f)) throw new Error(`파일 형식 오류: ${f}`)
const dirOf = rel => `${W}/${OUT}/${rel.replace(/\.md$/, '')}`
const CHECK = rel => `cd ${W} && uv run python -m tools.manual check ${rel}`
const TARGETING = new Set(args.targetingFiles)

const RESP = {
  type: 'object', required: ['responses', 'targeting_changes'],
  properties: {
    responses: { type: 'array', items: { type: 'object', required: ['ref', 'action', 'reason'],
      properties: { ref: { type: 'string' }, action: { type: 'string', enum: ['applied', 'dispute'] }, reason: { type: 'string' } } } },
    targeting_changes: { type: 'integer' },
  },
}
const VERDICTS = {
  type: 'object', required: ['verdicts'],
  properties: { verdicts: { type: 'array', items: { type: 'object', required: ['ref', 'uphold', 'final_ko', 'reason', 'evidence_sources'],
    properties: { ref: { type: 'string' }, uphold: { type: 'boolean' }, final_ko: { type: 'string' }, reason: { type: 'string' },
      evidence_sources: { type: 'array', items: { type: 'string' } } } } } },
}
const withOk = s => ({ ...s, required: [...s.required, 'ok'], properties: { ...s.properties, ok: { type: 'boolean' } } })
const DONE = { type: 'object', required: ['ok', 'remaining', 'not_found'], properties: { ok: { type: 'boolean' }, remaining: { type: 'array', items: { type: 'string' } }, not_found: { type: 'array', items: { type: 'string' } } } }

const TARGETING_TASK =
  `추가 작업: 이 파일에서 WowVision의 Targeting 모듈을 이름으로 가리키는 "대상 지정"(WowVision 메뉴 항목, 메뉴 경로의 모듈 이름, ` +
  `world/targeting.md 페이지 제목과 그 페이지로 가는 링크 글자)을 koKR 값 "목표 선택"(vision-locale/koKR/targeting.lua L["Targeting"], 게임 공식 TARGETING_HEADER도 같음)으로 바꾼다. ` +
  `설명서는 koKR 화면 문구를 따른다는 기존 원칙(wowwork/docs/manual-plan.md ### 용어 1번)이다. 원문 영어가 대문자 Targeting으로 모듈·메뉴·페이지를 가리키는 곳만 바꾸고, ` +
  `"소프트 대상 지정"처럼 다른 기능 이름의 일부이거나 대상을 고르는 동작을 뜻하는 곳은 그대로 둔다. 다른 파일은 다른 편집자가 동시에 고치고 있으므로 이 파일만 고친다(다른 파일의 앵커가 깨지면 나중에 따로 고친다). 바꾼 곳 수를 targeting_changes에 적는다.\n`

const gptRun = (label, pre, input, out) => agent(
  pre + `다음 명령을 Bash로 한 번 실행한다(timeout 600000).\n\n` +
  `cd ${W} && uv run python -m tools.review.gpt_review --prompt tools/review/prompts/polish-base.md --prompt tools/review/prompts/judge.md ` +
  `--batch ${input} --schema tools/review/verdicts.schema.json --out ${out}\n\n` +
  `성공하면 ${out} 을 Read로 읽어 그 내용을 한 글자도 바꾸지 않고 구조화 출력으로 돌려주고 ok=true. ` +
  `실패하면 한 번만 다시 실행하고, 그래도 실패하면 ok=false, 배열은 비운다. 판단을 직접 하지 않는다.`,
  { label, phase: 'Judge', schema: withOk(VERDICTS), effort: 'low' }).then(r => (r && r.ok === true ? r : null))

const STRICT =
  `이 항목들은 앞선 두 회사 판정이 갈린 지적이다. 사용자 결정(wowwork/docs/decisions.tsv 2026-11-06 "판정이 갈린 건도 같은 기준")에 따라, ` +
  `지적의 근거가 글자 그대로 확인될 때만 uphold=true로 한다. 인정하는 근거: koKR 값(wowvision-ko/vision-locale/koKR), 설치 프로그램 Loc.cs, ` +
  `wowwork/docs/glossary.tsv, 게임 공식 문자열(같은 문맥, wowwork/cache/gs_*.csv), 앱 코드, 다른 한국어 설명서의 표기. 직접 열어 그 글자를 확인한 경우만이다. ` +
  `자연스러움이나 취향만이 근거면 uphold=false다.\n`

const ITEMS = {
  type: 'object', required: ['items'],
  properties: { items: { type: 'array', items: { type: 'object', required: ['ref', 'kind', 'quote', 'suggestion'],
    properties: { ref: { type: 'string' }, kind: { type: 'string' }, by: { type: 'string' }, category: { type: 'string' }, severity: { type: 'string' },
      quote: { type: 'string' }, suggestion: { type: 'string' }, problem: { type: 'string' }, evidence: { type: 'string' }, why: { type: 'string' },
      gpt_reason: { type: 'string' }, claude_reason: { type: 'string' } } } } },
}
const loadItems = rel => agent(
  `Bash로 다음을 실행하고 출력된 JSON 배열을 한 글자도 바꾸지 않고 items로 돌려준다. 판단하지 않는다.\n\n` +
  `cd ${W} && uv run python -X utf8 -c "import json; print(json.dumps(json.load(open('${args.leftover}', encoding='utf-8')).get('${rel}', []), ensure_ascii=False))"`,
  { label: `load:${rel}`, phase: 'Edit', schema: ITEMS, effort: 'low' })

async function fixFile(rel) {
  const loaded = await loadItems(rel)
  if (!loaded) return { file: rel, error: '지적 목록을 읽지 못함', escalations: [{ ref: rel, why: '지적 목록을 읽지 못함' }], applied: 0, upheld: 0, kept: 0 }
  const items = loaded.items
  const reg = items.filter(i => i.kind === 'regression')
  const split = items.filter(i => i.kind !== 'regression')
  let resp = null
  if (reg.length || TARGETING.has(rel)) {
    resp = await agent(
      `너는 이 설명서 파일의 편집자다. ${P}/polish-base.md 를 Read로 읽고 "바꾸지 않는 것"을 지킨다. 번역문은 ${KO}/${rel}, 원문은 ${EN}/${rel}.\n` +
      (reg.length ? `아래는 회귀 확인 평가자의 중대 이상 지적이다. 지적이 맞으면 Edit로 반영하고(action=applied), 틀렸거나 원문과 사용자 결정(wowwork/docs/decisions.tsv)에 어긋나면 고치지 않고 근거를 든다(action=dispute). ` +
        `반박 근거는 원문, 앱 코드, koKR, 게임 공식 문자열, wowwork/docs의 translation-guide.md·decisions.tsv·glossary.tsv만 인정된다. 화면 문구 인용은 koKR 값과 글자가 같아야 한다.\n\n` +
        JSON.stringify(reg, null, 1) + '\n\n' : '') +
      (TARGETING.has(rel) ? TARGETING_TASK : '') +
      `끝나면 \`${CHECK(rel)}\` 로 기계 검사를 통과하는지 확인하고 깨졌으면 고친다. 결과를 ${dirOf(rel)}/editor.json 에 Write로 저장하고 구조화 출력으로도 돌려준다(지적이 없으면 responses는 빈 배열).`,
      { label: `editor:${rel}`, phase: 'Edit', schema: RESP })
  }
  const byRef = Object.fromEntries(((resp && resp.responses) || []).map(r => [r.ref, r]))
  const escalations = reg.filter(f => !byRef[f.ref]).map(f => ({ ref: f.ref, why: '편집자 응답 없음', quote: f.quote }))
  const disputed = reg.filter(f => byRef[f.ref] && byRef[f.ref].action === 'dispute')
  const toJudge = [
    ...disputed.map(f => ({ ref: f.ref, strict: false, finding: f, editor: byRef[f.ref] })),
    ...split.map(f => ({ ref: f.ref, strict: true, finding: f })),
  ]
  const base = { file: rel, regression: reg.length, applied: Object.values(byRef).filter(r => r.action === 'applied').length, targetingChanges: resp ? resp.targeting_changes : 0 }
  if (!toJudge.length) return { ...base, upheld: 0, kept: 0, escalations }

  const instr = `strict=true인 항목: ${STRICT}strict=false인 항목은 회귀 지적과 편집자 반박 가운데 근거가 강한 쪽을 고른다.\n`
  const [gj, cj] = await parallel([
    () => gptRun(`gpt:judge:${rel}`,
      `먼저 아래 JSON을 ${dirOf(rel)}/judge-gpt-input.json 에 Write로 그대로 저장한다.\n\n${JSON.stringify({ file: rel, instruction: instr, en_path: `wowvision-ko/WowVision/docs/src/user/en/${rel}`, ko_path: `wowvision-ko/WowVision/docs/src/user/ko/${rel}`, items: toJudge }, null, 1)}\n\n그다음 `,
      `${dirOf(rel)}/judge-gpt-input.json`, `${dirOf(rel)}/judge-gpt.json`),
    () => agent(
      `${P}/polish-base.md 와 ${P}/judge.md 를 Read로 읽고 판정자로서 따른다. 원문 ${EN}/${rel}, 번역문 ${KO}/${rel}.\n${instr}` +
      `아래 항목마다 판정한다. uphold=true면 final_ko에 quote를 대신할 문장을 적는다. 결과를 ${dirOf(rel)}/judge-claude.json 에 Write로 저장하고 구조화 출력으로도 돌려준다.\n\n` +
      JSON.stringify(toJudge, null, 1),
      { label: `claude:judge:${rel}`, phase: 'Judge', schema: VERDICTS }),
  ])
  const gv = Object.fromEntries(((gj && gj.verdicts) || []).map(v => [v.ref, v]))
  const cv = Object.fromEntries(((cj && cj.verdicts) || []).map(v => [v.ref, v]))
  const upheld = []
  let kept = 0
  for (const t of toJudge) {
    const a = gv[t.ref], c = cv[t.ref]
    if (!a || !c) { escalations.push({ ref: t.ref, why: `판정 누락 (gpt ${!!a}, claude ${!!c})`, quote: t.finding.quote }); continue }
    if (a.uphold !== c.uphold) { escalations.push({ ref: t.ref, why: '두 판정자의 결론이 다름', quote: t.finding.quote, suggestion: t.finding.suggestion, gpt: a.reason, claude: c.reason }); continue }
    if (a.uphold) upheld.push({ ref: t.ref, quote: t.finding.quote, final_ko: (t.finding.by === 'claude' ? a : c).final_ko })
    else kept++
  }
  let notFound = []
  if (upheld.length) {
    const fx = await agent(
      `${KO}/${rel} 에서 아래 각 항목의 quote를 final_ko로 Edit로 바꾼다. quote가 파일에 글자 그대로 한 번만 있을 때만 고친다. ` +
      `없거나 여러 번 있으면 고치지 않고 그 ref를 not_found에 넣는다(비슷한 곳을 대신 고치지 않는다). ` +
      `끝나면 \`${CHECK(rel)}\` 를 통과하는지 확인하고, 깨졌으면 원문 구조에 맞게 고친다. ok, remaining, not_found를 돌려준다.\n\n` + JSON.stringify(upheld, null, 1),
      { label: `fixer:${rel}`, phase: 'Apply', schema: DONE })
    notFound = fx ? fx.not_found : upheld.map(u => u.ref)
    for (const ref of notFound) escalations.push({ ref, why: '판정 반영 실패: quote가 정확히 일치하지 않음' })
  }
  return { ...base, upheld: upheld.length - notFound.length, kept, escalations, upheldItems: upheld.filter(u => !notFound.includes(u.ref)) }
}

phase('Edit')
const results = (await pipeline(args.files, rel => fixFile(rel))).filter(Boolean)
const esc = results.flatMap(r => r.escalations)
log(`파일 ${results.length}/${args.files.length}, 편집자 반영 ${results.reduce((n, r) => n + r.applied, 0)}, 판정 반영 ${results.reduce((n, r) => n + r.upheld, 0)}, 유지 ${results.reduce((n, r) => n + r.kept, 0)}, 사용자 판단 ${esc.length}, 목표 선택 ${results.reduce((n, r) => n + (r.targetingChanges || 0), 0)}곳`)
return { results, escalations: esc }

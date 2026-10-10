let DATA=[];
fetch('data-lite.json').then(r=>r.json()).then(d=>DATA=d);
const ROUTES=[
 [/duty|burnout|job|overtime|exam|fail|action/i,'gita','duty/action → Gita'],
 [/betray|sibling|parent|exile|team|leader|endurance|family/i,'ramayana','endurance/relationships → Ramayana'],
 [/anger|craving|scroll|rumina|insult|mind|crave/i,'dhammapada','reactivity/craving → Dhammapada'],
 [/grief|loss|trust|forgiv|caregiv/i,'bible','grief/trust → Bible'],
 [/patience|anxiet|medical|justice|unfair|trial|sabr/i,'quran','patience/justice → Qur\u2019an']];
const LENS={gita:'Nishkama Karma: act to standard, detach from fruits. Svadharma: name this season (stability vs growth). Agency: market is circumstance; effort and exit plan are yours.',
ramayana:'Dharma under friction: if you say yes, what conduct does yes require? Steadfastness over mood. Sacrificial leadership: half-presence taxes the team.',
dhammapada:'Mind precedes states. Name the trigger, pause the craving loop (Anicca: this urge passes). Replace scrolling/rumination with one deliberate act.',
bible:'Stewardship: work is trust. Forbearance in lean seasons. Humility: neither market fear nor excitement-feeling alone decides — counsel, then commit wholeheartedly.',
quran:'Sabr + Tawakkul: tie your camel — effort plus trust. Adl: name unfairness plainly, respond justly, leave outcome to God.'};
function pickTrad(q,lock){
 if(lock) return [lock,'locked by selector'];
 for(const [re,t,why] of ROUTES) if(re.test(q)) return [t,why];
 return ['gita','default (duty/action)'];
}
function score(e,words){let s=0;const hay=((e.keywords||[]).join(' ')+' '+(e.translation||'')).toLowerCase();for(const w of words) if(hay.includes(w)) s++;return s;}
function advise(){
 const q=document.getElementById('q').value.trim(),lock=document.getElementById('trad').value;
 const out=document.getElementById('out');if(!q){out.innerHTML='<p>Describe your dilemma first.</p>';return;}
 const [trad,why]=pickTrad(q,lock);
 const words=q.toLowerCase().split(/[^a-z]+/).filter(w=>w.length>3);
 const pool=DATA.filter(e=>e.tradition===trad);
 pool.sort((a,b)=>score(b,words)-score(a,words));
 const v=pool[0];
 const tension=/grief|loss/i.test(q)?'grief and the pull to withdraw':/anger|crav|scroll/i.test(q)?'reactivity vs intention':/job|offer|market|burnout/i.test(q)?'security vs engagement':'agency vs circumstance';
 out.innerHTML=`<div class="card"><h3>1. Contextual Mirror <small>(${trad}, ${why})</small></h3><p>You describe: ${q.replace(/</g,'&lt;')}. Root tension: ${tension}.</p></div>
 <div class="card"><h3>2. Canonical Anchor</h3><div class="anchor"><b>[${v.canonical_reference}]</b>\n${v.source_text||''}\n${v.transliteration||''}\n${v.translation||''}\n— ${v.translator||''}</div><p><small>Lite set (60 records). Full texts: repo data/unified/.</small></p></div>
 <div class="card"><h3>3. Philosophical Deconstruction</h3><p>${LENS[trad]}</p></div>
 <div class="card"><h3>4. Practical Reflection</h3><p>1) Write a 6-month contract with yourself: why stay/go, 3 exit signals, weekly review.<br>2) Fix one non-negotiable standard independent of mood.<br>3) Ask one negotiable (scope, mentor, review date) before signing.</p><p><small>Also relevant: ${trad==='gita'?'Ramayana':trad==='ramayana'?'Gita':trad==='dhammapada'?'Bible':trad==='bible'?'Qur’an':'Bible'} — switch the selector to compare. Crisis (self-harm/abuse): stop here, contact local emergency services.</small></p></div>`;
}

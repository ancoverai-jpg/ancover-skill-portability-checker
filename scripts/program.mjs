import {mkdir,open,readFile,writeFile,rename,unlink} from 'node:fs/promises';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
export const stages=['discovered','researched','prioritized','specified','developing','validating','ready','published','maintenance'];
export const dailyPublicationTarget=5;
export function dailyProgress(state,now=new Date()){
 const localDay=date=>new Intl.DateTimeFormat('en-CA',{timeZone:'America/Sao_Paulo',year:'numeric',month:'2-digit',day:'2-digit'}).format(date);
 const day=localDay(now),published=state.publications.filter(p=>localDay(new Date(p.at))===day).length;
 return {day,timeZone:'America/Sao_Paulo',target:dailyPublicationTarget,published,remaining:Math.max(0,dailyPublicationTarget-published),targetMet:published>=dailyPublicationTarget};
}
export async function transact(dir,fn){
 await mkdir(dir,{recursive:true});const lock=resolve(dir,'cycle.lock');let fd;
 try{fd=await open(lock,'wx');}catch{throw Error('LOCKED: inspect lock owner; never remove a live lock');}
 try{await fd.writeFile(JSON.stringify({pid:process.pid,started:new Date().toISOString()}));let state;
  try{state=JSON.parse(await readFile(resolve(dir,'state.json'),'utf8'));}catch(e){if(e.code!=='ENOENT')throw e;state={version:1,items:[],history:[],publications:[]};}
  const result=await fn(state);const tmp=resolve(dir,'state.json.tmp');await writeFile(tmp,JSON.stringify(state,null,2));await rename(tmp,resolve(dir,'state.json'));return result;
 }finally{await fd.close();await unlink(lock);}
}
export function advance(state,id,next,evidence,now=new Date()){
 const item=state.items.find(x=>x.id===id);if(!item)throw Error('UNKNOWN_ID');
 if(stages.indexOf(next)!==stages.indexOf(item.stage)+1)throw Error('INVALID_TRANSITION');
 if(!evidence||typeof evidence!=='object'||Array.isArray(evidence)||!evidence.artifact)throw Error('EVIDENCE_REQUIRED');
 if(next==='researched'&&(!(evidence.independentReports>=3)||new Set(evidence.communities||[]).size<2))throw Error('INSUFFICIENT_DEMAND');
 if(next==='ready'&&(evidence.blockers!==0||evidence.validation!=='passed'||!evidence.treeSha256))throw Error('QUALITY_GATE');
 if(next==='published'){
  if(!/^https:\/\/github\.com\/[\w.-]+\/[\w.-]+$/.test(evidence.url||'')||!evidence.remoteCommitVerified||!evidence.commit)throw Error('REMOTE_VERIFICATION_REQUIRED');
  const unit=evidence.unit||'project';if(!['skill','project'].includes(unit))throw Error('INVALID_PUBLICATION_UNIT');
  if(unit==='skill'&&!/^skills\/[a-z0-9-]+\/SKILL\.md$/.test(evidence.path||''))throw Error('SKILL_PATH_REQUIRED');
  if(state.publications.some(p=>p.id===id||(unit==='project'&&(p.unit||'project')==='project'&&p.url===evidence.url)||(unit==='skill'&&p.unit==='skill'&&p.url===evidence.url&&p.path===evidence.path)))throw Error('DUPLICATE_PUBLICATION');
  state.publications.push({id,unit,...(unit==='skill'?{path:evidence.path}:{}),url:evidence.url,commit:evidence.commit,at:now.toISOString()});
 }
 const at=now.toISOString();state.history.push({id,from:item.stage,to:next,evidence,at});item.stage=next;item.updated=at;
}
export async function main(args){
 const [cmd,...rest]=args,dir=resolve(process.env.ANCOVER_STATE_DIR||'.runtime');
 if(!['status'].includes(cmd)){try{const lease=JSON.parse(await readFile(resolve(dir,'cycle.lease'),'utf8'));if(lease.id!==process.env.ANCOVER_CYCLE_ID)throw Error('CYCLE_OWNED_BY_ANOTHER_RUN');}catch(e){if(e.code!=='ENOENT')throw e;}}
 return transact(dir,state=>{
  if(cmd==='add'){const [id,title]=rest;if(!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(id||'')||!title)throw Error('USAGE: add ID TITLE');if(state.items.some(x=>x.id===id||x.title.toLowerCase()===title.toLowerCase()))throw Error('DUPLICATE_IDEA');state.items.push({id,title,stage:'discovered'});return {added:id};}
  if(cmd==='advance'){const [id,next,json]=rest;advance(state,id,next,JSON.parse(json));return {id,stage:next};}
  if(cmd==='cycle'){
   const pending=state.items.filter(x=>['maintenance','published','validating','developing'].includes(x.stage));
   return {mode:'OPERATOR_HANDOFF',progress:dailyProgress(state),limits:{maxMinutes:45,maxAttempts:2,paidApiCalls:0},queue:pending.length?pending:state.items,notice:'Daily target is five distinct qualified projects or Skills actually published to GitHub. No weekly cap. No drafts, private plugin saves, version-only updates or duplicate publications count toward it. Quality gates remain mandatory.'};
  }if(cmd==='status')return state;throw Error('USAGE: program.mjs add|advance|cycle|status');
 });
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){try{console.log(JSON.stringify(await main(process.argv.slice(2)),null,2));}catch(e){console.error(JSON.stringify({error:e.message.startsWith('LOCKED')?e.message:'PROGRAM_FAILED',detail:'Inspect command, state and evidence locally; no raw input is logged.'}));process.exitCode=1;}}

import {open,lstat} from 'node:fs/promises';
import {resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
const LIMIT=1024*1024, outcomes=new Set(['success','failure','neutral','cancelled','timed_out','action_required','skipped','stale','startup_failure']);
const fields=(x,keys)=>!!x&&typeof x==='object'&&!Array.isArray(x)&&Object.keys(x).length===keys.length&&keys.every(k=>Object.hasOwn(x,k));
const validName=x=>typeof x==='string'&&/^[A-Za-z0-9][A-Za-z0-9 ._()/:-]{0,99}$/.test(x);
const app=x=>Number.isSafeInteger(x)&&x>0;
const sha=x=>typeof x==='string'&&/^[0-9a-f]{40}$/.test(x);
const key=x=>JSON.stringify([x.name,x.appId]);
function invalid(){throw Error('INVALID_INPUT');}
export function evaluate(input){
 if(!fields(input,['schemaVersion','expectedSha','observedSha','complete','expected','checks'])||input.schemaVersion!==1||!sha(input.expectedSha)||!sha(input.observedSha)||typeof input.complete!=='boolean'||!Array.isArray(input.expected)||input.expected.length<1||input.expected.length>100||!Array.isArray(input.checks)||input.checks.length>100)invalid();
 const expectedKeys=new Set();
 for(const c of input.expected){
  if(!fields(c,['name','appId','allowSkipped'])||!validName(c.name)||!app(c.appId)||typeof c.allowSkipped!=='boolean'||expectedKeys.has(key(c)))invalid();
  expectedKeys.add(key(c));
 }
 const indexed=new Map();
 for(const c of input.checks){
  if(!fields(c,['name','appId','status','conclusion'])||!validName(c.name)||!app(c.appId)||!['queued','in_progress','completed'].includes(c.status)||(c.status==='completed'?!outcomes.has(c.conclusion):c.conclusion!==null))invalid();
  if(!indexed.has(key(c)))indexed.set(key(c),[]);
  indexed.get(key(c)).push(c);
 }
 const records=input.expected.map(c=>{
  const found=indexed.get(key(c))||[];let result;
  if(found.length===0)result='MISSING';
  else if(found.length!==1)result='AMBIGUOUS';
  else if(found[0].status!=='completed')result='PENDING';
  else if(found[0].conclusion==='success')result='RECORDED_SUCCESS';
  else if(found[0].conclusion==='skipped')result=c.allowSkipped?'POLICY_ALLOWED_SKIP':'UNEXPECTED_SKIP';
  else result='NON_SUCCESS';
  return {name:c.name,appId:c.appId,result};
 });
 const gaps=records.filter(r=>!['RECORDED_SUCCESS','POLICY_ALLOWED_SKIP'].includes(r.result)).length;
 const problems=[];if(input.expectedSha!==input.observedSha)problems.push('REVISION_MISMATCH');if(!input.complete)problems.push('INCOMPLETE_SNAPSHOT');
 const policySatisfied=problems.length===0&&gaps===0;
 return {schemaVersion:1,evidence:'OPERATOR_SUPPLIED_SNAPSHOT',policySatisfied,problems,counts:{expected:records.length,recordedSuccess:records.filter(r=>r.result==='RECORDED_SUCCESS').length,allowedSkip:records.filter(r=>r.result==='POLICY_ALLOWED_SKIP').length,gaps,ignored:input.checks.filter(c=>!expectedKeys.has(key(c))).length},records,limitations:['No network, authentication, branch-protection discovery or test execution','Snapshot completeness, revision and policy are supplied by the operator','Policy satisfaction is not merge approval or proof of test coverage']};
}
async function readInput(path){
 if(!(await lstat(path)).isFile())invalid();
 const file=await open(path,'r');try{
  if(!(await file.stat()).isFile())invalid();
  const buffer=Buffer.alloc(LIMIT+1);let size=0;
  while(size<buffer.length){const {bytesRead}=await file.read(buffer,size,buffer.length-size,null);if(!bytesRead)break;size+=bytesRead;}
  if(size>LIMIT)invalid();
  return JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(buffer.subarray(0,size)));
 }finally{await file.close();}
}
export async function main(args){
 if(args.length===1&&args[0]==='--help')return {exitCode:0,text:'Usage: node check.mjs SNAPSHOT.json\nOffline policy review only; never executes or fetches checks.'};
 try{
  if(args.length!==1||typeof args[0]!=='string'||args[0].startsWith('-'))invalid();
  const report=evaluate(await readInput(args[0]));return {exitCode:report.policySatisfied?0:1,report};
 }catch{return {exitCode:2,error:'INVALID_INPUT'};}
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){
 const result=await main(process.argv.slice(2));if(result.error)process.stderr.write(JSON.stringify({error:result.error})+'\n');else process.stdout.write((result.text||JSON.stringify(result.report,null,2))+'\n');process.exitCode=result.exitCode;
}

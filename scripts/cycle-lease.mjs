import {mkdir,open,readFile,unlink} from 'node:fs/promises';import {resolve} from 'node:path';
const [action,id]=process.argv.slice(2),dir=resolve(process.env.ANCOVER_STATE_DIR||'.runtime'),path=resolve(dir,'cycle.lease');
try{
 if(!/^[a-zA-Z0-9-]{4,80}$/.test(id||''))throw Error('INVALID_RUN_ID');await mkdir(dir,{recursive:true});
 if(action==='acquire'){const f=await open(path,'wx');try{await f.writeFile(JSON.stringify({id,started:new Date().toISOString(),maxMinutes:45}));}finally{await f.close();}console.log(JSON.stringify({acquired:true,id}));}
 else if(action==='release'){const owner=JSON.parse(await readFile(path,'utf8'));if(owner.id!==id)throw Error('LEASE_OWNER_MISMATCH');await unlink(path);console.log(JSON.stringify({released:true,id}));}
 else throw Error('INVALID_ACTION');
}catch(e){console.error(JSON.stringify({error:e.code==='EEXIST'?'CYCLE_ALREADY_ACTIVE':e.message==='LEASE_OWNER_MISMATCH'?e.message:'LEASE_FAILED'}));process.exitCode=1;}

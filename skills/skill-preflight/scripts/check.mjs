import {readdir,readFile,lstat,realpath} from 'node:fs/promises';
import {resolve,relative,dirname,basename,isAbsolute,sep} from 'node:path';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';
let yaml;
try{yaml=await import('yaml');}catch{console.error(JSON.stringify({error:'DEPENDENCY_MISSING',evidence:'ENVIRONMENT_ERROR'}));process.exit(2);}
const {parseDocument,visit,isCollection}=yaml;

export async function inspect(input){
 const root=await realpath(resolve(input));if(!(await lstat(root)).isDirectory())throw Error('TARGET_NOT_DIRECTORY');
 const findings=[], files=[], bytes={n:0};const add=(rule,file)=>findings.push({rule,file});
 let directoryCount=0;
 async function walk(dir){if(++directoryCount>3000||relative(root,dir).split(sep).length>40)throw Error('TARGET_LIMIT_EXCEEDED');for(const e of (await readdir(dir,{withFileTypes:true})).sort((a,b)=>a.name.localeCompare(b.name,'en'))){
  if(['.git','node_modules','.runtime'].includes(e.name))continue;
  const p=resolve(dir,e.name), rel=relative(root,p).split(sep).join('/'),st=await lstat(p);
  if(st.isSymbolicLink()){add('SYMLINK',rel);continue;}
  if(st.isDirectory()){await walk(p);continue;}
  if(!st.isFile()){add('SPECIAL_FILE',rel);continue;}
  if(files.length>=3000||st.size>2*1024*1024||(bytes.n+=st.size)>20*1024*1024)throw Error('TARGET_LIMIT_EXCEEDED');
  if(/^\.env(?:\.|$)/i.test(e.name)||/\.(?:pem|key|p12|sqlite|db|log)$/i.test(e.name))add('PRIVATE_FILE_NAME',rel);
  const buffer=await readFile(p);files.push({path:rel,sha256:createHash('sha256').update(buffer).digest('hex'),text:/\.(?:md|json)$/i.test(e.name)?buffer.toString('utf8'):null});
 }}await walk(root);
 const paths=new Set(files.map(x=>x.path));
 const manifests=['plugin.json','.codex-plugin/plugin.json','.claude-plugin/plugin.json'];let identity;
 for(const name of manifests){const f=files.find(x=>x.path===name);if(!f)continue;try{const m=JSON.parse(f.text);if(!m||typeof m!=='object'||Array.isArray(m))throw Error();
  if(typeof m.name!=='string'||!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(m.name)||m.name.length>64)add('MANIFEST_NAME',name);
  if(typeof m.version!=='string'||!/^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$/.test(m.version))add('MANIFEST_VERSION',name);
  if(typeof m.description!=='string'||!m.description.trim())add('MANIFEST_DESCRIPTION',name);
  if(name==='plugin.json'&&m.$schema!=='https://agent-plugins.org/schemas/1.0.0/plugin.schema.json')add('PORTABLE_SCHEMA',name);
  if(identity&&(identity.name!==m.name||identity.version!==m.version))add('MANIFEST_IDENTITY_DRIFT',name);identity=m;
 }catch{add('MANIFEST_JSON',name);}}
 let skillCount=0;
 for(const f of files){if(basename(f.path)==='SKILL.md'){
  skillCount++;const match=f.text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  if(!match){add('FRONTMATTER_MISSING',f.path);continue;}
  const doc=parseDocument(match[1],{uniqueKeys:true});if(doc.errors.length){add('FRONTMATTER_YAML',f.path);continue;}
  const m=doc.toJS();if(!m||typeof m!=='object'||Array.isArray(m)){add('FRONTMATTER_MAPPING',f.path);continue;}
  const allowed=new Set(['name','description','license','allowed-tools','metadata','compatibility']);
  if(Object.keys(m).some(k=>!allowed.has(k)))add('FRONTMATTER_NONPORTABLE_FIELD',f.path);
  let flow=false;visit(doc,(_,node)=>{if(isCollection(node)&&node.flow)flow=true;});if(flow)add('FRONTMATTER_FLOW_COLLECTION',f.path);
  const expectedName=f.path==='SKILL.md'?basename(root):basename(dirname(f.path));
  if(typeof m.name!=='string'||m.name.length>64||!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(m.name)||m.name!==expectedName)add('SKILL_NAME',f.path);
  if(typeof m.description!=='string'||!m.description.trim()||m.description.length>1024)add('SKILL_DESCRIPTION',f.path);
  if(m.compatibility!==undefined&&(typeof m.compatibility!=='string'||m.compatibility.length>500))add('SKILL_COMPATIBILITY',f.path);
  if(!f.text.slice(match[0].length).trim())add('SKILL_BODY_EMPTY',f.path);
 }
 if(f.path.endsWith('.md'))for(const match of f.text.matchAll(/!?\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)/g)){
  let link=match[1].replace(/^<|>$/g,'');if(/^(?:[a-z][a-z0-9+.-]*:|#|\/\/)/i.test(link))continue;
  try{link=decodeURIComponent(link.split('#')[0].split('?')[0]);}catch{add('LINK_ENCODING',f.path);continue;}
  if(!link)continue;const target=resolve(root,dirname(f.path),link), rel=relative(root,target);
  if(isAbsolute(rel)||rel==='..'||rel.startsWith('..'+sep)){add('LINK_OUTSIDE_PACKAGE',f.path);continue;}
  if(!paths.has(rel.split(sep).join('/')))add('LINK_MISSING',f.path);
 }}
 if(!skillCount)add('NO_SKILLS','.');
 const treeSha256=createHash('sha256').update(files.map(f=>f.path+'\0'+f.sha256+'\n').join('')).digest('hex');
 return {schemaVersion:1,evidence:'STATIC_INSPECTION',profile:'ancover-portable-v0.1',treeSha256,fileCount:files.length,skillCount,findings,passed:findings.length===0,runtime:{codex:'NOT_TESTED',claudeCode:'NOT_TESTED'},limitations:['No execution, signature, secret-content scan, prompt-injection detection or full host schema validation','Markdown inline local files only; no anchors, HTML, code path or remote URL validation']};
}
if(process.argv[1]&&import.meta.url===pathToFileURL(resolve(process.argv[1])).href){
 try{if(process.argv.length!==3)throw Error('USAGE: node check.mjs TARGET_DIRECTORY');const r=await inspect(process.argv[2]);console.log(JSON.stringify(r,null,2));process.exitCode=r.passed?0:1;}catch(e){console.error(JSON.stringify({error:/^(USAGE:|TARGET_)/.test(e.message)?e.message:'INSPECTION_FAILED',evidence:'ENVIRONMENT_ERROR'}));process.exitCode=2;}
}

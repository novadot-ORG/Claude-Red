import pathlib,json,hashlib,os,shutil,tempfile,datetime
stage=pathlib.Path('/home/customer/www/novadot.co.uk/.security-release-2026-11-06')
plan=json.loads((stage/'plan.json').read_text());root=pathlib.Path(plan['root']);candidate=stage/'candidate';backup=stage/'before'
assert plan['status']=='staged_not_deployed'
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
def atomic_copy(source,target,mode):
 target.parent.mkdir(parents=True,exist_ok=True)
 fd,tmp=tempfile.mkstemp(prefix='.novadot-release-',dir=target.parent)
 try:
  with os.fdopen(fd,'wb') as f:
   f.write(source.read_bytes());f.flush();os.fsync(f.fileno())
  os.chmod(tmp,mode);os.replace(tmp,target)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
# Recheck every destination and staged byte immediately before first live mutation.
for rel,expected in plan['files'].items():
 target=root/rel
 assert target.resolve().is_relative_to(root.resolve()),rel
 assert not any(p.is_symlink() for p in [target,*target.parents] if p.is_relative_to(root)),rel
 old=plan['baseline'][rel]
 assert digest(target)==(old['sha256'] if old else None),'Live drift: '+rel
 assert digest(candidate/rel)==expected,'Staged drift: '+rel
 if rel in plan['changed'] and old:assert digest(backup/rel)==old['sha256'],'Backup drift: '+rel
order=sorted(plan['changed'],key=lambda p:(2 if p=='.htaccess' else 1 if p.endswith('.html') else 0,p))
installed=[]
try:
 # Immutable new assets first, HTML next, restrictive CSP last. Keep old assets.
 for rel in order:
  old=plan['baseline'][rel];mode=int(old['mode'],8) if old else 0o644
  atomic_copy(candidate/rel,root/rel,mode);installed.append(rel)
 for rel,expected in plan['files'].items():assert digest(root/rel)==expected,'Post-install mismatch: '+rel
 receipt={'status':'deployed_server_hashes_verified','deployed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'root':str(root),'backup':str(backup),'release_id':plan['release_id'],'archive_sha256':plan['archive_sha256'],'installed':installed,'verified_files':len(plan['files']),'databases_changed':False,'real_emails_sent':0}
except BaseException:
 # Restore old permissive policy first, then corresponding old HTML. New assets
 # may remain harmlessly available for a browser that loaded during cutover.
 for rel in sorted(installed,key=lambda p:(p!='.htaccess',p)):
  old=plan['baseline'][rel]
  if old:atomic_copy(backup/rel,root/rel,int(old['mode'],8))
 raise
(stage/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');os.chmod(stage/'receipt.json',0o600)
plan['status']='deployed';(stage/'plan.json').write_text(json.dumps(plan,indent=2)+'\n')
print(json.dumps(receipt))

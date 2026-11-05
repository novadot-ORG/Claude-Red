"""Source-only inventory, hashes and syntax checks; does not load WordPress.
Usage: python3 check-source.py SOURCE_ROOT OUTPUT_DIRECTORY
Excludes private configuration, database dumps, logs, and archived copies from lint.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, subprocess, sys
root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=True)
content = root/'public_html/wp-content'
files = set((content/'mu-plugins').glob('*.php'))
files.update((content/'mu-plugins').glob('*/assets/*.js'))
files.update(p for p in (content/'plugins/healthyaa-ai-assistant').rglob('*') if p.suffix in ('.php','.js') and p.is_file())
files.add(content/'themes/oceanwp/functions.php')
# Templates receive syntax coverage; do not imply full manual security review.
files.update((content/'themes/oceanwp/woocommerce').rglob('*.php'))
for rel in ['wc-thanks-redirect/src/Api.php','wc-thanks-redirect/src/Modules/SandBoxPayment.php','wc-thanks-redirect/src/Compatibility/SandBoxPaymentBlocksSupport.php','wc-thanks-redirect/wc-thanks-redirect.php','woocommerce/includes/class-wc-checkout.php','woocommerce/includes/class-wc-order.php','woocommerce/includes/class-wc-form-handler.php','woocommerce/src/StoreApi/Routes/V1/Checkout.php','woocommerce/src/StoreApi/Routes/V1/CheckoutOrder.php','woocommerce/src/StoreApi/Payments/PaymentContext.php']:
 files.add(content/'plugins'/rel)
manifest=[];checks=[]
for p in sorted(files):
 data=p.read_bytes(); rel=p.relative_to(root).as_posix()
 manifest.append({'path':rel,'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'lines':len(data.splitlines())})
 cmd=['php','-n','-l',str(p)] if p.suffix=='.php' else ['node','--check',str(p)]
 result=subprocess.run(cmd,capture_output=True,text=True)
 checks.append({'path':rel,'check':'PHP syntax' if p.suffix=='.php' else 'JavaScript syntax','exit_code':result.returncode,'output':(result.stdout+result.stderr).replace(str(root),'SOURCE_ROOT').strip()})
plugins=[]
for d in sorted((content/'plugins').iterdir()):
 if not d.is_dir(): continue
 for p in sorted(d.glob('*.php')):
  head=p.read_text(errors='replace')[:8192]
  name=re.search(r'^\s*\*?\s*Plugin Name:\s*(.+)',head,re.M)
  if not name: continue
  version=re.search(r'^\s*\*?\s*Version:\s*(.+)',head,re.M)
  plugins.append({'directory':d.name,'entry_file':p.relative_to(root).as_posix(),'name':name.group(1).strip(),'version':version.group(1).strip() if version else 'not detected','archived_copy':'.pre-' in d.name,'active_state':'not established from source'})
wp_version=re.search(r"\$wp_version\s*=\s*'([^']+)'",(root/'public_html/wp-includes/version.php').read_text()).group(1)
meta={'captured_at_utc':datetime.now(timezone.utc).isoformat(),'source_root':str(root),'git_metadata_present':(root/'.git').exists(),'snapshot_note':'Local handoff describes public_html as historical July copy, not refreshed by October migration; provenance not independently established. No live equivalence claimed.','files':manifest}
(out/'source-manifest.json').write_text(json.dumps(meta,indent=2)+'\n')
(out/'syntax-checks.json').write_text(json.dumps({'php_version':subprocess.run(['php','-n','-r','echo PHP_VERSION;'],capture_output=True,text=True).stdout,'node_version':subprocess.run(['node','--version'],capture_output=True,text=True).stdout.strip(),'checks':checks,'passed':sum(c['exit_code']==0 for c in checks),'total':len(checks)},indent=2)+'\n')
(out/'component-inventory.json').write_text(json.dumps({'wordpress_local_version':wp_version,'plugins':plugins,'note':'Installed-file inventory only; not a vulnerability scan or production/activation inventory.'},indent=2)+'\n')
print(json.dumps({'syntax_passed':sum(c['exit_code']==0 for c in checks),'syntax_total':len(checks),'php_files':sum(p.suffix=='.php' for p in files),'js_files':sum(p.suffix=='.js' for p in files),'plugin_entries':len(plugins),'archived_plugin_entries':sum(p['archived_copy'] for p in plugins),'wordpress_local_version':wp_version}))
sys.exit(any(c['exit_code'] for c in checks))

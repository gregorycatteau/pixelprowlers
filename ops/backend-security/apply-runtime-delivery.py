"""Targeted VPS delivery of a committed, published and exactly qualified image."""
import hashlib
import json
from pathlib import Path
import re
import runpy
import subprocess
import sys
import time

root=Path('/opt/pixelprowlers-deploy-backups/backend-operations-20261006')
manifest=json.loads(Path(sys.argv[1]).read_text())
if not re.fullmatch('[0-9a-f]{40}',manifest.get('delivery_commit','')):
    raise RuntimeError('A committed revision is required; uncommitted candidates cannot be deployed')
if not manifest.get('remote_branch_verified') or not manifest.get('exact_image_tests_passed') or manifest.get('migrations_required'):
    raise RuntimeError('Publication, exact-image qualification or zero-migration proof missing')
restore=json.loads((root/'restoration-proof.json').read_text())
if not restore.get('actual_production_backup_restored') or not restore.get('schema_ledger_constraints_table_counts_equal'):
    raise RuntimeError('Real production restoration proof missing')
if hashlib.sha256((root/'production.dump').read_bytes()).hexdigest() != (root/'SHA256SUMS').read_text().split()[0]:
    raise RuntimeError('Backup integrity mismatch')
baseline=json.loads((root/'baseline.json').read_text())
def inspect(name):
    result=subprocess.run(['docker','inspect',name],capture_output=True,check=True)
    return json.loads(result.stdout)[0]
for name,container in (('postgres','pixelprowlers-postgres'),('nuxt','pixelprowlers-nuxt')):
    if inspect(container)['Id'] != baseline['containers'][name]['id']:
        raise RuntimeError('Frontend or PostgreSQL baseline changed')
prepare=runpy.run_path(str(Path(__file__).with_name('prepare-runtime-overlay.py')))['prepare']
environment,override=prepare(manifest['image_id'],manifest['delivery_commit'])
command=['docker','compose','-p','pixelprowlers','-f','/opt/pixelprowlers/compose.yml','-f',str(override),
         'up','-d','--no-deps','--no-build','--pull','never','django']
result=subprocess.run(command,env=environment,cwd='/opt/pixelprowlers',capture_output=True)
if result.returncode:
    raise RuntimeError('Targeted recreation failed; inspect identity and apply confined rollback if necessary')
manifest['production_deployed']=True
manifest['container_id']=inspect('pixelprowlers-django')['Id']
(root/'deployed-manifest.json').write_text(json.dumps(manifest,indent=2))
for _ in range(30):
    active=inspect('pixelprowlers-django')
    if active['State'].get('Health',{}).get('Status')=='healthy':
        break
    time.sleep(1)
else:
    raise RuntimeError('Health not verified: apply rollback-confined.py; never restore the database')
if active['Image'] != manifest['image_id']:
    raise RuntimeError('Unexpected active image')
probe='import os;os.environ.setdefault("DJANGO_SETTINGS_MODULE","pixelprowlers.settings");import django;django.setup();from django.db import connection;c=connection.cursor();c.execute("SELECT 1");assert c.fetchone()==(1,)'
result=subprocess.run(['docker','exec','pixelprowlers-django','python','-c',probe],capture_output=True)
if result.returncode:
    raise RuntimeError('Database connection failed: apply confined rollback')
for name,container in (('postgres','pixelprowlers-postgres'),('nuxt','pixelprowlers-nuxt')):
    if inspect(container)['Id'] != baseline['containers'][name]['id']:
        raise RuntimeError('Unexpected unrelated recreation')
print('Backend image and database connection verified; frontend/PostgreSQL identities preserved. Perform public post-delivery checks.')

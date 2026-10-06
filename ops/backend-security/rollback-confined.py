"""Explicit production rollback: persist confinement, verify it, then old image only.

Run on the identified VPS with the protected prepared backup directory as argument.
Never restores a database, removes confinement, or changes the frontend.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import urllib.request
import urllib.error
import runpy

root = Path(sys.argv[1]).resolve()
if root != Path('/opt/pixelprowlers-deploy-backups/backend-operations-20261006'):
    raise RuntimeError('Unknown protected rollback directory')
proof = json.loads((root / 'confinement-proof.json').read_text())
candidate = (root / 'Caddyfile.confined').read_bytes()
if hashlib.sha256(candidate).hexdigest() != proof['candidate_sha256']:
    raise RuntimeError('Confinement integrity mismatch')

def run(args, data=None):
    result = subprocess.run(args, input=data, capture_output=True)
    if result.returncode:
        raise RuntimeError('Rollback command failed; do not restore the old image')
    return result.stdout

active = run(['docker', 'exec', 'caddy', 'cat', '/etc/caddy/Caddyfile'])
if hashlib.sha256(active).hexdigest() not in {proof['caddyfile_original_sha256'], proof['candidate_sha256']}:
    raise RuntimeError('Caddy configuration changed: prepare a new scoped confinement')
run(['docker', 'exec', '-i', 'caddy', 'sh', '-ec',
     'cp -p /etc/caddy/Caddyfile /etc/caddy/Caddyfile.pixelprowlers-next; '
     'cat > /etc/caddy/Caddyfile.pixelprowlers-next; '
     'mv /etc/caddy/Caddyfile.pixelprowlers-next /etc/caddy/Caddyfile'], candidate)
run(['docker', 'exec', 'caddy', 'caddy', 'reload', '--config', '/etc/caddy/Caddyfile', '--adapter', 'caddyfile'])
for path in ('/graphql', '/graphql/', '/graphql/anything'):
    request = urllib.request.Request('https://pixelprowlers.io' + path, data=b'{}', headers={'Content-Type':'application/json'})
    try:
        urllib.request.urlopen(request, timeout=15)
    except urllib.error.HTTPError as error:
        if error.code != 503:
            raise RuntimeError('Confinement not verified; old image forbidden')
    else:
        raise RuntimeError('Confinement not verified; old image forbidden')
baseline=json.loads((root/'baseline.json').read_text())
delivery=json.loads((root/'deployed-manifest.json').read_text())
backend=json.loads(run(['docker','inspect','pixelprowlers-django']))[0]
if backend['Image'] != delivery['image_id']:
    raise RuntimeError('Backend identity changed; confinement retained, rollback stopped')
prepare=runpy.run_path(str(Path(__file__).with_name('prepare-runtime-overlay.py')))['prepare']
environment,override=prepare(baseline['containers']['django']['image'],None,
    expected_active_id=backend['Id'],filename='rollback-runtime.json')
result=subprocess.run(['docker', 'compose', '-p', 'pixelprowlers', '-f', '/opt/pixelprowlers/compose.yml',
     '-f', str(override), 'up', '-d', '--no-deps', '--no-build', '--pull', 'never', 'django'],
     env=environment,cwd='/opt/pixelprowlers',capture_output=True)
if result.returncode:
    raise RuntimeError('Rollback failed; confinement retained')
print('Rollback applied with persistent verified GraphQL confinement; database preserved.')

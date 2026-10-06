"""On the VPS, preserve active Django settings without persisting secret values.

Writes a Compose override containing references only. Returns the subprocess
environment in memory; apply-runtime-delivery.py must use it in the same process.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path('/opt/pixelprowlers-deploy-backups/backend-operations-20261006')
BASE_COMPOSE = '/opt/pixelprowlers/compose.yml'

def capture(args):
    result = subprocess.run(args, cwd='/opt/pixelprowlers', capture_output=True)
    if result.returncode:
        raise RuntimeError('Controlled configuration command failed')
    return result.stdout

def prepare(image, revision, expected_active_id=None, filename='delivery-runtime.json'):
    baseline = json.loads((ROOT / 'baseline.json').read_text())
    active = json.loads(capture(['docker','inspect','pixelprowlers-django']))[0]
    if active['Id'] != (expected_active_id or baseline['containers']['django']['id']):
        raise RuntimeError('Active backend changed; refresh the delivery baseline')
    image_metadata = json.loads(capture(['docker','image','inspect',image]))[0]
    labels = image_metadata['Config'].get('Labels') or {}
    if revision is None:
        if image != baseline['containers']['django']['image']:
            raise RuntimeError('Unlabelled image is not the recorded previous backend')
    elif labels.get('org.opencontainers.image.revision') != revision:
        raise RuntimeError('Qualified revision and image label differ')
    compose = json.loads(capture(['docker','compose','-p','pixelprowlers','-f',BASE_COMPOSE,'config','--format','json']))
    service = compose['services']['django']
    if active['Mounts'] or service.get('volumes') or active['HostConfig']['PortBindings'] or service.get('ports'):
        raise RuntimeError('Django mounts/ports changed from the verified no-mount/no-port baseline')
    if set(active['NetworkSettings']['Networks']) != {'pixelprowlers_default'} or set(service.get('networks',{})) != {'default'}:
        raise RuntimeError('Django network topology changed')
    if service.get('restart') != active['HostConfig']['RestartPolicy']['Name']:
        raise RuntimeError('Django restart policy changed')
    active_env = dict(value.split('=',1) for value in active['Config']['Env'])
    expected = compose['services']['django'].get('environment', {})
    system = {'PATH','HOME','LANG','GPG_KEY','PYTHON_VERSION','PYTHON_SHA256'}
    keys = (set(active_env) | set(expected)) - system
    environment = dict(os.environ)
    references = {}
    for index, key in enumerate(sorted(keys)):
        reference = 'PIXELPROWLERS_DELIVERY_ENV_' + str(index)
        environment[reference] = active_env.get(key, '')
        references[key] = '${' + reference + '}'
    caddy = json.loads(capture(['docker','inspect','caddy']))[0]
    proxy = caddy['NetworkSettings']['Networks']['pixelprowlers_default']['IPAddress']
    environment['PIXELPROWLERS_DELIVERY_PROXY'] = proxy + '/32'
    references['DJANGO_TRUSTED_PROXY_NETWORKS'] = '${PIXELPROWLERS_DELIVERY_PROXY}'
    if active_env.get('EMAIL_BACKEND') != 'django.core.mail.backends.console.EmailBackend':
        raise RuntimeError('Email baseline changed; qualify notification settings first')
    override = {'services': {'django': {'image': image, 'pull_policy': 'never',
        'command': ['gunicorn','pixelprowlers.wsgi:application','--bind','0.0.0.0:8000','--workers','3','--timeout','120'],
        'environment': references}}}
    os.umask(0o077)
    if filename not in {'delivery-runtime.json','rollback-runtime.json','overlay-qualification.json'}:
        raise RuntimeError('Unknown overlay name')
    target = ROOT / filename
    target.write_text(json.dumps(override, indent=2))
    result = subprocess.run(['docker','compose','-p','pixelprowlers','-f',BASE_COMPOSE,'-f',str(target),'config','--format','json'],
        env=environment, cwd='/opt/pixelprowlers', capture_output=True)
    if result.returncode:
        raise RuntimeError('Targeted overlay configuration invalid')
    effective = json.loads(result.stdout)['services']['django']['environment']
    if any(effective.get(key) != active_env.get(key, '') for key in keys):
        raise RuntimeError('Overlay would alter active application settings')
    return environment, target

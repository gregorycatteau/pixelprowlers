"""Read-only HTTP checks; no production form submission, token or client data."""
import json
import urllib.request
import urllib.error

base = 'https://pixelprowlers.io'
for route in ('/', '/reparation-informatique', '/contact', '/_delivery.json'):
    with urllib.request.urlopen(base + route, timeout=15) as response:
        assert response.status == 200
        response.read()
# Invalid selections cannot access records. Production validation must reject them.
for query in ('{contacts{__typename}}', 'mutation{deleteCrmObject(model:"contact",id:"0"){ok}}', '{__schema{queryType{name}}}'):
    request = urllib.request.Request(base+'/graphql/',
        data=json.dumps({'query':query}).encode(),
        headers={'Content-Type':'application/json','Origin':base})
    try:
        response = urllib.request.urlopen(request,timeout=15)
    except urllib.error.HTTPError as response:
        payload = response.read()
    else:
        with response:
            payload = response.read()
    assert json.loads(payload).get('errors')
print('Public pages reachable; private selections and introspection rejected. No submission made.')

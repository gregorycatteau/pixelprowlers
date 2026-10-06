exec(open('/qualification/qualification.py').read().split('args=sys.argv[1:]')[0])
from graphql import parse,validate
from pixelprowlers.schema import schema
import json
ops=json.load(open('/qualification/frontend-contracts.json'))
results=[{'name':x['name'],'errors':[e.message for e in validate(schema.graphql_schema,parse(x['query']))]} for x in ops]
print(json.dumps(results));assert not any(x['errors'] for x in results)

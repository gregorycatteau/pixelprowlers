exec(open('/qualification/qualification.py').read().split('args=sys.argv[1:]')[0])
import json,hashlib
from django.db import connections
from django.test import Client
from crm.models import Contact
connections.databases['restored']={**connections.databases['default'],'HOST':'pixelprowlers-security-restore-20261006'}
def rows(alias,sql):
 with connections[alias].cursor() as c:c.execute(sql);return c.fetchall()
sql="select table_name,column_name,data_type,is_nullable,column_default from information_schema.columns where table_schema='public' order by table_name,ordinal_position"
assert rows('default',sql)==rows('restored',sql)
assert rows('default','select app,name from django_migrations order by app,name')==rows('restored','select app,name from django_migrations order by app,name')
for table in ['crm_contact','crm_contactmessage','audits_auditdossier','audits_auditreponse']:
 original=rows('default',f'select * from {table} order by id')
 assert original
 ids=','.join(str(row[0]) for row in original)
 assert original==rows('restored',f'select * from {table} where id in ({ids}) order by id')
obj=Contact.objects.using('restored').order_by('pk').first()
connections['default'].close();connections.databases['default']['HOST']='pixelprowlers-security-restore-20261006'
c=Client(HTTP_HOST='localhost',HTTP_ORIGIN='http://localhost')
r=c.post('/graphql/',json.dumps({'query':'query($t:String!){contactByToken(token:$t){messages{id}}}','variables':{'t':obj.secret_token}}),content_type='application/json').json()
assert not r.get('errors') and len(r['data']['contactByToken']['messages'])==2
print(json.dumps({'schema_and_migration_ledger_equal':True,'original_synthetic_rows_identical':True,'restored_existing_ticket_followup':True}))

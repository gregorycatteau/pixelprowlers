exec(open('/qualification/qualification.py').read().split('args=sys.argv[1:]')[0])
import json,time
from django.test import Client
from django.db import connection, DatabaseError
from crm.models import Contact,ContactMessage
from audits.models import AuditDossier,AuditReponse
from audits.questions import QUESTION_IDS
client=Client(HTTP_HOST='localhost',HTTP_ORIGIN='http://localhost')
def gql(q,v=None):
 r=client.post('/graphql/',json.dumps({'query':q,'variables':v or {}}),content_type='application/json').json()
 assert not r.get('errors'),r
 return r['data']
q='mutation($s:Float!){createContact(name:"Synthetic restore marker",email:"marker@example.invalid",serviceType:"materiel",message:"Synthetic qualification request for backup and restoration.",privacyConsent:true,startedAt:$s){contact{ticketId secretToken}}}'
a=gql(q,{'s':(time.time()-5)*1000})['createContact']['contact']
gql('query($t:String!){contactByToken(token:$t){ticketId}}',{'t':a['secretToken']})
gql('mutation($t:String!){addContactMessage(token:$t,message:"Synthetic followup",authorName:"Synthetic"){contact{status}}}',{'t':a['secretToken']})
obj=Contact.objects.get(secret_token=a['secretToken']);obj.read=True;obj.save(update_fields=['read']);assert obj.messages.count()==2
# Session writes and audit counter/signature must also work with runtime grants.
b=gql('mutation{createAuditDossier(prenom:"Alice",nom:"Martin",email:"marker@example.invalid",telephone:"0612345678",typePersonne:"individu",consentementRgpd:true){dossier{numeroDossier}}}')
gql('mutation($n:String!,$a:JSONString!){submitAuditReponses(numeroDossier:$n,reponses:$a){statut}}',{'n':b['createAuditDossier']['dossier']['numeroDossier'],'a':json.dumps({k:5 for k in QUESTION_IDS})})
with connection.cursor() as cur:
 cur.execute("select rolsuper,rolcreatedb,rolcreaterole from pg_roles where rolname=current_user")
 assert cur.fetchone()==(False,False,False)
 for sql in ('CREATE DATABASE forbidden_qualification','CREATE ROLE forbidden_qualification','ALTER TABLE crm_contact ADD COLUMN forbidden_qualification text','DROP TABLE crm_contact','CREATE TABLE forbidden_qualification(id int)'):
  try:cur.execute(sql)
  except DatabaseError:pass
  else:raise AssertionError('Unnecessary administration allowed')
print(json.dumps({'runtime_create_read_reply_update':True,'audit_session_signature':True,'admin_sql_denials':5,'superuser_createdb_createrole':False,'contacts':Contact.objects.count(),'messages':ContactMessage.objects.count(),'audits':AuditDossier.objects.count(),'responses':AuditReponse.objects.count()}))

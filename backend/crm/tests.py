"""Security boundary tests use synthetic fixtures and existing Django authentication."""
import json
import time
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core import mail, signing
from django.core.cache import cache
from django.test import Client, TestCase, override_settings
from audits.models import AuditDossier, AuditReponse, RefonteAudit
from audits.questions import QUESTION_IDS
from audits.refonte_questions import REFONTE_QUESTION_IDS
from audits.serializers import AuditSubmitSerializer
from audits import refonte_analysis as analysis
from crm.models import Contact, ContactMessage, DiagnosticTicket
from pixelprowlers.object_access import diagnostic_capability
from pixelprowlers.notifications import safe_send_mail
from pixelprowlers.schema import schema

CREATE = '''mutation($s:Float!){createContact(name:"Synthetic Owner",email:"owner@example.invalid",serviceType:"materiel",message:"Synthetic request with no real customer information.",privacyConsent:true,startedAt:$s){contact{ticketId secretToken messages{author authorName message} emailConfirmation}}}'''
AUDIT = '''mutation{createAuditDossier(prenom:"Alice",nom:"Martin",email:"owner@example.invalid",telephone:"0612345678",typePersonne:"individu",consentementRgpd:true){dossier{numeroDossier statut}}}'''
SUBMIT = '''mutation($n:String!,$a:JSONString!){submitAuditReponses(numeroDossier:$n,reponses:$a){numeroDossier statut}}'''
PRIVATE_QUERIES = ['contacts','contact','unreadContacts','leads','lead','formations','formation','formationRegistrations','formationRegistration','services','service','auditDossier','clientDossier']
PRIVATE_MUTATIONS = ['createLead','updateLeadStatus','createFormation','createFormationRegistration','updateFormationRegistrationStatus','upsertService','deleteCrmObject','sessionInit','recordPageView','recordQuestionInteraction','recordTrackingEvent']

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',DEFAULT_FROM_EMAIL='qualification@example.invalid',CONTACT_TO='qualification@example.invalid')
class SecurityBoundaryTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client(HTTP_HOST='localhost',HTTP_ORIGIN='http://localhost')
        self.other = Client(HTTP_HOST='localhost',HTTP_ORIGIN='http://localhost')
    def gql(self,q,v=None,client=None,**headers):
        return (client or self.client).post('/graphql/',json.dumps({'query':q,'variables':v or {}}),content_type='application/json',**headers)
    def created_contact(self):
        r=self.gql(CREATE,{'s':(time.time()-5)*1000}).json()
        self.assertFalse(r.get('errors'),r)
        return r['data']['createContact']['contact']
    def assert_denied(self,response):
        body=response.json()
        self.assertTrue(body.get('errors'),body)
        self.assertNotIn('owner@example.invalid',json.dumps(body))
        return body
    def test_private_fields_absent_for_anonymous_regular_staff_and_superuser(self):
        User=get_user_model()
        for role in ('anonymous','regular','staff','superuser'):
            if role!='anonymous':
                user=User.objects.create_user(role,is_staff=role in ('staff','superuser'),is_superuser=role=='superuser')
                self.client.force_login(user)
            for name in PRIVATE_QUERIES:
                self.assertNotIn(name,schema.graphql_schema.query_type.fields)
                self.assert_denied(self.gql('{'+name+'{__typename}}'))
            for name in PRIVATE_MUTATIONS:
                self.assertNotIn(name,schema.graphql_schema.mutation_type.fields)
                self.assert_denied(self.gql('mutation{'+name+'{__typename}}'))
            self.client.logout()
    @override_settings(DEBUG=False,SECURE_SSL_REDIRECT=False)
    def test_production_validation_alias_fragments_batch_and_no_partial_write(self):
        self.assert_denied(self.gql('query{alias:contacts{__typename}}'))
        self.assert_denied(self.gql('query{...Private} fragment Private on Query{contacts{__typename}}'))
        q=CREATE.replace('}}}','}} x:deleteCrmObject(model:"contact",id:"1"){ok}}')
        from graphql import parse
        parse(q)
        self.assert_denied(self.gql(q,{'s':(time.time()-5)*1000}))
        self.assertEqual(Contact.objects.count(),0)
        self.assert_denied(self.gql('{__schema{queryType{name}}}'))
        r=self.client.post('/graphql/',json.dumps([{'query':'{contacts{__typename}}'}]),content_type='application/json')
        self.assertEqual(r.status_code,400)
    def test_public_contact_initial_message_and_isolated_tokens(self):
        a=self.created_contact();b=self.created_contact()
        self.assertEqual(Contact.objects.count(),2)
        self.assertEqual(ContactMessage.objects.count(),2)
        q='query($t:String!){contactByToken(token:$t){ticketId messages{authorName message}}}'
        r=self.gql(q,{'t':a['secretToken']},client=self.other).json()
        self.assertEqual(r['data']['contactByToken']['ticketId'],a['ticketId'])
        self.assertNotEqual(a['secretToken'],b['secretToken'])
        for t in (a['ticketId'],'1','B'*43):self.assert_denied(self.gql(q,{'t':t}))
        self.assert_denied(self.gql('query($t:String!){contactByToken(token:$t){clientDossier{email} messages{contact{email}}}}',{'t':a['secretToken']}))
        self.assertEqual(json.loads(a['emailConfirmation'])['status'],'not_configured')
    def test_reply_requires_token_and_author_is_server_owned(self):
        a=self.created_contact()
        q='mutation($t:String!){addContactMessage(token:$t,message:"Synthetic reply",authorName:"ADMIN"){contact{ticketId messages{author authorName}}}}'
        self.assert_denied(self.gql(q,{'t':a['ticketId']}))
        r=self.gql(q,{'t':a['secretToken']}).json();self.assertFalse(r.get('errors'))
        last=ContactMessage.objects.last()
        self.assertEqual(last.author,ContactMessage.Author.CUSTOMER)
        self.assertEqual(last.author_name,'Synthetic Owner')
    def test_notification_failure_keeps_contact_and_initial_message(self):
        with patch('pixelprowlers.notifications.send_mail',side_effect=RuntimeError('synthetic failure')):
            a=self.created_contact()
        self.assertEqual(Contact.objects.count(),1);self.assertEqual(ContactMessage.objects.count(),1)
        self.assertEqual(json.loads(a['emailConfirmation'])['status'],'failed')
    def test_invalid_metadata_does_not_create_partial_contact(self):
        q=CREATE.replace('privacyConsent:true','privacyConsent:true,cms:"<invalid>"')
        self.assert_denied(self.gql(q,{'s':(time.time()-5)*1000}))
        self.assertEqual(Contact.objects.count(),0);self.assertEqual(ContactMessage.objects.count(),0)
    def test_email_links_ignore_untrusted_origin(self):
        self.gql(CREATE,{'s':(time.time()-5)*1000},HTTP_ORIGIN='https://attacker.invalid')
        self.assertTrue(mail.outbox)
        self.assertIn('https://pixelprowlers.io/ticket/',mail.outbox[-1].body)
        self.assertNotIn('attacker.invalid',mail.outbox[-1].body)
    def test_diagnostic_requires_signed_capability_and_rejects_expired_wrong_scope(self):
        ticket=DiagnosticTicket.objects.create(organization='Synthetic',email='owner@example.invalid',message='Test',answers={},diagnostic_result={})
        q='query($t:String!){diagnosticTicket(ticketId:$t){ticketId organization}}'
        cap=diagnostic_capability(ticket)
        self.assertFalse(self.gql(q,{'t':cap}).json().get('errors'))
        for cap_bad in (ticket.ticket_id,str(ticket.pk),cap+'x',signing.dumps({'pk':ticket.pk},salt='wrong-scope')):
            self.assert_denied(self.gql(q,{'t':cap_bad}))
        with patch('django.core.signing.time.time',return_value=time.time()+31*86400):
            self.assert_denied(self.gql(q,{'t':cap}))
    def test_audit_session_grant_blocks_other_browser_and_other_user(self):
        r=self.gql(AUDIT).json();self.assertFalse(r.get('errors'),r)
        n=r['data']['createAuditDossier']['dossier']['numeroDossier']
        args={'n':n,'a':json.dumps({k:5 for k in QUESTION_IDS})}
        self.assert_denied(self.gql(SUBMIT,args,client=self.other))
        self.assert_denied(self.gql(SUBMIT,args,HTTP_ORIGIN='https://attacker.invalid'))
        self.assertEqual(AuditReponse.objects.count(),0)
        self.assertFalse(self.gql(SUBMIT,args).json().get('errors'))
        user=get_user_model().objects.create_user('different-user')
        self.client.force_login(user)
        self.assert_denied(self.gql(SUBMIT,args))
    def test_audit_service_cannot_lookup_raw_reference_without_authorization(self):
        r=self.gql(AUDIT).json();n=r['data']['createAuditDossier']['dossier']['numeroDossier']
        serializer=AuditSubmitSerializer(data={'numero_dossier':n,'reponses':{k:5 for k in QUESTION_IDS}})
        self.assertFalse(serializer.is_valid());self.assertEqual(AuditReponse.objects.count(),0)
    def test_refonte_creation_followup_and_all_analysis_entrypoints_make_no_network(self):
        q='''mutation($a:JSONString!){createRefonteAudit(prenom:"Alice",nom:"Martin",email:"owner@example.invalid",telephone:"0612345678",typePersonne:"individu",siteUrl:"http://127.0.0.1/",consentementRgpd:true,reponses:$a){audit{reference analysisStatus analysisError}}}'''
        with patch('socket.socket.connect',side_effect=AssertionError('network forbidden')),patch('socket.getaddrinfo',side_effect=AssertionError('DNS forbidden')),patch('threading.Thread.start',side_effect=AssertionError('thread forbidden')),patch('subprocess.Popen',side_effect=AssertionError('browser forbidden')):
            r=self.gql(q,{'a':json.dumps({k:'ok' for k in REFONTE_QUESTION_IDS})}).json()
            self.assertFalse(r.get('errors'),r)
            obj=RefonteAudit.objects.get()
            self.assertEqual(obj.site_url,'http://127.0.0.1/')
            self.assertEqual(obj.analysis_status,'non_analysable')
            for url in ('http://127.0.0.1/','http://[::1]/','http://169.254.169.254/','https://example.invalid/redirect'):
                self.assertEqual(analysis.analyze_site(url)['status'],'non_analysable')
                self.assertEqual(analysis.analyze_site_with_playwright(url)['status'],'non_analysable')
                self.assertEqual(analysis.check_resources(url,[url]),[])
                self.assertEqual(analysis.fetch_pagespeed(url)['status'],'unavailable')
                with self.assertRaises(analysis.AutomaticAnalysisDisabled):analysis._request(url)
            analysis.schedule_refonte_analysis(obj.pk);analysis.run_refonte_analysis(obj.pk)
        query='query($r:String!){refonteAudit(reference:$r){reference analysisStatus}}'
        self.assertFalse(self.gql(query,{'r':obj.reference}).json().get('errors'))
        self.assert_denied(self.gql(query,{'r':obj.reference},client=self.other))
    def test_django_admin_requires_staff_and_explicit_model_permissions(self):
        obj=Contact.objects.create(name='Synthetic Owner',email='owner@example.invalid',message='Synthetic')
        path=f'/admin/crm/contact/{obj.pk}/change/'
        self.assertEqual(self.client.get(path).status_code,302)
        staff=get_user_model().objects.create_user('operator',is_staff=True)
        self.client.force_login(staff)
        self.assertEqual(self.client.get(path).status_code,403)
        staff.user_permissions.add(Permission.objects.get(codename='view_contact'))
        self.assertEqual(self.client.get(path).status_code,200)
        self.assertEqual(self.client.post(path,{}).status_code,403)
        staff.user_permissions.add(Permission.objects.get(codename='change_contact'))
        # A permitted incomplete change renders validation, rather than a permission denial.
        self.assertEqual(self.client.post(path,{}).status_code,200)
    def test_email_simulation_is_not_smtp_acceptance(self):
        args=dict(subject='Synthetic',message='Synthetic',from_email='test@example.invalid',recipient_list=['test@example.invalid'])
        for backend in ('console','dummy','filebased','locmem'):
            with override_settings(EMAIL_BACKEND=f'django.core.mail.backends.{backend}.EmailBackend'):
                self.assertEqual(safe_send_mail(**args),'not_configured')
        with override_settings(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'):
            with patch('pixelprowlers.notifications.send_mail',return_value=1):self.assertEqual(safe_send_mail(**args),'sent')
            with patch('pixelprowlers.notifications.send_mail',return_value=0):self.assertEqual(safe_send_mail(**args),'failed')
    def test_session_authorized_creation_requires_allowed_origin_before_writes(self):
        r=self.gql(AUDIT,HTTP_ORIGIN='')
        self.assert_denied(r);self.assertEqual(AuditDossier.objects.count(),0)
    def test_expired_session_grant_is_not_authority(self):
        r=self.gql(AUDIT).json();n=r['data']['createAuditDossier']['dossier']['numeroDossier']
        session=self.client.session
        grants=session['public_object_grants'];grants[0]['expires']=time.time()-1
        session['public_object_grants']=grants;session.save()
        self.assert_denied(self.gql(SUBMIT,{'n':n,'a':json.dumps({k:5 for k in QUESTION_IDS})}))
        self.assertEqual(AuditReponse.objects.count(),0)
    def test_public_urgency_contract_and_private_projection(self):

        # Validation choices are taken from the historical model, not invented fixtures.
        from urgencies.models import UrgencyRequest
        from urgencies.serializers import UrgencyRequestSerializer
        data=dict(problem_type=UrgencyRequest.ProblemType.values[0],impact_level=UrgencyRequest.ImpactLevel.values[0],affected_url='https://example.invalid',short_description='Synthetic outage requiring a controlled qualification request.',since_when='Synthetic today',name='Synthetic Owner',organization='Synthetic',email='owner@example.invalid',phone='0612345678',contact_preference='email',callback_slot='Synthetic morning',expected_next_step=UrgencyRequest.ExpectedNextStep.values[0],consent_to_contact=True,no_secrets_confirmed=True)
        serializer=UrgencyRequestSerializer(data=data)
        self.assertTrue(serializer.is_valid(),serializer.errors)
        def camel(name):
            parts=name.split('_')
            return parts[0]+''.join(p.title() for p in parts[1:])
        args=','.join(camel(k)+':'+json.dumps(v) for k,v in data.items())
        response=self.gql('mutation{createUrgencyRequest('+args+'){reference status clientEmailStatus ticket{reference status}}}').json()
        self.assertFalse(response.get('errors'),response)
        self.assertEqual(response['data']['createUrgencyRequest']['clientEmailStatus'],'not_configured')
        from pixelprowlers.schema import schema
        self.assertEqual(set(schema.graphql_schema.get_type('UrgencyRequestType').fields),{'reference','status'})

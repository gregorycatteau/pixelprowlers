"""No public load tests: a bounded 18-attempt synthetic multiprocessing check."""
import multiprocessing
import tempfile
from types import SimpleNamespace
from unittest.mock import patch
from django.test import SimpleTestCase, override_settings
from pixelprowlers.abuse import allow, client_ip, TrustedProxyMiddleware

def quota_attempt(_):
    return allow(SimpleNamespace(META={'REMOTE_ADDR':'192.0.2.1'}), 'parallel', 5, 600)

class AbuseTests(SimpleTestCase):
    def test_atomic_shared_quota_across_three_processes(self):
        with tempfile.TemporaryDirectory() as directory, override_settings(RATE_LIMIT_DATABASE=directory+'/quota.sqlite3'):
            with multiprocessing.get_context('fork').Pool(3) as pool:
                results=pool.map(quota_attempt,range(18))
            self.assertEqual(sum(results),5)
            with patch('pixelprowlers.abuse.time.time',return_value=99999999999):
                self.assertTrue(quota_attempt(None))

    @override_settings(TRUSTED_PROXY_NETWORKS=['192.0.2.10/32'])
    def test_forwarded_headers_only_from_recognized_peer(self):
        request=SimpleNamespace(META={'REMOTE_ADDR':'198.51.100.9','HTTP_X_FORWARDED_FOR':'203.0.113.2','HTTP_X_FORWARDED_PROTO':'https','HTTP_X_FORWARDED_HOST':'attacker.invalid'})
        self.assertEqual(client_ip(request),'198.51.100.9')
        TrustedProxyMiddleware(lambda r:r)(request)
        self.assertEqual(request.META,{'REMOTE_ADDR':'198.51.100.9'})
        request=SimpleNamespace(META={'REMOTE_ADDR':'192.0.2.10','HTTP_X_FORWARDED_FOR':'203.0.113.2, 198.51.100.9'})
        self.assertEqual(client_ip(request),'198.51.100.9')
        request.META['HTTP_X_FORWARDED_FOR']='malformed'
        self.assertEqual(client_ip(request),'192.0.2.10')

    def test_storage_failure_denies_quota(self):
        with override_settings(RATE_LIMIT_DATABASE='/unavailable/no-directory/quota.sqlite3'):
            self.assertFalse(quota_attempt(None))

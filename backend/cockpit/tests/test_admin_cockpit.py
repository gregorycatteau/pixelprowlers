from unittest.mock import Mock

from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management import call_command
from django.test import Client, RequestFactory, TestCase, override_settings

from cockpit.admin import LogEntryAdmin
from crm.admin import ContactAdmin, ContactMessageAdmin
from crm.models import Contact, ContactMessage
from tracking.admin import TrackingEventAdmin
from tracking.models import TrackingEvent


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class AdminAccessTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()

    def test_anonymous_is_redirected_to_login_without_data(self):
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response["Location"])

    def test_authenticated_non_staff_is_refused(self):
        user = self.user_model.objects.create_user("normal-user", password="test-only-password")
        self.client.force_login(user)
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response["Location"])

    def test_superuser_sees_dashboard_without_secrets(self):
        user = self.user_model.objects.create_superuser("admin-test", password="test-only-password")
        self.client.force_login(user)
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ce qui demande votre attention")
        self.assertContains(response, "cockpit/css/admin.css")
        rendered = response.content.decode().lower()
        self.assertNotIn("secret_token", rendered)
        self.assertNotIn("signature_hmac", rendered)

    def test_staff_dashboard_respects_model_permissions(self):
        user = self.user_model.objects.create_user("staff-test", password="test-only-password", is_staff=True)
        user.user_permissions.add(Permission.objects.get(codename="view_refurbishedmachine"))
        user = self.user_model.objects.get(pk=user.pk)
        self.client.force_login(user)
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Machines disponibles")
        self.assertNotContains(response, "Urgences ouvertes")
        self.assertNotContains(response, "Dernières modifications")

    def test_admin_login_post_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post("/admin/login/", {"username": "nobody", "password": "irrelevant"})
        self.assertEqual(response.status_code, 403)

    def test_session_cookie_security_is_explicit(self):
        from django.conf import settings
        self.assertTrue(settings.SESSION_COOKIE_HTTPONLY)
        self.assertTrue(settings.CSRF_COOKIE_HTTPONLY)
        self.assertEqual(settings.SESSION_COOKIE_SAMESITE, "Lax")
        self.assertTrue(settings.SESSION_EXPIRE_AT_BROWSER_CLOSE)
        self.assertEqual(settings.SESSION_COOKIE_AGE, 28800)
        self.assertEqual(settings.X_FRAME_OPTIONS, "DENY")


class ProvisionAdminCommandTests(TestCase):
    def test_command_creates_unusable_superuser_and_groups_idempotently(self):
        call_command("provision_admin", username="striker", verbosity=0)
        user = get_user_model().objects.get(username="striker")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertFalse(user.has_usable_password())
        self.assertEqual(set(Group.objects.values_list("name", flat=True)), {"Opérations", "Éditorial", "Commercial", "Direction"})
        self.assertTrue(Group.objects.get(name="Direction").permissions.filter(codename="view_logentry").exists())
        self.assertTrue(Group.objects.get(name="Éditorial").permissions.filter(codename="publish_refurbishedmachine").exists())

        call_command("provision_admin", username="striker", verbosity=0)
        self.assertEqual(get_user_model().objects.filter(username="striker").count(), 1)

    def test_existing_password_is_never_replaced(self):
        user = get_user_model().objects.create_user("striker", password="existing-test-only-password")
        original_hash = user.password
        call_command("provision_admin", username="striker", verbosity=0)
        user.refresh_from_db()
        self.assertEqual(user.password, original_hash)
        self.assertTrue(user.is_superuser)


class AdminProtectionTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model().objects.create_superuser("protection-test", password="test-only-password")
        self.request = self.factory.get("/admin/")
        self.request.user = self.user

    def test_contact_sensitive_fields_are_read_only(self):
        model_admin = ContactAdmin(Contact, admin.site)
        readonly = set(model_admin.get_readonly_fields(self.request))
        self.assertTrue({"secret_token", "signature_hmac", "notification_status", "client_dossier"}.issubset(readonly))

    def test_support_message_actor_comes_from_request(self):
        model_admin = ContactMessageAdmin(ContactMessage, admin.site)
        message = ContactMessage(author="customer", author_name="forged", message="Réponse de suivi")
        message.save = Mock()
        model_admin.save_model(self.request, message, form=None, change=False)
        self.assertEqual(message.author, ContactMessage.Author.SUPPORT)
        self.assertEqual(message.author_name, self.user.get_username())

    def test_tracking_is_strictly_read_only(self):
        model_admin = TrackingEventAdmin(TrackingEvent, admin.site)
        self.assertFalse(model_admin.has_add_permission(self.request))
        self.assertFalse(model_admin.has_change_permission(self.request))
        self.assertFalse(model_admin.has_delete_permission(self.request))

    def test_admin_log_is_strictly_read_only(self):
        model_admin = LogEntryAdmin(LogEntry, admin.site)
        self.assertFalse(model_admin.has_add_permission(self.request))
        self.assertFalse(model_admin.has_change_permission(self.request))
        self.assertFalse(model_admin.has_delete_permission(self.request))

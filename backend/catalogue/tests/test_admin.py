from unittest.mock import patch

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.test import RequestFactory, TestCase

from catalogue.admin import RefurbishedMachineAdmin
from catalogue.models import RefurbishedMachine
from catalogue.tests.factories import create_machine


class RefurbishedMachineAdminTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.admin = RefurbishedMachineAdmin(RefurbishedMachine, AdminSite())
        user_model = get_user_model()
        self.superuser = user_model.objects.create_superuser("root", "root@example.invalid", "test-password")
        self.editor = user_model.objects.create_user(
            "editor", "editor@example.invalid", "test-password", is_staff=True
        )
        permissions = Permission.objects.filter(
            codename__in=(
                "view_refurbishedmachine",
                "change_refurbishedmachine",
                "edit_refurbishedmachine_drafts",
                "publish_refurbishedmachine",
                "change_refurbishedmachine_commercial_status",
            )
        )
        self.editor.user_permissions.set(permissions)

    def request_for(self, user):
        request = self.factory.get("/admin/catalogue/refurbishedmachine/")
        request.user = user
        return request

    def test_admin_configuration_has_required_search_filters_fieldsets_and_no_mass_delete(self):
        self.assertTrue({"internal_reference", "title", "brand", "model_name", "slug"}.issubset(self.admin.search_fields))
        self.assertTrue({"status", "commercial_status", "brand", "featured"}.issubset(self.admin.list_filter))
        headings = {heading for heading, _options in self.admin.fieldsets}
        self.assertEqual(
            headings,
            {"Identité", "Présentation", "Caractéristiques", "Interventions et tests", "Disponibilité", "Prix", "SEO", "Publication", "Traçabilité"},
        )
        self.assertNotIn("delete_selected", self.admin.get_actions(self.request_for(self.superuser)))

    def test_save_model_sets_audit_users_and_only_superuser_can_change_reference(self):
        machine = create_machine()
        request = self.request_for(self.editor)
        self.admin.save_model(request, machine, form=None, change=True)
        machine.refresh_from_db()
        self.assertEqual(machine.updated_by, self.editor)

        machine.internal_reference = "EDITOR-CHANGE"
        with self.assertRaises(ValidationError):
            self.admin.save_model(request, machine, form=None, change=True)

        request = self.request_for(self.superuser)
        self.admin.save_model(request, machine, form=None, change=True)
        machine.refresh_from_db()
        self.assertEqual(machine.internal_reference, "EDITOR-CHANGE")

        new_machine = RefurbishedMachine(internal_reference="NEW")
        self.admin.save_model(request, new_machine, form=None, change=False)
        self.assertEqual(new_machine.created_by, self.superuser)
        self.assertEqual(new_machine.updated_by, self.superuser)

    def test_actions_validate_publish_and_transitions_are_idempotent(self):
        valid = create_machine(reference="VALID", slug="valid")
        invalid = RefurbishedMachine.objects.create(internal_reference="INVALID")
        request = self.request_for(self.superuser)
        with patch.object(self.admin, "message_user"):
            self.admin.publish_selected(request, RefurbishedMachine.objects.filter(pk__in=[valid.pk, invalid.pk]))
        valid.refresh_from_db()
        invalid.refresh_from_db()
        self.assertEqual(valid.status, valid.Status.PUBLISHED)
        self.assertEqual(invalid.status, invalid.Status.DRAFT)

        with patch.object(self.admin, "message_user"):
            self.admin.mark_sold(request, RefurbishedMachine.objects.filter(pk=valid.pk))
            valid.refresh_from_db()
            sold_at = valid.sold_at
            self.admin.mark_sold(request, RefurbishedMachine.objects.filter(pk=valid.pk))
        valid.refresh_from_db()
        self.assertEqual(valid.sold_at, sold_at)

    def test_editor_cannot_delete_published_machine_but_superuser_can(self):
        machine = create_machine()
        machine.publish()
        self.assertFalse(self.admin.has_delete_permission(self.request_for(self.editor), machine))
        self.assertTrue(self.admin.has_delete_permission(self.request_for(self.superuser), machine))

    def test_custom_permissions_control_draft_publication_and_commercial_status(self):
        request = self.request_for(self.editor)
        draft = create_machine()
        self.assertTrue(self.admin.has_change_permission(request, draft))
        self.assertTrue(self.admin.has_publish_permission(request))
        self.assertTrue(self.admin.has_commercial_permission(request))

        self.editor.user_permissions.clear()
        self.editor = get_user_model().objects.get(pk=self.editor.pk)
        request = self.request_for(self.editor)
        self.assertFalse(self.admin.has_change_permission(request, draft))
        self.assertFalse(self.admin.has_publish_permission(request))
        self.assertFalse(self.admin.has_commercial_permission(request))

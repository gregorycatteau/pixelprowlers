from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from catalogue.models import RefurbishedMachine
from catalogue.tests.factories import create_machine, machine_data


class RefurbishedMachineModelTests(TestCase):
    def test_draft_can_be_created_and_is_not_published(self):
        machine = create_machine()
        self.assertEqual(machine.status, machine.Status.DRAFT)
        self.assertFalse(RefurbishedMachine.objects.published().exists())

    def test_public_text_rejects_html(self):
        with self.assertRaises(ValidationError):
            create_machine(summary="<script>alert(1)</script>")

    def test_structured_json_rejects_depth_unknown_keys_and_oversized_values(self):
        invalid_values = (
            {"name": "not-a-list"},
            [{"name": "CPU", "nested": {"value": "x"}}],
            [{"name": "CPU", "value": {"nested": True}}],
            [{"name": "CPU", "value": "x" * 501}],
            [{"name": "<b>CPU</b>", "value": "x"}],
        )
        for index, value in enumerate(invalid_values):
            with self.subTest(value=value), self.assertRaises(ValidationError):
                create_machine(reference=f"BAD-{index}", slug=f"bad-{index}", specifications=value)

    def test_negative_price_is_rejected_and_null_price_is_allowed(self):
        create_machine(price_amount=None)
        with self.assertRaises(ValidationError):
            create_machine(reference="BAD-PRICE", slug="bad-price", price_amount=Decimal("-0.01"))

    def test_incomplete_publication_is_rejected(self):
        machine = RefurbishedMachine(**machine_data(title=""))
        machine.status = machine.Status.PUBLISHED
        machine.published_at = timezone.now()
        with self.assertRaises(ValidationError) as error:
            machine.save()
        self.assertIn("title", error.exception.message_dict)

    def test_publication_and_archive_dates_are_validated(self):
        machine = create_machine()
        machine.status = machine.Status.PUBLISHED
        with self.assertRaises(ValidationError):
            machine.save()

        machine.status = machine.Status.ARCHIVED
        machine.commercial_status = machine.CommercialStatus.ARCHIVED
        machine.published_at = timezone.now()
        machine.archived_at = machine.published_at - timedelta(seconds=1)
        with self.assertRaises(ValidationError):
            machine.save()

    def test_internal_reference_is_immutable_without_explicit_superuser_override(self):
        machine = create_machine()
        machine.internal_reference = "CAT-CHANGED"
        with self.assertRaises(ValidationError):
            machine.save()
        machine._allow_internal_reference_change = True
        machine.save()
        self.assertEqual(machine.internal_reference, "CAT-CHANGED")

    def test_slug_is_immutable_after_first_publication(self):
        machine = create_machine()
        machine.publish()
        machine.slug = "new-slug"
        with self.assertRaises(ValidationError):
            machine.save()

    def test_commercial_transitions_validate_dates_and_are_idempotent(self):
        machine = create_machine()
        self.assertTrue(machine.mark_reserved())
        reserved_at = machine.reserved_at
        self.assertFalse(machine.mark_reserved())
        machine.refresh_from_db()
        self.assertEqual(machine.reserved_at, reserved_at)

        self.assertTrue(machine.mark_sold())
        sold_at = machine.sold_at
        self.assertFalse(machine.mark_sold())
        machine.refresh_from_db()
        self.assertEqual(machine.sold_at, sold_at)

        self.assertTrue(machine.mark_available())
        self.assertIsNone(machine.reserved_at)
        self.assertIsNone(machine.sold_at)
        self.assertFalse(machine.mark_available())

    def test_reserved_and_sold_require_their_dates(self):
        for status in (RefurbishedMachine.CommercialStatus.RESERVED, RefurbishedMachine.CommercialStatus.SOLD):
            with self.subTest(status=status), self.assertRaises(ValidationError):
                create_machine(reference=f"BAD-{status}", slug=f"bad-{status}", commercial_status=status)

    def test_archive_transition_is_consistent_and_idempotent(self):
        machine = create_machine()
        self.assertTrue(machine.archive())
        archived_at = machine.archived_at
        self.assertEqual(machine.status, machine.Status.ARCHIVED)
        self.assertEqual(machine.commercial_status, machine.CommercialStatus.ARCHIVED)
        self.assertFalse(machine.archive())
        machine.refresh_from_db()
        self.assertEqual(machine.archived_at, archived_at)


class PublishableManagerTests(TestCase):
    def test_published_filters_drafts_future_publications_and_archives(self):
        now = timezone.now()
        visible = create_machine(reference="VISIBLE", slug="visible")
        visible.publish(at=now - timedelta(minutes=1))
        create_machine(reference="DRAFT", slug="draft")
        future = create_machine(reference="FUTURE", slug="future")
        future.status = future.Status.PUBLISHED
        future.published_at = now + timedelta(days=1)
        future.save()
        archived = create_machine(reference="ARCHIVED", slug="archived")
        archived.archive(at=now)

        self.assertEqual(list(RefurbishedMachine.objects.published()), [visible])

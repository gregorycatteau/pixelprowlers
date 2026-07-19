import json
from datetime import timedelta

from django.test import Client, TestCase, override_settings
from django.utils import timezone

from catalogue.models import RefurbishedMachine
from catalogue.tests.factories import create_machine
from pixelprowlers.schema import schema


class CatalogueGraphQLTests(TestCase):
    query = """
        query Available($first: Int, $after: String) {
          availableMachines(first: $first, after: $after) {
            edges { cursor node { slug title commercialStatus priceAmount } }
            pageInfo { hasNextPage endCursor }
          }
        }
    """

    def publish(self, reference, slug, **overrides):
        published_at = overrides.pop("published_at", None)
        machine = create_machine(reference=reference, slug=slug, **overrides)
        machine.publish(at=published_at or timezone.now())
        return machine

    def execute(self, query=None, variables=None):
        result = schema.execute(query or self.query, variable_values=variables or {})
        self.assertIsNone(result.errors, result.errors)
        return result.data

    def test_available_machine_is_visible_but_draft_future_and_archives_are_hidden(self):
        visible = self.publish("VISIBLE", "visible")
        create_machine(reference="DRAFT", slug="draft")
        future = create_machine(reference="FUTURE", slug="future")
        future.status = future.Status.PUBLISHED
        future.published_at = timezone.now() + timedelta(days=1)
        future.save()
        archived = create_machine(reference="ARCHIVED", slug="archived")
        archived.archive()

        slugs = [edge["node"]["slug"] for edge in self.execute()["availableMachines"]["edges"]]
        self.assertEqual(slugs, [visible.slug])

    def test_reserved_and_sold_are_absent_from_list_but_accessible_by_slug(self):
        reserved = self.publish("RESERVED", "reserved")
        reserved.mark_reserved()
        sold = self.publish("SOLD", "sold")
        sold.mark_sold()
        self.assertEqual(self.execute()["availableMachines"]["edges"], [])

        for machine, expected in ((reserved, "reserved"), (sold, "sold")):
            result = self.execute(
                "query($slug: String!) { refurbishedMachine(slug: $slug) { slug commercialStatus } }",
                {"slug": machine.slug},
            )
            self.assertEqual(result["refurbishedMachine"]["commercialStatus"], expected)

    def test_unknown_draft_future_and_archived_slugs_all_return_null(self):
        draft = create_machine(reference="DRAFT", slug="draft")
        future = create_machine(reference="FUTURE", slug="future")
        future.status = future.Status.PUBLISHED
        future.published_at = timezone.now() + timedelta(days=1)
        future.save()
        archived = create_machine(reference="ARCHIVE", slug="archive")
        archived.archive()
        query = "query($slug: String!) { refurbishedMachine(slug: $slug) { slug } }"
        for slug in (draft.slug, future.slug, archived.slug, "unknown"):
            with self.subTest(slug=slug):
                self.assertIsNone(self.execute(query, {"slug": slug})["refurbishedMachine"])

    def test_pagination_default_maximum_cursor_and_stable_order(self):
        now = timezone.now()
        expected = []
        for index in range(22):
            machine = create_machine(
                reference=f"PAGE-{index:02}",
                slug=f"page-{index:02}",
                featured=index < 2,
                display_order=index,
            )
            machine.publish(at=now - timedelta(minutes=index))
            expected.append(machine.slug)

        first_page = self.execute()["availableMachines"]
        self.assertEqual(len(first_page["edges"]), 20)
        self.assertTrue(first_page["pageInfo"]["hasNextPage"])
        second_page = self.execute(variables={"first": 20, "after": first_page["pageInfo"]["endCursor"]})[
            "availableMachines"
        ]
        actual = [edge["node"]["slug"] for edge in first_page["edges"] + second_page["edges"]]
        self.assertEqual(actual, expected)

        for invalid_first in (0, 51):
            result = schema.execute(self.query, variable_values={"first": invalid_first})
            self.assertIsNotNone(result.errors)
            self.assertFalse(result.data)
        result = schema.execute(self.query, variable_values={"after": "not-a-cursor"})
        self.assertIsNotNone(result.errors)

    def test_public_type_is_an_explicit_allowlist(self):
        fields = set(schema.graphql_schema.get_type("RefurbishedMachineType").fields)
        self.assertEqual(
            fields,
            {
                "slug", "title", "brand", "modelName", "summary", "description",
                "cosmeticCondition", "installedOperatingSystem", "specifications",
                "performedInterventions", "performedTests", "commercialStatus",
                "priceAmount", "currency", "warrantyInformation", "availabilityNote",
                "featured", "seoTitle", "seoDescription", "publishedAt", "updatedAt",
            },
        )
        self.assertTrue({"internalReference", "createdBy", "updatedBy", "internalNotes", "id"}.isdisjoint(fields))

    def test_catalogue_has_no_mutation_and_private_crm_queries_remain_absent(self):
        mutation_fields = set(schema.graphql_schema.mutation_type.fields)
        query_fields = set(schema.graphql_schema.query_type.fields)
        self.assertFalse(any("machine" in field.lower() for field in mutation_fields))
        self.assertTrue({"contacts", "leads", "services"}.isdisjoint(query_fields))

    @override_settings(DEBUG=False)
    def test_http_endpoint_still_blocks_introspection_in_production(self):
        response = Client(HTTP_HOST="localhost").post(
            "/graphql/",
            data=json.dumps({"query": "query { __schema { queryType { name } } }"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIsNotNone(response.json().get("errors"))
        self.assertFalse(response.json().get("data"))

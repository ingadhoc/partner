##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from lxml import etree
from odoo.tests import TransactionCase, tagged
from odoo.tools import mute_logger
from psycopg2 import IntegrityError


@tagged("post_install", "-at_install")
class TestPartnerInternalCode(TransactionCase):
    def test_code_assigned_from_sequence(self):
        sequence = self.env.ref("partner_internal_code.sequence")
        expected = sequence.get_next_char(sequence.number_next_actual)
        partners = self.env["res.partner"].create([{"name": "Partner A"}, {"name": "Partner B"}])
        self.assertEqual(partners[0].internal_code, expected)
        self.assertTrue(partners[1].internal_code)
        self.assertNotEqual(partners[0].internal_code, partners[1].internal_code)

    def test_explicit_code_is_kept(self):
        partner = self.env["res.partner"].create({"name": "Partner C", "internal_code": "MANUAL-001"})
        self.assertEqual(partner.internal_code, "MANUAL-001")

    def test_copy_gets_new_code(self):
        partner = self.env["res.partner"].create({"name": "Partner D"})
        copy = partner.copy()
        self.assertTrue(copy.internal_code)
        self.assertNotEqual(copy.internal_code, partner.internal_code)

    def test_code_must_be_unique(self):
        self.env["res.partner"].create({"name": "Partner E", "internal_code": "DUP-001"})
        with self.assertRaises(IntegrityError), mute_logger("odoo.sql_db"):
            self.env["res.partner"].create({"name": "Partner F", "internal_code": "DUP-001"})
            self.env.flush_all()

    def test_search_by_code(self):
        partner = self.env["res.partner"].create({"name": "Partner G", "internal_code": "FIND-001"})
        self.assertEqual(self.env["res.partner"].search([("internal_code", "=", "FIND-001")]), partner)

    def test_field_in_views(self):
        Partner = self.env["res.partner"]
        for view_type in ("list", "form", "search"):
            arch = Partner.get_view(view_type=view_type)["arch"]
            self.assertIn('name="internal_code"', arch, view_type)

    def test_list_column_before_name(self):
        arch = etree.fromstring(self.env["res.partner"].get_view(view_type="list")["arch"])
        names = [field.get("name") for field in arch.iter("field")]
        self.assertEqual(names.index("internal_code") + 1, names.index("display_name"))

    def test_search_name_filter_includes_code(self):
        arch = etree.fromstring(self.env["res.partner"].get_view(view_type="search")["arch"])
        name_field = arch.xpath("//field[@name='name']")[0]
        self.assertIn("internal_code", name_field.get("filter_domain"))

##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from lxml import etree
from odoo.tests import TransactionCase, tagged
from odoo.tools import mute_logger
from odoo.tools.safe_eval import safe_eval
from psycopg2 import IntegrityError


@tagged("post_install", "-at_install")
class TestPartnerInternalCode(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Acme Internal Code",
                "internal_code": "IC-9876",
                "vat": "VAT-9876",
            }
        )
        # its name carries the code of the one above and sorts before it, so the native
        # search returns it first and fills a limit of one
        cls.named = cls.env["res.partner"].create({"name": "AAA IC-9876 Branch"})

    def _search_box_domain(self, term):
        """The domain the web client builds when typing in the Contacts search box."""
        view = self.env["res.partner"].get_view(self.env.ref("base.view_res_partner_filter").id, "search")
        field = etree.fromstring(view["arch"]).xpath("//search/field[@name='name']")[0]
        return safe_eval(field.get("filter_domain"), {"self": term})

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
        self.assertEqual(names.index("internal_code") + 1, names.index("complete_name"))

    def test_internal_code_reaches_both_search_surfaces(self):
        """The code finds the contact on both surfaces, exactly, and takes nothing from the core."""
        partners = self.env["res.partner"]
        with self.subTest("the code finds the contact on a contact field of a document"):
            self.assertIn(self.partner.id, [res[0] for res in partners.name_search("IC-9876")])
        with self.subTest("the code finds the contact on the Contacts search box"):
            self.assertIn(self.partner, partners.search(self._search_box_domain("IC-9876")))
        with self.subTest("part of the code does not find the contact"):
            self.assertNotIn(self.partner, partners.search(self._search_box_domain("IC-98")))
        with self.subTest("the box still finds by the fields the core searches"):
            self.assertIn(self.partner, partners.search(self._search_box_domain("VAT-9876")))
        with self.subTest("the exact code takes the only suggestion the limit allows"):
            results = partners.name_search("IC-9876", limit=1)
            self.assertEqual([res[0] for res in results], [self.partner.id])

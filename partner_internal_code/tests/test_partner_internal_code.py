##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from lxml import etree
from odoo.tests import TransactionCase, tagged
from odoo.tools.safe_eval import safe_eval


@tagged("post_install", "-at_install")
class TestPartnerInternalCode(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Acme Internal Code",
                "internal_code": "IC-9876",
                "company_registry": "REG-9876",
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
            self.assertIn(self.partner, partners.search(self._search_box_domain("REG-9876")))
        with self.subTest("the exact code takes the only suggestion the limit allows"):
            results = partners.name_search("IC-9876", limit=1)
            self.assertEqual([res[0] for res in results], [self.partner.id])

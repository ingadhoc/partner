##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo.exceptions import AccessError
from odoo.tests import HttpCase, TransactionCase, new_test_user, tagged


@tagged("post_install", "-at_install")
class TestPortalPartnerState(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.portal_user = new_test_user(cls.env, login="portal_partner_state", groups="base.group_portal")
        field = cls.env["ir.model.fields"]._get("res.partner", "name")
        cls.state_field = cls.env["res.partner.state_field"].create({"field_id": field.id})

    def test_portal_reads_state_fields(self):
        records = self.env["res.partner.state_field"].with_user(self.portal_user).search([])
        self.assertIn(self.state_field, records)
        self.assertEqual(records.field_id.mapped("name"), records.sudo().field_id.mapped("name"))

    def test_portal_cannot_write_state_fields(self):
        with self.assertRaises(AccessError):
            self.state_field.with_user(self.portal_user).write({"approval": False})

    def test_portal_reads_only_partner_fields(self):
        fields = self.env["ir.model.fields"].with_user(self.portal_user).search([])
        self.assertTrue(fields)
        self.assertEqual(set(fields.mapped("model")), {"res.partner"})


@tagged("post_install", "-at_install")
class TestPortalPartnerStateHttp(HttpCase):
    def test_portal_home(self):
        new_test_user(self.env, login="portal_partner_state", groups="base.group_portal")
        self.authenticate("portal_partner_state", "portal_partner_state")
        response = self.url_open("/my")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.url.endswith("/my"), "the portal user was redirected to the login")

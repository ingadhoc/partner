##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

import odoo.tests.common as common
from odoo.exceptions import UserError


class TestPartnerCreationAccess(common.TransactionCase):
    def setUp(self):
        super().setUp()
        # Usuario solo con el grupo Portal: no es partner manager ni public,
        # asi que con sus propios permisos no puede crear contactos.
        self.portal_user = self.env["res.users"].create(
            {
                "name": "Portal Test User",
                "login": "portal_test_user",
                "email": "portal_test_user@example.com",
                "group_ids": [(6, 0, [self.env.ref("base.group_portal").id])],
            }
        )

    def test_create_partner_portal_with_sudo(self):
        """Un usuario portal en modo superusuario (self.env.su) puede crear
        contactos: replica el flujo del express checkout de website_sale, que
        crea direcciones con res.partner.sudo().create()."""
        partner = self.env["res.partner"].with_user(self.portal_user).sudo().create({"name": "Demo User"})
        self.assertTrue(partner.exists())
        self.assertEqual(partner.name, "Demo User")

    def test_create_partner_portal_without_sudo(self):
        """Un usuario portal con sus propios permisos (sin sudo) sigue sin poder
        crear contactos desde la interfaz."""
        msg = "You don't have access to create contacts"
        with self.assertRaisesRegex(UserError, msg):
            self.env["res.partner"].with_user(self.portal_user).create({"name": "Demo User"})

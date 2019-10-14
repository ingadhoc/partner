##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

import odoo.tests.common as common
from odoo.exceptions import UserError


class TestPartnerState(common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner = self.env.ref('base.res_partner_1')

    def test_partner_state_pending(self):
        self.partner.partner_state_pending()

    def test_partner_state_potential(self):
        self.partner.partner_state_potential()

    def test_partner_state_approved(self):
        self.partner.partner_state_approved()

    def test_partner_state_block_edition(self):
        self.partner.partner_state_approved()
        msg = 'You can not modify this field "name"'
        with self.assertRaisesRegexp(UserError, msg):
            self.partner.name = 'new name'

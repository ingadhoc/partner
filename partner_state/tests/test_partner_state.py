# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################

import openerp.tests.common as common


class TestPartnerState(common.TransactionCase):

    def setUp(self):
        super(TestPartnerState, self).setUp()
        self.partner = self.env.ref('base.res_partner_1')

    def test_partner_state_pending(self):
        self.partner.partner_state_pending()

    def test_partner_state_potential(self):
        self.partner.partner_state_potential()

    def test_partner_state_approved(self):
        self.partner.partner_state_approved()

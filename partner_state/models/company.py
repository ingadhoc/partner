# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################

from openerp import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    partner_state = fields.Boolean(
        'Use partner state?'
    )

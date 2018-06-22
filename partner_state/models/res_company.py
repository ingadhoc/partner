##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    partner_state_enable = fields.Boolean(
        'Use partner state?',
        default=True,
        oldname='partner_state',
    )

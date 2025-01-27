##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    partner_state_enable = fields.Boolean(
        "Use partner state?",
        default=True,
    )

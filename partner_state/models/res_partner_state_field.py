##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import models, fields


class ResPartnerStateField(models.Model):
    _name = 'res.partner.state_field'
    _description = 'Partner State Fields'

    field_id = fields.Many2one(
        'ir.model.fields',
        string='Field',
        required=True,
        domain=[('model_id.model', '=', 'res.partner')]
    )
    approval = fields.Boolean(
        'Approval?',
        help="Required for Approval",
        default=True
    )
    track = fields.Boolean(
        'Track?',
        help="Track and, if change, go back to Potencial",
        default=True
    )
    block_edition = fields.Boolean(
        help="Do not allow to edit this field if the partner is approved",
        default=True,
    )

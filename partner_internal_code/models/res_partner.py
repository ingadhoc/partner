##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models, api


class Partner(models.Model):

    _inherit = 'res.partner'

    internal_code = fields.Char(
        'Internal Code',
        copy=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('internal_code'):
                vals['internal_code'] = self.env['ir.sequence'].next_by_code('partner.internal.code')
        return super().create(vals)

    _sql_constraints = {
        ('internal_code_uniq', 'unique(internal_code)',
            'Internal Code must be unique!')
    }

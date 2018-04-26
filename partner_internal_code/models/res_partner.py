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

    # we let this to base nane search improoved
    # def name_search(self, cr, uid, name, args=None,
    #                 operator='ilike', context=None, limit=100):
    #     args = args or []
    #     res = []
    #     if name:
    #         recs = self.search(
    #             cr, uid, [('internal_code', operator, name)] + args,
    #             limit=limit, context=context)
    #         res = self.name_get(cr, uid, recs)
    #     res += super(partner, self).name_search(
    #         cr, uid,
    #         name=name, args=args, operator=operator, limit=limit)
    #     return res

    @api.model
    def create(self, vals):
        if not vals.get('internal_code', False):
            vals['internal_code'] = self.env[
                'ir.sequence'].next_by_code('partner.internal.code') or '/'
        return super(Partner, self).create(vals)

    _sql_constraints = {
        ('internal_code_uniq', 'unique(internal_code)',
            'Internal Code mast be unique!')
    }

##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import fields, models


class partner(models.Model):

    _inherit = 'res.partner'
    abc_sales_amount = fields.Char('ABC Sales amount')

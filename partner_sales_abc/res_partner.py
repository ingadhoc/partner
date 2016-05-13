# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################

from openerp import fields, models, api



class partner(models.Model):

    _inherit = 'res.partner'

    abc_sales_amount = fields.Char('ABC Sales amount')

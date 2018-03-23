# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields
import odoo.addons.decimal_precision as dp


class res_partner_sample(models.Model):
    _name = "res.partner.sample"
    _description = "Partner Samples"
    _order = 'delivery_date desc'

    delivery_date = fields.Date(
        string='Delivery Date',
        required=True,
        default=fields.Date.context_today)
    user_id = fields.Many2one(
        'res.users',
        required=True,
        default=lambda self: self.env.user,
        string='User',)
    partner_id = fields.Many2one(
        'res.partner',
        required=True,
        string='Partner')
    product_id = fields.Many2one(
        'product.product',
        required=True,
        string='Product')
    quantity = fields.Float(
        'Quantity',
        required=True,
        digits=dp.get_precision('Product UoS'))
    return_date = fields.Date(
        string='Return Date',)


class res_partner(models.Model):
    _inherit = "res.partner"

    sample_ids = fields.One2many(
        'res.partner.sample',
        'partner_id',
        'Samples')

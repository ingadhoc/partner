# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from openerp import fields, models


class res_partner_course(models.Model):

    """"""

    _name = 'res.partner.course'
    _description = 'Res Partner Course'

    name = fields.Char(
        string='Name',
        required=True
    )
    partner_id = fields.Many2many(
        'res.partner',
        'res_partner_course_rel',
        'course_id',
        'partner_id',
        string='Partners'
    )

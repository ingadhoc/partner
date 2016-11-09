# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import Warning


class partner_area(models.Model):
    _name = 'res.partner.area'
    _description = 'Area'
    name = fields.Char(string='Name',
                       required=True)

    @api.model
    def create(self, vals):
        if 'from_m2m' not in self._context:
            raise Warning(_('You can only '
                            'create Areas from companies!'))
        return super(partner_area, self).create(vals)


class res_partner(models.Model):
    _inherit = "res.partner"

    area_ids = fields.Many2many(
        'res.partner.area',
        string='Areas')
    parent_area_ids = fields.Many2many('res.partner.area',
                                       'partner_area_rel',
                                       'parent_id',
                                       'area_ids',
                                       string='Parent Areas')
    area_id = fields.Many2one('res.partner.area',
                              string='Area')

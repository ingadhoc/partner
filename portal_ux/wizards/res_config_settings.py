from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    allow_portal_on_companies = fields.Boolean(
        string="Use Company as Portal User",
        help="Add company partner to the partners to add to portal access")

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            allow_portal_on_companies=self.env['ir.config_parameter']
            .sudo().get_param('portal_ux.allow_portal_on_companies')
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'portal_ux.allow_portal_on_companies',
            self.allow_portal_on_companies)

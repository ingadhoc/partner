from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    allow_portal_on_companies = fields.Boolean(
        string="Allow companies to be portal users",
        help="Add functionality to allow companies (parents partners)"
        " to be portal users, by default odoo does not show parent"
        " companies on invite to portal wizard")

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(allow_portal_on_companies=get_param(
            'portal_ux.allow_portal_on_companies',
            'False').lower() == 'true'
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('portal_ux.allow_portal_on_companies',
                  repr(self.allow_portal_on_companies))

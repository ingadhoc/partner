from odoo import api, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model_create_multi
    def create(self, vals):
        if not self.env.user.has_group("base.group_partner_manager") and not self.env.user.has_group(
            "base.group_public"
        ):
            raise UserError(
                "You don't have access to create contacts. Only users with the 'Contact Creation' access can do it."
            )
        return super().create(vals)

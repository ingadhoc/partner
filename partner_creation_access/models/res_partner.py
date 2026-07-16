from odoo import api, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model_create_multi
    def create(self, vals):
        # No restringimos las creaciones hechas en modo superusuario (self.env.su):
        # son flujos de sistema que elevan privilegios a proposito (por ejemplo, el
        # express checkout de website_sale, que crea direcciones con
        # res.partner.sudo().create()). La restriccion solo aplica a usuarios que
        # crean contactos con sus propios permisos desde la interfaz.
        if (
            not self.env.su
            and not self.env.user.has_group("base.group_partner_manager")
            and not self.env.user.has_group("base.group_public")
        ):
            raise UserError(
                "You don't have access to create contacts. Only users with the 'Contact Creation' access can do it."
            )
        return super().create(vals)

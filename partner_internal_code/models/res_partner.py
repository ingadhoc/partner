##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import api, fields, models
from odoo.fields import Domain


class Partner(models.Model):
    _inherit = "res.partner"

    internal_code = fields.Char(
        copy=False,
        index="btree_not_null",
        help="Unique code for the contact; if left empty it is assigned automatically, and "
        "you can also use it to search for the contact.",
    )

    _internal_code_uniq = models.Constraint(
        "unique (internal_code)",
        "Internal Code must be unique!",
    )

    @api.model
    def _search_display_name(self, operator, value):
        """The code is matched exactly: it is a short sequence every contact has."""
        domain = super()._search_display_name(operator, value)
        if not value or not isinstance(value, str):
            return domain
        if operator in Domain.NEGATIVE_OPERATORS or not operator.endswith("like"):
            return domain
        return Domain.OR([domain, Domain("internal_code", "=", value)])

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("internal_code"):
                vals["internal_code"] = self.env["ir.sequence"].next_by_code("partner.internal.code")
        return super().create(vals_list)

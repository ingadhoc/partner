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

    @api.model
    def name_search(self, name="", domain=None, operator="ilike", limit=100):
        """The exact code goes first, because the native OR comes back ordered by complete_name and
        cut by limit. Hooked here too: a module that replaces name_search skips _search_display_name."""
        results = super().name_search(name, domain, operator, limit)
        if not name or not isinstance(name, str):
            return results
        if operator in Domain.NEGATIVE_OPERATORS or not operator.endswith("like"):
            return results
        partner = self.search(Domain(domain or Domain.TRUE) & Domain("internal_code", "=", name), limit=1)
        if not partner:
            return results
        results = [(partner.id, partner.display_name)] + [res for res in results if res[0] != partner.id]
        return results[:limit] if limit else results

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("internal_code"):
                vals["internal_code"] = self.env["ir.sequence"].next_by_code("partner.internal.code")
        return super().create(vals_list)

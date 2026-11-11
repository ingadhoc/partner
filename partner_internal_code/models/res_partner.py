##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
import logging

from odoo import api, fields, models
<<<<<<< d23ecdfac17cc5f16d87b964d9b38718b9981b4b
from odoo.fields import Domain
||||||| be9a347cd56daef5a9db4fa64d30d14abaaa567c
=======
from odoo.modules.db import FunctionStatus
from odoo.tools import create_index

_logger = logging.getLogger(__name__)

INTERNAL_CODE_TRIGRAM_INDEX = "res_partner__internal_code_trgm_index"
# Same flag as base_ux partner search indexes; read directly to avoid the dependency.
TRIGRAM_FLAG_PARAM = "saas_feature.partner_search_trigram_index"
>>>>>>> 1df1d9c1bfac5b633022acf6314f7464a2b32ddd


class Partner(models.Model):
    _inherit = "res.partner"

    internal_code = fields.Char(
        copy=False,
        index="btree_not_null",
        help="Unique code for the contact; if left empty it is assigned automatically, and "
        "you can also use it to search for the contact.",
    )

<<<<<<< d23ecdfac17cc5f16d87b964d9b38718b9981b4b
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

||||||| be9a347cd56daef5a9db4fa64d30d14abaaa567c
=======
    def init(self):
        super().init()
        self._create_internal_code_trigram_index()

    def _create_internal_code_trigram_index(self):
        """Add a gin trigram index for ILIKE on internal_code.

        It goes next to the btree index of the field, with its own name: an
        index="trigram" on the field would make the registry drop the btree and
        rebuild it as gin without CONCURRENTLY, and the btree is what serves "=".
        Only runs when the feature flag is on, so the rollout goes base by base.
        """
        flag = self.env["ir.config_parameter"].sudo().get_param(TRIGRAM_FLAG_PARAM, "")
        if flag.strip().lower() not in ("1", "true", "yes"):
            return
        registry = self.env.registry
        # Logged at info: a WARNING during install turns the runbot build red.
        if not registry.has_trigram:
            _logger.info("pg_trgm is missing: %s is not created.", INTERNAL_CODE_TRIGRAM_INDEX)
            return
        # Without an IMMUTABLE unaccent the index would not match the ORM query.
        if registry.has_unaccent != FunctionStatus.INDEXABLE:
            _logger.info("unaccent is not indexable: %s is not created.", INTERNAL_CODE_TRIGRAM_INDEX)
            return
        create_index(
            self.env.cr,
            indexname=INTERNAL_CODE_TRIGRAM_INDEX,
            tablename="res_partner",
            expressions=[registry.unaccent('"internal_code"') + " gin_trgm_ops"],
            method="gin",
        )

>>>>>>> 1df1d9c1bfac5b633022acf6314f7464a2b32ddd
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("internal_code"):
                vals["internal_code"] = self.env["ir.sequence"].next_by_code("partner.internal.code")
        return super().create(vals_list)

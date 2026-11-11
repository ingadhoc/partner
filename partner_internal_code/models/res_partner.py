##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
import logging

from odoo import api, fields, models
from odoo.modules.db import FunctionStatus
from odoo.tools import create_index

_logger = logging.getLogger(__name__)

INTERNAL_CODE_TRIGRAM_INDEX = "res_partner__internal_code_trgm_index"
# Same flag as base_ux partner search indexes; read directly to avoid the dependency.
TRIGRAM_FLAG_PARAM = "saas_feature.partner_search_trigram_index"


class Partner(models.Model):
    _inherit = "res.partner"

    internal_code = fields.Char(
        copy=False,
        index="btree_not_null",
    )

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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("internal_code"):
                vals["internal_code"] = self.env["ir.sequence"].next_by_code("partner.internal.code")
        return super().create(vals_list)

    _sql_constraints = {("internal_code_uniq", "unique(internal_code)", "Internal Code must be unique!")}

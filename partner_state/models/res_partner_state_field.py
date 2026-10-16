##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import api, fields, models


class ResPartnerStateField(models.Model):
    _name = "res.partner.state_field"
    _description = "Partner State Fields"

    field_id = fields.Many2one(
        "ir.model.fields",
        string="Field",
        required=True,
        domain=[("model_id.model", "=", "res.partner")],
        ondelete="cascade",
    )
    approval = fields.Boolean("Approval?", help="Required for Approval", default=True)
    changes = fields.Boolean("Changes?", help="Track changes of the partner in the chatter box")
    native_tracking = fields.Boolean(compute="_compute_native_tracking")
    chatter_tracking = fields.Boolean(
        compute="_compute_chatter_tracking",
        inverse="_inverse_chatter_tracking",
        help="Fields with native tracking are always tracked.",
    )
    track = fields.Boolean("Track?", help="Track and, if change, go back to Potencial", default=True)
    block_edition = fields.Boolean(
        help="Do not allow to edit this field if the partner is approved",
        default=True,
    )

    @api.depends("field_id.tracking")
    def _compute_native_tracking(self):
        for line in self:
            line.native_tracking = bool(line.field_id.tracking)

    @api.depends("changes", "native_tracking")
    def _compute_chatter_tracking(self):
        for line in self:
            line.chatter_tracking = line.changes or line.native_tracking

    def _inverse_chatter_tracking(self):
        for line in self.filtered(lambda x: not x.native_tracking):
            line.changes = line.chatter_tracking

    @api.onchange("track")
    def _compute_changes(self):
        if self.track:
            self.changes = True

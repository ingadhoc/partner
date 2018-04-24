##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResPartnerStateField(models.Model):
    _name = 'res.partner.state_field'
    _description = 'Partner State Fields'

    field_id = fields.Many2one(
        'ir.model.fields',
        string='Field',
        required=True,
        domain=[('model_id.model', '=', 'res.partner')]
    )
    approval = fields.Boolean(
        'Approval?',
        help="Required for Approval",
        default=True
    )
    track = fields.Boolean(
        'Track?',
        help="Track and, if change, go back to Potencial",
        default=True
    )


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_state_enable = fields.Boolean(
        compute='_compute_partner_state_enable',
    )

    @api.multi
    def _compute_partner_state_enable(self):
        if self.env.user.company_id.partner_state:
            partners = self.filtered(lambda r:
                                     r.commercial_partner_id == r)
            partners.update({'partner_state_enable': True})

    partner_state = fields.Selection(
        '_get_partner_states',
        string='Partner State',
        readonly=True,
        required=True,
        default='potential'
    )

    @api.model
    def _get_partner_states(self):
        return [
            ('potential', _('Potential')),
            ('pending', _('Pending Approval')),
            ('approved', _('Approved'))]

    @api.multi
    def write(self, vals):
        for partner in self.filtered(lambda r:
                                     r.partner_state in
                                     ['approved', 'pending']):
            fields = partner.check_fields('track')
            if fields:
                fields_set = set(fields)
                vals_set = set(vals)
                if fields_set & vals_set:
                    partner.partner_state_potential()

        return super(ResPartner, self).write(vals)

    @api.multi
    def partner_state_potential(self):
        self.update({'partner_state': 'potential'})

    @api.multi
    def partner_state_pending(self):
        self.ensure_one()
        fields = self.check_fields('approval')
        if not fields:
            self.partner_state = 'pending'
            return

        partner_data = self.read(fields)[0]
        if all(partner_data.values()):
            self.partner_state = 'pending'
            return
        for partner_field, value in partner_data.items():
            if not value:
                raise UserError(_(
                    "Can not request approval, "
                    "required field %s" % (
                        partner_field)))
        self.partner_state = 'pending'

    @api.multi
    def partner_state_approved(self):
        self.check_partner_approve()
        self.partner_state = 'approved'

    @api.multi
    def check_partner_approve(self):
        user_can_approve_partners = self.env[
            'res.users'].has_group('partner_state.approve_partners')
        if not user_can_approve_partners:
            raise UserError(
                _("User can't approve partners, "
                    "please check user permissions!"))
        return True

    @api.multi
    def check_fields(self, field_type):
        ret = False
        for rec in self.filtered(lambda x: x.partner_state_enable):
            partner_field_ids = rec.env['res.partner.state_field'].search([])
            if field_type == 'approval':
                ret = [
                    field.field_id.name for field in partner_field_ids if
                    field.approval]
            elif field_type == 'track':
                ret = [
                    field.field_id.name for field in partner_field_ids if
                    field.track]
        return ret

    @api.model
    def _get_tracked_fields(self, updated_fields):
        tracked_fields = []
        # TODO we should use company of modified partner
        for line in self.env['res.partner.state_field'].search([]):
            if line.track and line.field_id.name in updated_fields:
                tracked_fields.append(line.field_id.name)

        if tracked_fields:
            return self.fields_get(tracked_fields)
        return super(ResPartner, self)._get_tracked_fields(updated_fields)

    @api.multi
    def message_track(self, tracked_fields, initial_values):
        """
        We need to set attribute temporary because message_track read it
        from field properties to make message
        """
        # TODO we should use company of modified partner
        for line in self.env['res.partner.state_field'].search([(
                'track', '=', True)]):
            field = self._fields[line.field_id.name]
            setattr(field, 'track_visibility', 'always')
        return super(ResPartner, self).message_track(
            tracked_fields, initial_values)

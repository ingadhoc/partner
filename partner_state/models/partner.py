# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################

from openerp import models, fields, api, _
from openerp.exceptions import Warning


class res_partner_state_field(models.Model):
    _name = 'res.partner.state.field'
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

    company_partner_state = fields.Boolean(
        compute='_compute_company_partner_state',
    )

    @api.one
    def _compute_company_partner_state(self):
        self.company_partner_state = self.env.user.company_id.partner_state

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
        for partner in self:
            if partner.partner_state in ['approved', 'pending']:
                fields = partner.check_fields('track')
                if fields:
                    fields_set = set(fields)
                    vals_set = set(vals)
                    if fields_set & vals_set:
                        partner.partner_state_potential()

        ret = super(ResPartner, self).write(vals)

        return ret

    @api.multi
    def partner_state_potential(self):
        self.partner_state = 'potential'

    @api.multi
    def partner_state_pending(self):
        fields = self.check_fields('approval')
        if fields:
            partners_read = self.read(fields)
            for partner_read in partners_read:
                for partner_field in partner_read:
                    partner_name = self.browse(partner_read['id']).display_name
                    if not partner_read[partner_field]:
                        raise Warning(_(
                            "Can not request approval, "
                            "required field %s empty on partner  %s!" % (
                                partner_field, partner_name)))
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
            raise Warning(
                _("User can't approve partners, "
                    "please check user permissions!"))
        return True

    @api.multi
    def check_fields(self, field_type):
        ret = False
        if self.company_partner_state:
            partner_field_ids = self.env['res.partner.state.field'].search([])
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
        for line in self.env['res.partner.state.field'].search([]):
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
        for line in self.env['res.partner.state.field'].search([]):
            if line.track:
                field = self._fields[line.field_id.name]
                setattr(field, 'track_visibility', 'always')
        return super(ResPartner, self).message_track(
            tracked_fields, initial_values)

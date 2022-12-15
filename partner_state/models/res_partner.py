##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################

from odoo import models, fields, tools, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_state_enable = fields.Boolean(
        compute='_compute_partner_state_enable',
    )

    partner_state = fields.Selection(
        [('potential', 'Potential'), ('pending', 'Pending pproval'), ('approved', 'Approved')],
        string='Partner State',
        readonly=True,
        required=True,
        default='potential',
        copy=False,
    )

    def _compute_partner_state_enable(self):
        self.partner_state_enable = False
        if self.env.company.partner_state_enable:
            partners = self.filtered(lambda r:
                                     r.commercial_partner_id == r)
            partners.partner_state_enable = True

    def write(self, vals):
        ResPartnerStateField = self.env['res.partner.state_field']
        for partner in self.filtered(lambda r:
                                     r.partner_state in
                                     ['approved', 'pending']):
            partner_block_fields = ResPartnerStateField.search(
                [('block_edition', '=', True)]).mapped('field_id.name')
            modified_fields = vals.keys()
            # if it's a contact we only check the none commercial fields to
            # allow them to be synchronized from parent
            if partner.commercial_partner_id != partner:
                modified_fields = list(
                    set(modified_fields) - set(self._commercial_fields()))

            for key in modified_fields:
                if key in partner_block_fields:
                    raise UserError(
                        _('You can not modify this field "%s"' % (key)))
            fields = partner.check_fields('track')
            if fields:
                fields_set = set(fields)
                vals_set = set(modified_fields)
                if fields_set & vals_set:
                    partner.partner_state_potential()
        return super().write(vals)

    def partner_state_potential(self):
        self.write({'partner_state': 'potential'})

    def partner_state_pending(self):
        for rec in self:
            fields = rec.check_fields('approval')
            if not fields:
                rec.partner_state = 'pending'
                continue
            partner_data = rec.read(fields)[0]
            if all(partner_data.values()):
                rec.partner_state = 'pending'
                continue
            for partner_field, value in partner_data.items():
                if not value:
                    raise UserError(_(
                        'Partner "%s" can not request approval, '
                        'required field %s' % (
                            rec.display_name, partner_field)))

    def partner_state_approved(self):
        self.check_partner_approve()
        self.write({'partner_state': 'approved'})

    def check_partner_approve(self):
        user_can_approve_partners = self.env[
            'res.users'].has_group('partner_state.approve_partners')
        if not user_can_approve_partners:
            raise UserError(
                _("User can't approve partners, "
                    "please check user permissions!"))
        return True

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

    @tools.ormcache('self.env.uid', 'self.env.su')
    def _track_get_fields(self):
        tracked_fields = []
        # TODO we should use company of modified partner
        for line in self.env['res.partner.state_field'].search([]):
            if line.track:
                tracked_fields.append(line.field_id.name)
        if tracked_fields:
            return set(self.fields_get(tracked_fields))
        return super()._track_get_fields()

    def _message_track(self, tracked_fields, initial_values):
        """
        We need to set attribute temporary because message_track read it
        from field properties to make message
        """
        # TODO we should use company of modified partner
        for line in self.env['res.partner.state_field'].search([(
                'track', '=', True)]):
            field = self._fields[line.field_id.name]
            setattr(field, 'track_visibility', 'always')
        return super()._message_track(
            tracked_fields, initial_values)

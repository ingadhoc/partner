from odoo import models, api
from odoo.tools.safe_eval import safe_eval


class PortalWizard(models.TransientModel):
    _inherit = 'portal.wizard'

    @api.onchange('portal_id')
    def onchange_portal_id(self):
        super(PortalWizard, self).onchange_portal_id()
        allow_portal_on_companies = safe_eval(
            self.env['ir.config_parameter'].sudo().get_param(
                'portal_ux.allow_portal_on_companies',
                'False'))
        if not allow_portal_on_companies:
            return None
        user_ids = self.user_ids
        partner_ids = self.env.context.get('active_ids', [])
        contact_ids = set()
        user_changes = []
        for partner in self.env['res.partner'].sudo().browse(partner_ids):
            # si no tiene hijos entonces ya fue agregado
            if not partner.child_ids:
                continue
            for contact in [partner]:
                # make sure that each contact appears at most once in the list
                if contact.id not in contact_ids:
                    contact_ids.add(contact.id)
                    in_portal = False
                    if contact.user_ids:
                        in_portal = self.portal_id in [
                            g.id for g in contact.user_ids[0].groups_id]
                    user_changes.append((0, 0, {
                        'partner_id': contact.id,
                        'email': contact.email,
                        'in_portal': in_portal,
                    }))
        self.user_ids = user_changes + [(4, user.id) for user in user_ids]

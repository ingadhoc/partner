from odoo import models, SUPERUSER_ID
from odoo.tools.safe_eval import safe_eval


class PortalWizard(models.TransientModel):
    _inherit = 'portal.wizard'

    def onchange_portal_id(self, cr, uid, ids, portal_id, context=None):
        res = super(PortalWizard, self).onchange_portal_id(
            cr, uid, ids, portal_id, context=context)
        allow_portal_on_companies = safe_eval(
            self.pool('ir.config_parameter').get_param(
                cr, SUPERUSER_ID, 'portal_usability.allow_portal_on_companies',
                'False'))
        if not allow_portal_on_companies:
            return res
        res_partner = self.pool.get('res.partner')
        partner_ids = context and context.get('active_ids') or []
        contact_ids = set()
        user_changes = []
        for partner in res_partner.browse(
                cr, SUPERUSER_ID, partner_ids, context):
            # si no tiene hijos entonces ya fue agregado
            if not partner.child_ids:
                continue
            for contact in [partner]:
                # make sure that each contact appears at most once in the list
                if contact.id not in contact_ids:
                    contact_ids.add(contact.id)
                    in_portal = False
                    if contact.user_ids:
                        in_portal = portal_id in [
                            g.id for g in contact.user_ids[0].groups_id]
                    user_changes.append((0, 0, {
                        'partner_id': contact.id,
                        'email': contact.email,
                        'in_portal': in_portal,
                    }))
        res['value']['user_ids'] += user_changes
        return res

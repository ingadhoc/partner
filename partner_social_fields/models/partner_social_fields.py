# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################

from openerp import models, fields, api


class ResPartner(models.Model):
    '''
    Add social media to res.partner
    '''
    _inherit = 'res.partner'

    facebook = fields.Char(
    )
    twitter = fields.Char(
    )
    skype = fields.Char(
    )

    @api.multi
    def goto_facebook(self):
        self.ensure_one()
        partner = self
        if partner.facebook:
            good_starting_urls = [
                'https://facebook.com/', 'https://www.facebook.com/',
                'http://facebook.com/', 'http://www.facebook.com/']
            non_protocol_starting_urls = ['facebook.com/', 'www.facebook.com/']

            if any(map(lambda x: partner.facebook.startswith(
                    x), good_starting_urls)):
                url = partner.facebook
            elif any(map(lambda x: partner.facebook.startswith(
                    x), non_protocol_starting_urls)):
                url = 'https://' + partner.facebook
            else:
                url = 'https://www.facebook.com/' + partner.facebook

            return {'type': 'ir.actions.act_url', 'url': url, 'target': 'new'}

    @api.multi
    def goto_twitter(self):
        self.ensure_one()
        partner = self
        if partner.twitter:
            good_starting_urls = [
                'https://twitter.com/', 'https://www.twitter.com/',
                'http://twitter.com/', 'http://www.twitter.com/']
            non_protocol_starting_urls = ['twitter.com/', 'www.twitter.com/']

            if any(map(lambda x: partner.twitter.startswith(
                    x), good_starting_urls)):
                url = partner.twitter
            elif any(map(lambda x: partner.twitter.startswith(
                    x), non_protocol_starting_urls)):
                url = 'https://' + partner.twitter
            else:
                url = 'https://www.twitter.com/' + partner.twitter

            return {'type': 'ir.actions.act_url', 'url': url, 'target': 'new'}

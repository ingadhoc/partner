# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models


class partner_configuration(models.TransientModel):
    _name = 'partner.config.settings'
    _inherit = 'res.config.settings'

    group_disabilities = fields.Boolean(
        "Show Disabilities Information",
        implied_group='partner_person.person_disabilities',
        help="Show Disabilities Information Tab")
    group_person_ni = fields.Boolean(
        "Show National Identity",
        implied_group='partner_person.person_ni',
        help="Show National Identity Field in Personal Information Tab")
    group_person_passport = fields.Boolean(
        "Show Passport",
        implied_group='partner_person.person_passport',
        help="Show Passport Field in Personal Information Tab")
    group_person_marital_information = fields.Boolean(
        "Show Marital Information",
        implied_group='partner_person.personal_marital_information',
        help="Show Marital Status, Husband and Wife Fields in Personal "
        "Information Tab")
    group_person_birthdate = fields.Boolean(
        "Show Birthdate",
        implied_group='partner_person.person_birthdate',
        help="Show Birthdate Field in Personal Information Tab")
    group_person_family = fields.Boolean(
        "Show Family Information",
        implied_group='partner_person.person_family',
        help="Show Mother, Father and Childs Fields in Personal Information "
        "Tab")
    group_person_nationality = fields.Boolean(
        "Show Nationality",
        implied_group='partner_person.person_nationality',
        help="Show Nationality Field in Personal Information Tab")

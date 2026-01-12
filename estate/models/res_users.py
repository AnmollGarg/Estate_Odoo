from odoo import fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        'real_estate_property',
        'sales_person_id',
        string='Properties',
        domain=[('state', 'in', ['new', 'offer_rec'])]
    )

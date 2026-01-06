from odoo import fields, models

class RealEstatePropertyTags(models.Model):
    _name = 'real_estate_property_tags'
    _description = 'RealEstatePropertyTags'

    name = fields.Char(required=True)

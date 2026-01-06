from odoo import fields, models

class RealEstatePropertyType(models.Model):
    _name = 'real_estate_property_type'
    _description = 'RealEstatePropertyType'

    name = fields.Char(required=True)

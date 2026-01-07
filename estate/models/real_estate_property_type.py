from odoo import fields, models

class RealEstatePropertyType(models.Model):
    _name = 'real_estate_property_type'
    _description = 'RealEstatePropertyType'

    name = fields.Char(required=True)
    _sql_constraints = [
        ('check_unique_type_name', 'UNIQUE(name)', 'The TYpe Name will be unique')]
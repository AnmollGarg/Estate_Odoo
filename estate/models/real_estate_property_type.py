from odoo import fields, models

class RealEstatePropertyType(models.Model):
    _name = 'real_estate_property_type'
    _description = 'RealEstatePropertyType'

    name = fields.Char(required=True)
    property_ids = fields.One2many("real_estate_property", "property_type_id", string="Properties")

    _sql_constraints = [
        ('check_unique_type_name', 'UNIQUE(name)', 'The TYpe Name will be unique')]
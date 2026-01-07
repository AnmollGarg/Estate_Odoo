from odoo import fields, models

class RealEstatePropertyTags(models.Model):
    _name = 'real_estate_property_tags'
    _description = 'RealEstatePropertyTags'

    name = fields.Char(required=True)
    _sql_constraints = [
        ('check_unique_tags_name', 'UNIQUE(name)', 'The Tags Name will be unique')]
from odoo import fields, models, api

class RealEstatePropertyType(models.Model):
    _name = 'real_estate_property_type'
    _description = 'RealEstatePropertyType'

    name = fields.Char(required=True)
    property_ids = fields.One2many("real_estate_property", "property_type_id", string="Properties")
    offer_ids = fields.One2many("real_estate_property_offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ('check_unique_type_name', 'UNIQUE(name)', 'The TYpe Name will be unique')]
from odoo import fields, models

class RealEstateProperty(models.Model):
    _name = 'real_estate_property'
    _description = 'RealEstate'

    name = fields.Char(required=True, default='Unknown')
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([('horizontal', 'Horizontal'), ('vertical', 'Vertical')])
    active = fields.Boolean(default=False)
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')])
    property_type_id = fields.Many2one('real_estate_property_type')
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    sales_person_id = fields.Many2one("res.users", string="Sales Person", index=True, tracking=True, default=lambda self: self.env.user)
    tags_id = fields.Many2many("real_estate_property_tags", string="Tags")


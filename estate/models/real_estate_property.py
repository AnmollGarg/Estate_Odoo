from odoo import fields, models
from odoo import api
from odoo.exceptions import UserError , ValidationError


class RealEstateProperty(models.Model):
    _name = 'real_estate_property'
    _description = 'RealEstate'
    _order = 'id desc'

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
    state = fields.Selection([('new','New'), ('offer_rec', 'Offer Received'), ('offer_acc', 'Offer Accepted'), ('sold', 'Sold'), ('cancel','Cancel')], default='new')
    property_type_id = fields.Many2one('real_estate_property_type')
    buyer_id = fields.Many2one("res.partner")
    sales_person_id = fields.Many2one("res.users", string="Sales Person", index=True, tracking=True, default=lambda self: self.env.user)
    tags_id = fields.Many2many("real_estate_property_tags", string="Tags")
    offer_id = fields.One2many("real_estate_property_offer", "property_id")
    total_area = fields.Integer(compute='_compute_total_area')
    best_offer_price = fields.Float(compute='_compute_best_offer_price')



    #sum of living and garden area = total area
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    #best price based on offer , max of offer prices
    @api.depends('offer_id.price', 'offer_id.status')
    def _compute_best_offer_price(self):
        for record in self:
            valid_offers = record.offer_id.filtered(
                lambda o: o.status != 'refused'
            )
            record.best_offer_price = max(
                valid_offers.mapped('price'),
                default=0.0
            )

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'horizontal'
            else:
                record.garden_area = 0
                record.garden_orientation = False

    def action_sold(self):
        for record in self:
            if record.state == 'cancel':
                raise UserError("A cancelled property cannot be sold.")
            record.state = 'sold'

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("A sold property cannot be cancelled.")
            record.state = 'cancel'

    _sql_constraints = [('check_expected_price_positive', 'CHECK(expected_price > 0)', 'The expected price will be in positive only')]
    _sql_constraints =[('check_selling_price_positive', 'CHECK(selling_price > 0)', 'The selling price will be in positive only')]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price and record.expected_price:
                min_price = record.expected_price * 0.9
                if record.selling_price < min_price:
                    raise ValidationError(
                        "Selling price must be at least 90% of the expected price."
                    )

    @api.depends('offer_id')
    def _compute_best_offer_price(self):
        for record in self:
            valid_offers = record.offer_id.filtered(lambda o: o.status != 'refused')
            record.best_offer_price = max(valid_offers.mapped('price'), default=0.0)
            # Mark property as offer received if any valid offer exists and state is 'new'
            if valid_offers and record.state == 'new':
                record.state = 'offer_rec'




from datetime import timedelta

from odoo import fields, models
from odoo.odoo import api
from odoo.exceptions import UserError


class RealEstatePropertyOffer(models.Model):
    _name = 'real_estate_property_offer'
    _description = 'RealEstatePropertyOffer'

    price = fields.Float(string='Price')
    property_id = fields.Many2one("real_estate_property", string='Property')

    status = fields.Selection([('accepted', 'Accepted'),('refused', 'Refused')], string='Status')
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    validity = fields.Integer()
    date_deadline = fields.Date(compute='_compute_date_deadline',inverse='_inverse_date_deadline')

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date
            if create_date:
                offer.date_deadline = create_date.date() + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                delta = offer.date_deadline - offer.create_date.date()
                offer.validity = delta.days

    def action_confirm(self):
        for offer in self:
            if offer.property_id.state == 'sold':
                raise UserError("Property is already sold.")

            # refuse other offers
            other_offers = offer.property_id.offer_id - offer
            other_offers.write({'status': 'refused'})

            # accept this offer
            offer.status = 'accepted'

            # UPDATE PROPERTY
            offer.property_id.write({
                'selling_price': offer.price,
                'buyer_id': offer.buyer_id.id,
                'state': 'offer_acc',
            })


    def action_refused(self):
        for record in self:
            record.status = 'refused'

    _sql_constraints = [
        ('check_offer_price_positive', 'CHECK(price > 0)', 'The offer price will be in positive only')]



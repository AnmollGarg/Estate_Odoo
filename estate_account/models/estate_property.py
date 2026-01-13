from odoo import models

class RealEstateAccount(models.Model):
    _inherit = 'real_estate_property'

    def action_sold(self):
        for record in self:
            self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': record.buyer_id.id,
                'invoice_line_ids': [
                    (0, 0, {
                        'name': f'Property Sale: {record.name}',
                        'quantity': 1,
                        'price_unit': record.selling_price,
                    }),

                    (0, 0, {
                        'name': 'Commission (6%)',
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),

                    (0, 0, {
                        'name': 'Administrative fees',
                        'quantity': 1,
                        'price_unit': 100.0,
                    }),
                ],
            })

        return super().action_sold()

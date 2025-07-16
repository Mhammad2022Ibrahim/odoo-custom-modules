from email.policy import default

from odoo import api, fields, models

class VetAppointmentLine(models.Model):
    _name = 'vet.appointment.line'
    _description = 'Vet Appointment Line'

    appointment_id = fields.Many2one('vet.appointment', string='Appointment')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    qty = fields.Integer(string='Quantity', default=1)
    price = fields.Float(string='Price', compute='_compute_price', store=True)

    @api.depends('product_id')
    def _compute_price(self):
        for record in self:
            record.price = record.product_id.list_price if record.product_id else 0.0


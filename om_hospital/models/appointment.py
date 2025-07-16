from odoo import api, fields, models

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread']
    _description = 'Hospital Appointment'
    _rec_names_search = ['reference', 'patient_id']
    _rec_name = 'patient_id'

    reference = fields.Char(string='Reference', default='New')

    # patient_id = fields.Many2one('hospital.patient', string='Patient', ondelete='cascade')
    patient_id = fields.Many2one('hospital.patient', string='Patient', ondelete='restrict', required=False)
    appointment_date = fields.Date(string='Appointment Date')
    note = fields.Text(string='Note')
    state = fields.Selection([
        ('draft', 'Draft'),('confirmed', 'Confirmed'),('ongoing','Ongoing'),
        ('done','Done'), ('cancelled', 'Cancelled')
        ], default='draft', tracking=True)
    appointment_line_ids = fields.One2many(
        'hospital.appointment.line', 'appointment_id', string='Lines'
    )
    total_qty = fields.Float(
        compute='_compute_total_qty', string='Total Quantities', store=True
    ) #this field is not stored in database and if we need to store  it we need add store=True
    date_of_birth = fields.Date(related='patient_id.date_of_birth', store=True,
                                groups='om_hospital.group_hospital_doctor')
    # this field is not store in database and if we need to store it we need add store=True



    @api.model_create_multi
    def create(self, vals_list):
        # print("odoo mates", vals_list)
        for val in vals_list:
            if not val.get('reference') or val['reference'] == 'New':
                val['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super().create(vals_list)


    def _compute_display_name(self):
        for record in self:
            record.display_name = f"[{record.reference}] {record.patient_id.name}"

    @api.depends('appointment_line_ids', 'appointment_line_ids.qty')
    def _compute_total_qty(self):
        # first method
        # for record in self:
        #     total_qty = 0
        #     print(f"line_id: {record.appointment_line_ids}")
        #     for line in record.appointment_line_ids:
        #         print(f"line value: {line.qty}")
        #         total_qty += line.qty
        #     record.total_qty = total_qty

        # second method
        for record in self:
            # print(record.appointment_line_ids.mapped('qty')) # return a list of qty
            record.total_qty = sum(record.appointment_line_ids.mapped('qty'))


    def action_confirm(self):
        for record in self:
            record.state = 'confirmed'

    def action_ongoing(self):
        for record in self:
            record.state = 'ongoing'

    def action_done(self):
        for record in self:
            record.state = 'done'

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'


class HospitalAppointmentLine(models.Model):
    _name = 'hospital.appointment.line'
    _description = 'Hospital Appointment Line'

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    qty = fields.Float(string='Quantity')


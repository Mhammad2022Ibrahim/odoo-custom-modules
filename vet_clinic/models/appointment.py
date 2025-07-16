from odoo import api, fields, models

class VetAppointment(models.Model):
    _name = 'vet.appointment'
    _inherit = ['mail.thread']
    _description = 'Vet Appointment'
    _rec_names_search = ['reference', 'owner_id']
    _rec_name = 'owner_id'

    # reference = fields.Char(string='Reference', default='New')
    reference = fields.Char(
        string='Reference',
        required=True,
        readonly=True,
        default='New'
        # lambda self: self.env['ir.sequence'].next_by_code('vet.appointment')
    )

    # owner_id = fields.Many2one('pet.owner', string='Owner', ondelete='cascade')
    owner_id = fields.Many2one('pet.owner', string='Owner', ondelete='restrict', required=False)
    appointment_date = fields.Date(string='Appointment Date')
    type_appointment = fields.Selection([
        ('vaccine', 'Vaccine'),
        ('surgery', 'Surgery'),
        ('check-up', 'Check-up')
    ])
    note = fields.Text(string='Note')
    state = fields.Selection([
        ('draft', 'Draft'),('confirmed', 'Confirmed'),('ongoing','Ongoing'),
        ('done','Done'), ('cancelled', 'Cancelled')
        ], default='draft', tracking=True)
    appointment_line_ids = fields.One2many(
        'vet.appointment.line', 'appointment_id', string='Lines'
    )
    total_qty = fields.Float(
        compute='_compute_total_qty', string='Total Quantities', store=True
    ) #this field is not stored in database and if we need to store  it we need add store=True
    total_price = fields.Float(
        compute='_compute_total_price', string='Total Price', store=True
    )

    # his_pet = fields.One2many(related='owner_id.his_pet', store=True,)
                                # groups='om_hospital.group_hospital_doctor')

    pet_id = fields.Many2one(
        'pet.pet',
        string='Pet',
        domain="[('owner_id', '=', owner_id)]",
    )

    # pet_ids = fields.Many2many(
    #     'pet.pet',
    #     compute='_compute_pet_ids',
    #     string='Pets',
    #     store=False,
    # )

    # @api.depends('owner_id')
    # def _compute_pet_ids(self):
    #     for rec in self:
    #         rec.pet_ids = rec.owner_id.his_pet

    # this field is not store in database and if we need to store it we need add store=True



    @api.model_create_multi
    def create(self, vals_list):
        # print("odoo mates", vals_list)
        for val in vals_list:
            if not val.get('reference') or val['reference'] == 'New':
                val['reference'] = self.env['ir.sequence'].next_by_code('vet.appointment')
        return super().create(vals_list)

    def _compute_display_name(self):
        for record in self:
            record.display_name = f"[{record.reference}] {record.owner_id.name}"

    @api.depends('appointment_line_ids', 'appointment_line_ids.qty')
    def _compute_total_qty(self):
        for record in self:
            record.total_qty = sum(record.appointment_line_ids.mapped('qty'))

    @api.depends('appointment_line_ids.price', 'appointment_line_ids.qty')
    def _compute_total_price(self):
        for record in self:
            record.total_price = sum(line.price * line.qty for line in record.appointment_line_ids)

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
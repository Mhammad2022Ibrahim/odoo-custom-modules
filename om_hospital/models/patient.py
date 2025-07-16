from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import date

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread']
    _description = 'Patient Master'

    name = fields.Char(string="Patient Name", required=True, tracking=True)
    date_of_birth = fields.Date(string="Date of Birth", tracking=True)
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')]
        , string="Gender", tracking=True
    )
    tag_ids = fields.Many2many(
        'patient.tag',  # related model
        'patient_tag_rel',  # relation table name
        'patient_id',  # column for this record's ID
        'tag_id',  # column for related record's ID
        string="Patient Tags", # field label
        tracking=True
    ) # the patient_tag_rel is the name of new table with columns patient_id and tag_id

    is_kid = fields.Boolean(string="Kid", compute="_compute_is_kid", store=True, tracking=True)
    parent = fields.Char(string="Parent", tracking=True)
    weight = fields.Float(string="Weight", tracking=True)

    # product_ids = fields.Many2many(
    #     'product.product', string="Product IDs"
    # ) # or we can create without specification the table name

    @api.ondelete(at_uninstall=False)
    def _check_patient_appointment(self):
        for record in self:
            domain = [('patient_id','=',record.id)]
            appointments = self.env['hospital.appointment'].search(domain)
            if appointments:
                raise ValidationError(_(
                    f"You cannot delete this patient {record.name}.\n"
                    f"Delete their linked appointments first: {', '.join(appointments.mapped('reference'))}"
                ))

    @api.depends('date_of_birth')
    def _compute_is_kid(self):
        for record in self:
            if record.date_of_birth:
                today = date.today()
                age = today.year - record.date_of_birth.year - (
                    (today.month, today.day) < (record.date_of_birth.month, record.date_of_birth.day)
                )
                record.is_kid = age < 10
            else:
                record.is_kid = False # If date_of_birth is not provided, default to False (not a kid).


    # def unlink(self):
    #     # we can perform anything here
    #     for record in self:
    #         domain = [('patient_id','=',record.id)]
    #         appointments = self.env['hospital.appointment'].search(domain)
    #         if appointments:
    #             # raise ValidationError(_(f"You cannot delete this patient {record.name}.\n"
    #             #                         f" Delete before his linked appointment {[appointment.reference for appointment in appointments]}"))
    #             # or
    #             # raise ValidationError(_(
    #             #     f"You cannot delete this patient {record.name}.\n"
    #             #     f"Delete their linked appointments first: {', '.join(appointments.mapped('reference'))}"
    #             # ))
    #             # or
    #             raise UserError(_(
    #                 f"You cannot delete this patient {record.name}.\n"
    #                 f"Delete their linked appointments first: {', '.join(appointments.mapped('reference'))}"
    #             ))
    #     return super().unlink()


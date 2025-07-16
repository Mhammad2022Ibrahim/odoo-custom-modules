from odoo import api, fields, models, _

class Pet(models.Model):
    _name = 'pet.pet'
    _description = 'Pet Model'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name', required=True,tracking=True)
    pet_type = fields.Selection([
        ('cat','Cat'),
        ('dog','Dog'),
        ('sheep','Sheep'),
        ('goat','Goat'),
        ('other','Other')
    ],string='Type',required=True,tracking=True)
    # age = fields.Char(string='Age',required=True,tracking=True)
    DOB = fields.Date(string='DOB', required=True,tracking=True)
    owner_id = fields.Many2one(
        'pet.owner',
        string='Owner',
        required=True,
        tracking=True
    )

    vaccine_ids = fields.One2many(
        'pet.vaccine',
        'pet_id',
        string='Vaccines',
        tracking=True,
    )
    vaccine_date = fields.Date(related='vaccine_ids.vaccine_date', store=True)

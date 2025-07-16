from odoo import api, fields, models, _

class Owner(models.Model):
    _name = 'pet.owner'
    _description = 'Pet Owner'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name', required=True,tracking=True)
    address = fields.Char(string='Address',tracking=True)
    phone = fields.Char(string='Phone',tracking=True, required=True)
    email = fields.Char(string='Email',tracking=True)

    # One owner can have many pets
    his_pet = fields.One2many(
        'pet.pet',  # target model
        'owner_id',  # reverse field name
        string='His Pet(s)',
        tracking=True,
    )

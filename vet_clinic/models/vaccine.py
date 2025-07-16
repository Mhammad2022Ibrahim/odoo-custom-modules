from odoo import api, fields, models, _

class Vaccine(models.Model):
    _name = 'pet.vaccine'
    _description = 'Pet Vaccines'
    _inherit = ['mail.thread']
    _rec_name = 'vaccine_type'
    '''the _rec_name attribute is used to specify which field will be 
    displayed as the record's name in views and dropdown lists (like selection fields or many2one relations).'''

    # name = fields.Char(string='Vaccine', required=True,tracking=True)
    code = fields.Char(string='Code', readonly=True, required=True, tracking=True, default='New')
    vaccine_type = fields.Selection(
        [
            ('rabies','Rabies'),
            ('parvo','Parvo'),
            ('distemper','Distemper'),
            ('leptospirosis','Leptospirosis'),
            ('canine adenovirus','Canine Adenovirus'),
            ('dog vaccine','Dog Vaccine'),
            ('bordetella','Bordetella')
        ]
    )
    description = fields.Char(string='Description', tracking=True)
    vaccine_date = fields.Date(string='Vaccine Date', required=True, tracking=True)
    pet_id = fields.Many2one(
        'pet.pet',
        string='Pet Vaccine',
        tracking=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        # print("odoo mates", vals_list)
        for val in vals_list:
            if not val.get('code') or val['code'] == 'New':
                val['code'] = self.env['ir.sequence'].next_by_code('pet.vaccine')
        return super().create(vals_list)
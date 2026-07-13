from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    gender = fields.Selection(
        [('female', 'Femenino'), ('male', 'Masculino'), ('other', 'Otro')],
        string='Género',
    )

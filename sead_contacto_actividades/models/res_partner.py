from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    actividad_economica_id = fields.Many2one(
        'actividad.economica',
        string='Actividad Económica',
    )

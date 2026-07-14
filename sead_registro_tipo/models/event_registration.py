from odoo import fields, models


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    registration_type_id = fields.Many2one(
        'event.registration.type',
        string='Tipo de Registro',
        ondelete='restrict',
        index=True,
    )

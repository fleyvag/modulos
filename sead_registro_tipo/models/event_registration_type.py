from odoo import fields, models


class EventRegistrationType(models.Model):
    _name = 'event.registration.type'
    _description = 'Tipo de Registro para Asistentes'
    _order = 'sequence, name'

    name = fields.Char(string='Nombre', required=True, translate=True)
    description = fields.Text(string='Descripción', translate=True)
    sequence = fields.Integer(string='Secuencia', default=10)
    color = fields.Integer(string='Color')
    active = fields.Boolean(string='Activo', default=True)

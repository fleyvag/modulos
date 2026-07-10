from odoo import models, fields


class EventCategory(models.Model):
    _name = 'event.category'
    _description = 'Categoría de Evento'
    _order = 'name'

    name = fields.Char('Nombre', required=True, translate=True)

from odoo import fields, models


class ActividadPadre(models.Model):
    _name = 'actividad.padre'
    _description = 'Actividad Padre'

    actividad = fields.Char(string='Actividad', required=True)

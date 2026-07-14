from odoo import fields, models


class ActividadPadre(models.Model):
    _name = 'actividad.padre'
    _description = 'Actividad Padre'
    _rec_name = 'actividad'

    actividad = fields.Char(string='Actividad', required=True)

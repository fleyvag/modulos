from odoo import api, fields, models


class ActividadEconomica(models.Model):
    _name = 'actividad.economica'
    _description = 'Actividad Económica'

    actividad = fields.Char(string='Actividad', required=True)
    actividad_padre_id = fields.Many2one(
        'actividad.padre',
        string='Actividad Padre',
        required=True,
    )
    nombre_completo = fields.Char(
        string='Nombre Completo',
        compute='_compute_nombre_completo',
        store=True,
        readonly=True,
    )

    @api.depends('actividad_padre_id.actividad', 'actividad')
    def _compute_nombre_completo(self):
        for record in self:
            partes = []
            if record.actividad_padre_id:
                partes.append(record.actividad_padre_id.actividad)
            if record.actividad:
                partes.append(record.actividad)
            record.nombre_completo = ' / '.join(partes)

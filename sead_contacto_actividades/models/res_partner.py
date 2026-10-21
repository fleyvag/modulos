from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    actividad_economica_ids = fields.Many2many(
        'actividad.economica',
        'res_partner_actividad_economica_rel',
        'partner_id',
        'actividad_id',
        string='Actividades Económicas',
    )
    actividad_padre_ids = fields.Many2many(
        'actividad.padre',
        'res_partner_actividad_padre_rel',
        'partner_id',
        'padre_id',
        string='Actividades Padre',
        compute='_compute_actividad_padre_ids',
        store=True,
        readonly=True,
    )
    vendedor_auspicio_id = fields.Many2one(
        'res.users',
        string='Vendedor Auspicio',
        domain=[('share', '=', False)],
    )
    tamano_empresa = fields.Selection(
        [
            ('grande', 'Grande'),
            ('medio', 'Medio'),
            ('pequeno', 'Pequeño'),
        ],
        string='Tamaño de la Empresa',
    )

    @api.depends('actividad_economica_ids.actividad_padre_id')
    def _compute_actividad_padre_ids(self):
        for partner in self:
            partner.actividad_padre_ids = partner.actividad_economica_ids.actividad_padre_id

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    area_id = fields.Many2one(
        comodel_name='contact.area',
        string='Área',
    )
    hierarchy_level_id = fields.Many2one(
        comodel_name='contact.hierarchy.level',
        string='Nivel Jerárquico',
    )
    status_id = fields.Many2one(
        comodel_name='contact.status',
        string='Estatus',
    )

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    peso_cupo = fields.Integer(
        string='Peso del cupo',
        help='Cupos que representa cada unidad vendida. Si es 0 se usa 2 para '
             '"CUPO/DIA COMPLETO" y 1 para el resto.',
    )

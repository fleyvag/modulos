# -*- coding: utf-8 -*-
# NOTA: este archivo se llamaba "product_product.py" en el original, pero
# la clase en realidad hereda 'product.template' (no 'product.product').
# Se renombró a product_template.py para que el nombre del archivo
# coincida con el modelo, como es la convención de Odoo.
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    peso_cupo = fields.Integer(string='Peso del cupo')

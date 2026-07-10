from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    razon_social = fields.Char(string='Razón Social')
    nombre_comercial = fields.Char(string='Nombre Comercial')

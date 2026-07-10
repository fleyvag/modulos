from odoo import fields, models


class ContactArea(models.Model):
    _name = 'contact.area'
    _description = 'Contact Area'
    _order = 'name'

    name = fields.Char(
        string='Nombre',
        required=True,
        index=True,
    )
    active = fields.Boolean(
        string='Activo',
        default=True,
    )

from odoo import fields, models


class ContactStatus(models.Model):
    _name = 'contact.status'
    _description = 'Contact Status'
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

from odoo import fields, models


class ContactHierarchyLevel(models.Model):
    _name = 'contact.hierarchy.level'
    _description = 'Contact Hierarchy Level'
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

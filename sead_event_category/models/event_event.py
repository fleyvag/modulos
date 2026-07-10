from odoo import models, fields


class EventEvent(models.Model):
    _inherit = 'event.event'

    category_id = fields.Many2one('event.category', string='Categoría')

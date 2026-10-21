from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('product_id')
    def _compute_event_id(self):
        # event_sale borra el evento en productos que no son de tipo evento;
        # se conserva para que el evento traído desde el CRM no se pierda.
        kept_events = {
            line: line.event_id
            for line in self
            if line.event_id and line.product_id.detailed_type != 'event'
        }
        super()._compute_event_id()
        for line, event in kept_events.items():
            line.event_id = event

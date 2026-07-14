from odoo import fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    event_id = fields.Many2one('event.event', string='Evento')
    custom_order_line_ids = fields.One2many(
        'crm.lead.line', 'lead_id', string='Líneas de Pedido'
    )

    def action_new_quotation(self):
        if not self.custom_order_line_ids:
            return super().action_new_quotation()

        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'opportunity_id': self.id,
            'company_id': self.company_id.id or self.env.company.id,
            'currency_id': self.company_id.currency_id.id or self.env.company.currency_id.id,
            'campaign_id': self.campaign_id.id,
            'medium_id': self.medium_id.id,
            'source_id': self.source_id.id,
            'tag_ids': [(6, 0, self.tag_ids.ids)],
            'user_id': self.user_id.id or self.env.user.id,
            'team_id': self.team_id.id,
            'origin': self.name,
        })

        for line in self.custom_order_line_ids:
            self.env['sale.order.line'].create({
                'order_id': sale_order.id,
                'product_id': line.product_id.id,
                'name': line.name or line.product_id.display_name,
                'product_uom_qty': line.quantity,
                'product_uom': line.product_id.uom_id.id,
                'price_unit': line.price_unit,
                'tax_id': [(6, 0, line.tax_ids.ids)],
            })

        self.action_set_won()

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': sale_order.id,
            'view_mode': 'form',
            'view_id': self.env.ref('sale.view_order_form').id,
            'target': 'current',
        }

    def _create_quotation(self):
        sale_order = super()._create_quotation()
        if self.custom_order_line_ids:
            self._add_custom_lines_to_sale_order(sale_order)
        return sale_order

    def _add_custom_lines_to_sale_order(self, sale_order):
        sale_order.order_line.filtered(lambda l: not l.product_id).unlink()
        for line in self.custom_order_line_ids:
            self.env['sale.order.line'].create({
                'order_id': sale_order.id,
                'product_id': line.product_id.id,
                'name': line.name or line.product_id.display_name,
                'product_uom_qty': line.quantity,
                'product_uom': line.product_id.uom_id.id,
                'price_unit': line.price_unit,
                'tax_id': [(6, 0, line.tax_ids.ids)],
            })

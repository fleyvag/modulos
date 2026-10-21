from odoo import _, api, fields, models
from odoo.exceptions import UserError


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    event_id = fields.Many2one('event.event', string='Evento')
    custom_order_line_ids = fields.One2many(
        'crm.lead.line', 'lead_id', string='Líneas de Pedido'
    )
    lines_amount_untaxed = fields.Monetary(
        string='Base imponible', compute='_compute_lines_amounts', store=True,
        currency_field='company_currency',
    )
    lines_amount_tax = fields.Monetary(
        string='Impuesto', compute='_compute_lines_amounts', store=True,
        currency_field='company_currency',
    )
    lines_amount_total = fields.Monetary(
        string='Total', compute='_compute_lines_amounts', store=True,
        currency_field='company_currency',
    )
    planned_revenue_usd = fields.Float(string='Ingreso previsto (USD)')
    amount_of_quota = fields.Float(string='Cantidad de cupos')

    @api.depends('custom_order_line_ids.subtotal', 'custom_order_line_ids.tax_ids', 'partner_id')
    def _compute_lines_amounts(self):
        for lead in self:
            untaxed = sum(lead.custom_order_line_ids.mapped('subtotal'))
            tax = sum(line._get_tax_amount() for line in lead.custom_order_line_ids)
            lead.lines_amount_untaxed = untaxed
            lead.lines_amount_tax = tax
            lead.lines_amount_total = untaxed + tax

    @api.onchange('custom_order_line_ids', 'partner_id')
    def _onchange_custom_order_line_ids(self):
        # Solo recalcula si hay líneas, para no borrar un ingreso escrito a mano.
        if not self.custom_order_line_ids:
            return
        expected_revenue = planned_revenue_usd = amount_of_quota = 0.0
        currency = self.partner_id.property_product_pricelist.currency_id or self.company_currency
        for line in self.custom_order_line_ids:
            weight = line.product_id.peso_cupo or (
                2 if line.product_id.name == 'CUPO/DIA COMPLETO' else 1
            )
            amount_of_quota += weight * line.quantity
            total = line.subtotal + line._get_tax_amount()
            if currency.name == 'PEN':
                expected_revenue += total
            else:
                planned_revenue_usd += total
        self.expected_revenue = expected_revenue
        self.planned_revenue_usd = planned_revenue_usd
        self.amount_of_quota = amount_of_quota

    def action_new_quotation(self):
        self.ensure_one()
        if not self.custom_order_line_ids:
            return super().action_new_quotation()

        if not self.partner_id:
            raise UserError(_('Debe asignar un cliente a la oportunidad antes de crear la cotización.'))

        sale_order = self.env['sale.order'].create(self._prepare_custom_sale_order_values())

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': sale_order.id,
            'view_mode': 'form',
            'views': [(self.env.ref('sale.view_order_form').id, 'form')],
            'target': 'current',
        }

    def _prepare_custom_sale_order_values(self):
        self.ensure_one()
        values = {
            'partner_id': self.partner_id.id,
            'opportunity_id': self.id,
            'company_id': self.company_id.id or self.env.company.id,
            'campaign_id': self.campaign_id.id,
            'medium_id': self.medium_id.id,
            'source_id': self.source_id.id,
            'tag_ids': [(6, 0, self.tag_ids.ids)],
            'user_id': self.user_id.id or self.env.user.id,
            'origin': self.name,
            'event_id': self.event_id.id,
            'order_line': [
                (0, 0, line._prepare_sale_order_line_values())
                for line in self.custom_order_line_ids
            ],
        }
        if self.team_id:
            values['team_id'] = self.team_id.id
        return values

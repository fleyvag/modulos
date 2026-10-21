# -*- coding: utf-8 -*-
from odoo import api, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # opportunity_id ya lo define sale_crm en v17 (con check_company y
    # dominio por compañía); redefinirlo aquí pisaba su etiqueta y dominio.

    def _prepare_sale_order_lines_from_opportunity(self, record):
        vals = {
            'product_id': record.product_id.id,
            'name': record.description or record.product_id.display_name,
            'product_uom_qty': record.qty,
            'price_unit': record.price_unit,
            'tax_id': [(6, 0, record.tax_id.ids)],
            'analytics_id': record.analytics_id.id,
        }
        if record.product_uom:
            vals['product_uom'] = record.product_uom.id
        if record.analytics_id:
            vals['analytic_distribution'] = {str(record.analytics_id.id): 100}
        return vals

    @api.onchange('opportunity_id')
    def opportunity_id_change(self):
        if not self.opportunity_id or not self.opportunity_id.crm_line:
            return
        if not self.partner_id:
            self.partner_id = self.opportunity_id.partner_id

        new_lines = self.env['sale.order.line']
        for line in self.opportunity_id.crm_line:
            data = self._prepare_sale_order_lines_from_opportunity(line)
            new_lines += new_lines.new(data)

        self.order_line += new_lines

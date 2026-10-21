# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CrmLeadLine(models.Model):
    _name = 'crm.lead.line'
    _description = 'Lineas de pedido crm'

    lead_id = fields.Many2one(
        'crm.lead',
        string='Lead Reference',
        required=True,
        ondelete='cascade',
        index=True,
        readonly=True,
    )
    product_id = fields.Many2one('product.product', string='Producto')
    description = fields.Char(string='Descripcion')
    qty = fields.Integer('Cantidad', default=1)
    price_unit = fields.Float(string='Precio unitario')
    sub_total = fields.Float(
        string='Sub Total',
        compute='_compute_sub_total',
        store=True,
    )
    # product.uom fue renombrado a uom.uom en Odoo 13.
    product_uom = fields.Many2one('uom.uom', string='Unidad de medida')
    tax_id = fields.Many2many('account.tax', string='IGV')
    # account.analytic.plan.instance ya no existe (modelo eliminado hace
    # muchas versiones, era de la época account_analytic_plans en OpenERP
    # 7/8). Se reemplaza por account.analytic.account, en línea con cómo
    # se maneja la cuenta analítica en el resto de módulos ya migrados.
    analytics_id = fields.Many2one(
        'account.analytic.account',
        string='Distribución analítica',
    )
    name_analytics = fields.Char(string='Nombre de la Distribucion analitica')
    name_product = fields.Char(string='Nombre del producto')

    @api.depends('qty', 'price_unit')
    def _compute_sub_total(self):
        for line in self:
            line.sub_total = line.qty * line.price_unit

    def _get_tax_amount(self):
        """Impuesto de la línea. En v17 account.tax.amount es un porcentaje
        (18.0), no una fracción (0.18) como en v8, por eso se usa
        compute_all en lugar de multiplicar directamente."""
        self.ensure_one()
        if not self.tax_id:
            return 0.0
        taxes = self.tax_id.compute_all(
            self.price_unit,
            quantity=self.qty,
            product=self.product_id,
            partner=self.lead_id.partner_id,
        )
        return taxes['total_included'] - taxes['total_excluded']

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.description = self.product_id.name
            self.price_unit = self.product_id.lst_price
            self.product_uom = self.product_id.uom_id
            self.name_product = self.product_id.product_tmpl_id.name
            self.tax_id = [(6, 0, self.product_id.taxes_id.ids)]

    @api.onchange('analytics_id')
    def _onchange_analytics_id(self):
        if self.analytics_id:
            self.name_analytics = self.analytics_id.name

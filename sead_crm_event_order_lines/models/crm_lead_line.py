from odoo import api, fields, models


class CrmLeadLine(models.Model):
    _name = 'crm.lead.line'
    _description = 'Línea de Pedido de CRM'
    _order = 'sequence, id'

    sequence = fields.Integer(default=10)
    lead_id = fields.Many2one('crm.lead', string='Oportunidad', ondelete='cascade', index=True)
    company_id = fields.Many2one(related='lead_id.company_id', string='Compañía')
    event_id = fields.Many2one('event.event', string='Evento')
    product_id = fields.Many2one(
        'product.product', string='Producto', required=True,
        domain="[('sale_ok', '=', True)]",
    )
    name = fields.Text(string='Descripción')
    quantity = fields.Float(string='Cantidad', default=1.0, required=True)
    price_unit = fields.Float(string='Precio Unitario', required=True)
    tax_ids = fields.Many2many(
        'account.tax', string='Impuestos',
        domain="[('type_tax_use', '=', 'sale')]",
    )
    analytic_account_id = fields.Many2one(
        'account.analytic.account', string='Cuenta analítica',
    )
    currency_id = fields.Many2one('res.currency', string='Moneda', compute='_compute_currency_id')
    subtotal = fields.Monetary(
        string='Subtotal',
        compute='_compute_subtotal',
        currency_field='currency_id',
        store=True,
    )

    @api.depends('lead_id.company_id')
    def _compute_currency_id(self):
        for line in self:
            line.currency_id = line.lead_id.company_id.currency_id or self.env.company.currency_id

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit

    def _get_tax_amount(self):
        self.ensure_one()
        if not self.tax_ids:
            return 0.0
        taxes = self.tax_ids.compute_all(
            self.price_unit,
            currency=self.currency_id,
            quantity=self.quantity,
            product=self.product_id,
            partner=self.lead_id.partner_id,
        )
        return taxes['total_included'] - taxes['total_excluded']

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if not self.product_id:
            return
        company = self.lead_id.company_id or self.env.company
        self.name = self.product_id.get_product_multiline_description_sale()
        self.price_unit = self.product_id.lst_price
        self.tax_ids = self.product_id.taxes_id.filtered(lambda t: t.company_id == company)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'event_id' not in vals and vals.get('lead_id'):
                vals['event_id'] = self.env['crm.lead'].browse(vals['lead_id']).event_id.id
        return super().create(vals_list)

    def _prepare_sale_order_line_values(self):
        self.ensure_one()
        values = {
            'sequence': self.sequence,
            'product_id': self.product_id.id,
            'name': self.name or self.product_id.get_product_multiline_description_sale(),
            'product_uom_qty': self.quantity,
            'product_uom': self.product_id.uom_id.id,
            'price_unit': self.price_unit,
            'tax_id': [(6, 0, self.tax_ids.ids)],
            'event_id': self.event_id.id,
        }
        if self.analytic_account_id:
            values['analytic_distribution'] = {str(self.analytic_account_id.id): 100}
        return values

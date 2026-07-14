from odoo import api, fields, models


class CrmLeadLine(models.Model):
    _name = 'crm.lead.line'
    _description = 'Línea de Pedido de CRM'
    _order = 'sequence, id'

    sequence = fields.Integer(default=10)
    lead_id = fields.Many2one('crm.lead', string='Oportunidad', ondelete='cascade', index=True)
    product_id = fields.Many2one('product.product', string='Producto', required=True)
    name = fields.Text(string='Descripción')
    quantity = fields.Float(string='Cantidad', default=1.0, required=True)
    price_unit = fields.Float(string='Precio Unitario', required=True)
    tax_ids = fields.Many2many('account.tax', string='Impuestos')
    currency_id = fields.Many2one(related='lead_id.company_id.currency_id', string='Moneda')
    subtotal = fields.Monetary(
        string='Subtotal',
        compute='_compute_subtotal',
        currency_field='currency_id',
        store=True,
    )

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit

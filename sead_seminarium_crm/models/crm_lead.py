# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    crm_line = fields.One2many(
        'crm.lead.line',
        'lead_id',
        string='Lineas de pedido',
    )
    amount_untaxed = fields.Monetary(
        string='Base imponible',
        compute='_compute_amounts',
        store=True,
        currency_field='currency_active',
    )
    amount_tax = fields.Monetary(
        string='Impuesto',
        compute='_compute_amounts',
        store=True,
        currency_field='currency_active',
    )
    amount_total = fields.Monetary(
        string='Total',
        compute='_compute_amounts',
        store=True,
        currency_field='currency_active',
    )
    # El widget monetary necesita un Many2one a res.currency (antes era Char
    # y se le asignaba un id, lo que rompía el formato de moneda).
    currency_active = fields.Many2one(
        'res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id,
    )

    # --- NOTA DE MIGRACIÓN ---
    # El onchange original (_onchange_crm_line) ya usaba estos dos campos
    # (self.planned_revenue_usd y self.amount_of_quota) pero NUNCA estaban
    # declarados en el módulo que me pasaste, ni existen en crm.lead
    # estándar de Odoo. Sin ellos, ese onchange se habría caído con
    # AttributeError al primer uso. Los agregué aquí como campos Float
    # simples para que el módulo sea funcional. Si en tu instalación
    # original estos campos vivían en OTRO módulo (con lógica propia,
    # traducciones, formato, etc.), avísame y los quito de aquí para que
    # no choquen con esa definición.
    planned_revenue_usd = fields.Float(string='Ingreso previsto (USD)')
    amount_of_quota = fields.Float(string='Cantidad de cupos')

    @api.depends('crm_line.sub_total', 'crm_line.tax_id', 'partner_id')
    def _compute_amounts(self):
        for record in self:
            untaxed = sum(record.crm_line.mapped('sub_total'))
            tax = sum(line._get_tax_amount() for line in record.crm_line)
            record.amount_untaxed = untaxed
            record.amount_tax = tax
            record.amount_total = untaxed + tax

    @api.onchange('crm_line', 'partner_id')
    def _onchange_crm_line(self):
        # planned_revenue se renombró a expected_revenue en Odoo 14.
        self.expected_revenue = 0
        self.planned_revenue_usd = 0
        self.amount_of_quota = 0
        if self.partner_id:
            price_list = self.partner_id.property_product_pricelist
            self.currency_active = price_list.currency_id
            for line in self.crm_line:
                planned_revenue = line.sub_total + line._get_tax_amount()
                mult = line.product_id.peso_cupo or (
                    2 if line.product_id.name == "CUPO/DIA COMPLETO" else 1
                )
                self.amount_of_quota += (mult * line.qty)
                if price_list.currency_id.name == 'PEN':
                    self.expected_revenue += planned_revenue
                else:
                    self.planned_revenue_usd += planned_revenue

    def action_create_quotation(self):
        self.ensure_one()
        if not self.partner_id:
            raise UserError(_('Debe indicar un cliente antes de crear la cotización.'))
        if not self.crm_line:
            raise UserError(_('La oportunidad no tiene líneas de pedido.'))

        # --- NOTA DE MIGRACIÓN ---
        # El original enviaba 'lead_id' y 'project_id' (cuenta analítica) a
        # sale.order; ninguno existe en v17. La cuenta analítica de cada
        # línea se pasa ahora a analytic_distribution de sale.order.line.
        order_lines = []
        for line in self.crm_line:
            vals = {
                'product_id': line.product_id.id,
                'name': line.description or line.product_id.display_name,
                'product_uom_qty': line.qty,
                'price_unit': line.price_unit,
                'tax_id': [(6, 0, line.tax_id.ids)],
                'analytics_id': line.analytics_id.id,
            }
            if line.product_uom:
                vals['product_uom'] = line.product_uom.id
            if line.analytics_id:
                vals['analytic_distribution'] = {str(line.analytics_id.id): 100}
            order_lines.append((0, 0, vals))

        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'campaign_id': self.campaign_id.id,
            'medium_id': self.medium_id.id,
            'source_id': self.source_id.id,
            'opportunity_id': self.id,
            'origin': self.name,
            'user_id': self.user_id.id,
            'team_id': self.team_id.id,
            'order_line': order_lines,
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': sale_order.id,
            'view_mode': 'form',
            'target': 'current',
        }

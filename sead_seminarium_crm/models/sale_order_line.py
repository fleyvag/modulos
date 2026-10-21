# -*- coding: utf-8 -*-
from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # --- NOTA DE MIGRACIÓN ---
    # sale_order.py (_prepare_sale_order_lines_from_opportunity) y
    # crm_lead.py (action_create_quotation) escriben el valor
    # 'analytics_id' en sale.order.line, pero ese campo NUNCA estaba
    # declarado en el módulo original que me pasaste. Sin esta
    # declaración, crear la cotización desde una oportunidad se habría
    # caído con un error de campo inexistente. Lo agregué aquí, apuntando
    # a account.analytic.account por consistencia con crm.lead.line.
    # Si este campo ya existe en otro módulo tuyo (con otro nombre u
    # otro modelo destino), avísame para no duplicarlo.
    analytics_id = fields.Many2one(
        'account.analytic.account',
        string='Distribución analítica',
    )

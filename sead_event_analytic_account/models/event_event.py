from odoo import models, fields


class EventEvent(models.Model):
    _inherit = 'event.event'

    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Cuenta Analítica',
        required=True,
        domain="[('company_id', '=', company_id)]",
        help="Cuenta analítica asociada al evento"
    )

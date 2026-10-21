# -*- coding: utf-8 -*-
{
    'name': "CRM - Seminarium",
    'summary': "Extiende la funcionalidad del CRM de Odoo",
    'description': """
Adaptación del CRM de Odoo: agrega líneas de producto a la oportunidad
(crm.lead) y permite convertirlas en una cotización (sale.order).

Migrado desde OpenERP/Odoo 8-9 a la versión 17.
    """,
    'author': "SEAD S.A.C",
    'website': "http://www.sead.pe",
    'license': 'AGPL-3',
    'category': 'Sales/CRM',
    'version': '17.0.1.0.0',
    'depends': [
        'base',
        'crm',
        'sale',
        'sale_crm',
        'product',
        'analytic',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

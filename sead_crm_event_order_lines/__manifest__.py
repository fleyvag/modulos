{
    'name': 'CRM - Eventos y Líneas de Pedido',
    'version': '17.0.1.0.0',
    'category': 'Sales/CRM',
    'summary': 'Agrega campo de evento y líneas de pedido personalizadas en CRM',
    'description': """
Módulo que extiende CRM de Odoo 17 para agregar:
- Campo de evento (vinculado a event.event) en oportunidades
- Pestaña "Línea de pedido" con productos, precios, impuestos y cantidades
- Transferencia automática de líneas a la cotización al crear una
    """,
    'depends': [
        'crm',
        'sale',
        'event',
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}

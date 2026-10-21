{
    'name': 'CRM - Eventos y Líneas de Pedido',
    'version': '17.0.1.2.0',
    'category': 'Sales/CRM',
    'summary': 'Agrega campo de evento y líneas de pedido personalizadas en CRM',
    'description': """
Módulo que extiende CRM de Odoo 17 para agregar:
- Campo de evento (vinculado a event.event) en oportunidades
- Pestaña "Línea de pedido" con productos, precios, impuestos y cantidades
- Campo de evento en cada línea (por defecto el evento de la oportunidad)
- Transferencia automática de líneas y evento a la cotización al crear una
- Cuenta analítica por línea (se pasa a la distribución analítica de la cotización)
- Totales con impuestos, ingreso previsto PEN/USD y cantidad de cupos
- Campo "Peso del cupo" en el producto
    """,
    'depends': [
        'crm',
        'sale_crm',
        'event_sale',
        'product',
        'analytic',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}

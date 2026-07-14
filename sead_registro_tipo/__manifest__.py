{
    'name': 'Tipo de Registro para Asistentes',
    'version': '17.0.1.0.0',
    'category': 'Marketing/Events',
    'summary': 'Agrega tipo de registro a los asistentes de eventos',
    'description': """
        Módulo que permite agregar un campo de tipo de registro
        a los asistentes de eventos en Odoo.
    """,
    'depends': ['event'],
    'data': [
        'security/ir.model.access.csv',
        'views/event_registration_type_views.xml',
        'views/event_registration_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}

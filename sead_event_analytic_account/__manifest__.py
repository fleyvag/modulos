{
    'name': 'Cuenta Analítica en Eventos',
    'version': '1.0',
    'category': 'Marketing/Eventos',
    'summary': 'Agrega cuenta analítica obligatoria a los eventos',
    'description': '''
        Módulo que agrega un campo obligatorio de cuenta analítica
        a los eventos para asociar cuentas analíticas.
    ''',
    'depends': ['event', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/event_event_views.xml',
        'views/analytic_account_views.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}

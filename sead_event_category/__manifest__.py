{
    'name': 'Categorías de Eventos',
    'version': '1.0',
    'category': 'Marketing/Eventos',
    'summary': 'Agrega categorías a los eventos',
    'description': '''
        Módulo que agrega el modelo de categorías para eventos.
        Permite clasificar eventos por categorías configurables desde el menú de Configuración.
    ''',
    'depends': ['event'],
    'data': [
        'security/ir.model.access.csv',
        'views/event_category_views.xml',
        'views/event_event_views.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}

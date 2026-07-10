{
    'name': 'Contacto - Actividades Padre y Económica',
    'version': '17.0.1.0.0',
    'category': 'Contacts',
    'summary': 'Agrega modelos Actividad Padre y Actividad Económica en Contactos > Configuración',
    'depends': ['contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/actividad_padre_views.xml',
        'views/actividad_economica_views.xml',
        'views/res_partner_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}

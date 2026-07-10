{
    'name': 'Razón Social y Nombre Comercial',
    'version': '17.0.1.0.0',
    'category': 'Contacts',
    'summary': 'Agrega campos de Razón Social y Nombre Comercial al contacto',
    'description': """
        Este módulo agrega dos campos al formulario de contacto:
        - Razón Social
        - Nombre Comercial
        Se muestran debajo del campo NIF.
    """,
    'author': 'Custom',
    'depends': ['base'],
    'data': [
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}

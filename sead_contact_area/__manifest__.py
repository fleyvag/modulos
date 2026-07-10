{
    'name': 'Contact Areas',
    'version': '17.0.1.0.0',
    'category': 'Contacts',
    'summary': 'Agrega campos de Área y Nivel Jerárquico a los contactos',
    'description': """
        Este módulo agrega los campos Área y Nivel Jerárquico a los contactos (res.partner).
        Permite seleccionar un área y un nivel jerárquico desde listas predefinidas
        configuradas en Contactos > Configuración.
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': [
        'contacts',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/contact_area_views.xml',
        'views/contact_hierarchy_level_views.xml',
        'views/contact_status_views.xml',
        'views/res_partner_views.xml',
        'views/contact_area_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}

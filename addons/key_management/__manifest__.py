# -*- coding: utf-8 -*-


{
    'name': 'Key Management',
    'version': '19.0.1.0.0',
    'author': 'Christoph Osswald',
    'category': 'DVZO/Key management',
    'depends': [
        'base',
    ],
    'installable': True,
    'application': False,
    'license': "LGPL-3",
    'data': [
        'security/key_management_security.xml',
        'security/ir.model.access.csv',
        'views/key_lending_views.xml',
        'views/key_permission_views.xml',
        'views/key_group_views.xml',
        'views/key_system_views.xml',
        'views/key_views.xml',
        'views/key_management_menu_views.xml'
    ],
}

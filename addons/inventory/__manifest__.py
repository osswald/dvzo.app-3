# -*- coding: utf-8 -*-


{
    'name': 'Inventory',
    'author': 'Christoph Osswald',
    'category': 'DVZO/Inventory',
    'depends': [
        'base',
        'mail',
    ],
    'installable': True,
    'application': False,
    'license': "LGPL-3",
    'data': [
        'security/inventory_security.xml',
        'security/ir.model.access.csv',

        'views/inventory_views.xml',
        'views/inventory_type_views.xml',
        'views/inventory_manufacturer_views.xml',
        'views/inventory_location_views.xml',
        'views/inventory_place_views.xml',
        'views/inventory_status_views.xml',
        'views/inventory_check_views.xml',

        'views/inventory_menu_views.xml',

        'wizards/add_inventory_check_wizard.xml',

        'data/inventory_scheduled_actions.xml',
    ],
}

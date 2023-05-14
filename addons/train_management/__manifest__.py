# -*- coding: utf-8 -*-


{
    'name': 'Train Management',
    'depends': [
        'base',
    ],
    'author': 'Christoph Osswald',
    'installable': True,
    'application': False,
    'license': "LGPL-3",
    'data': [
        'security/ir.model.access.csv',
        'data/train_management.station.csv',
        'data/train_management.stop_code.csv',
        'data/train_management.railway_company.csv',
        'views/circuit_views.xml',
        'views/day_planning_views.xml',
        'views/day_planning_text_views.xml',
        'views/day_planning_shift_views.xml',
        'views/railway_company_views.xml',
        'views/station_views.xml',
        'views/vehicle_views.xml',
        'views/train_views.xml',
        'views/stop_code_views.xml',
        'views/reservation_views.xml',
        'views/copy_recipient_views.xml',
        'views/shift_position_views.xml',
        'views/shift_position_type_views.xml',
        'views/shift_template_views.xml',
        'views/shift_menu_views.xml',
        'views/train_management_menu_views.xml',
    ],
}

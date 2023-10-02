# -*- coding: utf-8 -*-


{
    'name': 'Minimal hours',
    'author': 'Christoph Osswald',
    'category': 'DVZO/Minimal hours',
    'depends': [
        'base',
        'training',
        'train_management',
    ],
    'installable': True,
    'application': False,
    'license': "LGPL-3",
    'data': [
        'views/res_partner_views.xml',

        'report/minimal_hours.xml',
        'report/minimal_hours_report_views.xml'
    ],
}

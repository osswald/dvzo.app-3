# -*- coding: utf-8 -*-


{
    'name': 'Minimal hours',
    'version': '19.0.1.0.0',
    'author': 'Christoph Osswald',
    'category': 'DVZO/Minimal hours',
    'version': '19.0.1.0.0',
    'depends': [
        'base',
        'website',
        'training',
        'train_management',
    ],
    'installable': True,
    'application': False,
    'license': "LGPL-3",
    'data': [
        'views/web_minimal_hours_views.xml',

        'views/res_partner_views.xml',

        'report/minimal_hours.xml',
        'report/minimal_hours_report_views.xml'
    ],
}

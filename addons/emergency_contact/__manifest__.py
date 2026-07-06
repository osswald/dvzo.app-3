# -*- coding: utf-8 -*-


{
    'name': 'Emergency contact',
    'version': '19.0.1.0.0',
    'author': 'Christoph Osswald',
    'category': 'DVZO/Emergency contact',
    'depends': [
        'base',
    ],
    'installable': True,
    'application': False,
    'license': "LGPL-3",
    'data': [
        'security/emergency_contact_security.xml',
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
    ],
}

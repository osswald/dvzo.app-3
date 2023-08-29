# -*- coding: utf-8 -*-
{
    'name': 'membership',
    'author': 'Christoph Osswald',
    'category': 'DVZO/Membership',
    'depends': [
        'base',
    ],
    'installable': True,
    'application': False,
    'license': "LGPL-3",
    'data': [
        'views/res_partner_views.xml',
        'views/department_views.xml',
        'security/ir.model.access.csv',
    ],
}

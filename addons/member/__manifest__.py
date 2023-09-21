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
        'views/membership_views.xml',
        'views/department_views.xml',
        'views/member_menu_views.xml',
        'security/membership_security.xml',
        'security/ir.model.access.csv',
    ],
}

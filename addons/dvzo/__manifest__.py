# -*- coding: utf-8 -*-


{
    'name': 'DVZO.app',
    'author': "Christoph Osswald",
    'maintainer': 'Dampfbahn-Verein Zürcher Oberland',
    'depends': [
        'base',
        'project',
        'contacts',
        'partner_firstname',
        'emergency_contact',
        'key_management',
        'member',
        'train_management',
        'uniform',
        'web_window_title',
        'auth_oidc',
    ],
    'data': [
        'report/layouts.xml',
    ],
    'installable': True,
    'application': True,
    'license': "LGPL-3"
}

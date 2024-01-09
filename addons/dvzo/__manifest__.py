# -*- coding: utf-8 -*-


{
    'name': 'DVZO.app',
    'author': "Christoph Osswald",
    'maintainer': 'Dampfbahn-Verein Zürcher Oberland',
    'category': 'DVZO',
    'depends': [
        'base',
        'website',
        'project',
        'contacts',
        'partner_firstname',
        'emergency_contact',
        'key_management',
        'member',
        'training',
        'train_management',
        'minimal_hours',
        'risk_management',
        'inventory',
        'uniform',
        'web_window_title',
        'auth_oidc',
        'account_statement_import_camt54',
    ],
    'data': [
        'report/layouts.xml',
    ],
    'installable': True,
    'application': True,
    'license': "LGPL-3"
}

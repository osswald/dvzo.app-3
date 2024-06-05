# -*- coding: utf-8 -*-


{
    'name': 'Risk management',
    'author': 'Christoph Osswald',
    'category': 'DVZO/Risk management',
    'depends': [
        'base',
        'inventory',
        'emergency_contact'
    ],
    'installable': True,
    'application': False,
    'license': "LGPL-3",
    'data': [
        'security/risk_management_security.xml',
        'security/ir.model.access.csv',

        'views/asset_type_views.xml',
        'views/asset_views.xml',
        'views/business_risk_type_views.xml',
        'views/business_risk_views.xml',
        'views/certification_views.xml',
        'views/damage_views.xml',
        'views/department_views.xml',
        'views/extent_of_damage_views.xml',
        'views/probability_views.xml',
        'views/res_partner_views.xml',
        'views/residual_risk_views.xml',
        'views/risk_assessment_views.xml',
        'views/risk_assessment_check_views.xml',
        'views/risk_zone_views.xml',
        'views/inventory_views.xml',

        'views/risk_management_menu_views.xml',

        'wizards/add_risk_assessment_check_wizard.xml',
    ],
}

# -*- coding: utf-8 -*-


{
    'name': 'Train Management',
    'depends': [
        'base',
        'training',
    ],
    'author': 'Christoph Osswald',
    'category': 'DVZO/Train management',
    'installable': True,
    'application': False,
    'license': "LGPL-3",
    'data': [
        'security/train_management_security.xml',
        'security/ir.model.access.csv',

        'data/train_management.station.csv',
        'data/train_management.stop_code.csv',
        'data/train_management.railway_company.csv',
        'data/update_vehicles_batch.xml',
        'data/update_vehicle_defect_batch.xml',

        'report/train_management_briefing_report.xml',
        'report/train_management_bulletin_report.xml',
        'report/train_management_day_planning_shift_report.xml',
        'report/train_management_shift_report.xml',
        'report/train_management_report_views.xml',

        'wizards/create_train_wizard.xml',
        'wizards/add_shifts_wizard.xml',
        'wizards/add_shift_positions_wizard.xml',
        'wizards/show_briefing_recipients_wizard.xml',

        'views/circuit_views.xml',
        'views/day_planning_shift_views.xml',
        'views/train_views.xml',
        'views/day_planning_views.xml',
        'views/day_planning_text_views.xml',
        'views/day_planning_shift_offer_views.xml',
        'views/railway_company_views.xml',
        'views/station_views.xml',
        'views/vehicle_defect_views.xml',
        'views/vehicle_views.xml',
        'views/train_template_views.xml',
        'views/stop_code_views.xml',
        'views/reservation_views.xml',
        'views/copy_recipient_views.xml',
        'views/shift_position_views.xml',
        'views/shift_position_type_views.xml',
        'views/shift_template_views.xml',
        'views/shift_template_group_views.xml',
        'views/res_partner_views.xml',

        'views/web_day_planning_views.xml',
        'views/web_current_shifts_views.xml',
        'views/web_shifts_views.xml',
        'views/web_shifts_needed_views.xml',
        'views/web_single_day_planning_detail_views.xml',

        'views/shift_menu_views.xml',
        'views/train_management_menu_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'train_management/static/src/js/shift_offer.js',
        ],
    },
}

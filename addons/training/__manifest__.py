# -*- coding: utf-8 -*-


{
    'name': 'Training',
    'author': 'Christoph Osswald',
    'category': 'DVZO/Training',
    'depends': [
        'base',
        'mail',
    ],
    'installable': True,
    'application': False,
    'license': "LGPL-3",
    'data': [
        'security/training_security.xml',
        'security/ir.model.access.csv',

        'data/activity_type_data.xml',
        'data/competence_validation.xml',

        'report/training_participant_list_report.xml',
        'report/training_invitation_report.xml',
        'report/training_competence_matrix.xml',
        'report/training_hours_current_year.xml',
        'report/training_report_views.xml',

        'views/training_views.xml',
        'views/training_module_views.xml',
        'views/training_date_views.xml',
        'views/training_participants_views.xml',
        'views/training_medical_fitness_level_views.xml',
        'views/training_exam_views.xml',
        'views/training_qualification_category_views.xml',
        'views/training_qualification_type_views.xml',
        'views/training_medical_assessment_views.xml',
        'views/training_menu_views.xml',
        'views/res_partner_views.xml',
        'views/res_partner_category_views.xml',
    ],
}

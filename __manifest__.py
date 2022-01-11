# -*- coding: utf-8 -*-
{
    'name': "University_managment",
    'sequence': '-100',
    'description': """
        gestion de l'université (etudiants, enseignants, matières ... etc)
    """,
    'author': "Achraf",

    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'mail', 'website'],
    'sequence': '-100',
    'data':
        [
            'security/security.xml',
            'security/ir.model.access.csv',
            'data/sequences.xml',
            # 'data/cron.xml',
            'report/report_student.xml',
            'report/template_student.xml',
            'data/mail_template.xml',
            #    'wizards/teacher_grade.xml',
            #   'report/report_teacher.xml',
            #   'report/template_teacher.xml',

            #   'report/report_department.xml',
            #   'report/template_department.xml',
            'views/website.xml',
            'views/university_view.xml',
            'views/seance_view.xml',
            'views/emploi_view.xml',
            'views/teacher_view.xml',
            'views/student_view.xml',
            'views/class_view.xml',
            'views/subject_view.xml',

        ],

    'demo': [

    ],
    'installable': True,
    'application': True
}

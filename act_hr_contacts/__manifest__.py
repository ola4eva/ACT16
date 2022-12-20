# -*- coding: utf-8 -*-
{
    'name': "HR Extension",

    'summary': """
        Extend HR implementation""",

    'description': """
        Extend HR implementation. Add features like:
        - Employee Guarantor implementation
        - Health Management information
    """,

    'author': "Olalekan Babawale",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': [
        'base',
        'contacts',
        'hr',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/guarantor_views.xml',
        'views/hr_employee_views.xml',
        'views/res_partner_views.xml',
    ],
}

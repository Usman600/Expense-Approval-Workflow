{
    "name": "Expense Approval Workflow",
    "author": "Muhammad Usman Hussain",
    "License": "LGPL-3",
    "version": "1.0",
    "summary": 'Manage all proects',
    'description': """
This module offers the basic functionalities to manage projects.
    """,
    "depends": ["base", "hr_expense", "mail" ],

    'data': [
        'security/ir.model.access.csv',
        'views/expense_view.xml',
        'data/email_templates.xml',
    ]
}

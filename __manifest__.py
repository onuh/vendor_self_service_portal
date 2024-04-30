# -*- coding: utf-8 -*-
{
    'name': "Vendor Self-Service Portal",

    'summary': """
        Vendor view forcast and Order Adjustment Request""",

    'description': """
        Forcast and Order Adjustment
    """,

    'author': "Onuh Victor",
    'website': "https://github.com/onuh",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '16.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'product', 'portal'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/mail_template.xml',
        'report/vendor_forcast_report.xml',
        'views/report_template.xml',
    ],

    'assets': {

        'web.assets_backend': [
            'vendor_self_service_portal/static/src/css/custom.css',
        ],

        'web.assets_frontend': [
            'vendor_self_service_portal/static/src/css/style.css',
            'vendor_self_service_portal/static/src/css/alertify.min.css',
            'vendor_self_service_portal/static/src/css/selectize.bootstrap3.min.css',
            'vendor_self_service_portal/static/src/css/waitMe.min.css',
            'vendor_self_service_portal/static/src/js/alertify.min.js',
            'vendor_self_service_portal/static/src/js/waitMe.min.js',
            'vendor_self_service_portal/static/src/js/selectize.min.js',
            'vendor_self_service_portal/static/src/js/jquery.steps.js',
            'vendor_self_service_portal/static/src/js/main.js',
        ],
    },

    # only loaded in demonstration mode
    'demo': [],
    'installable': True,
    'application': True,
}

# -*- coding: utf-8 -*-
{
    "name": "Central Bank Of Egypt (CBE) Currency Updater",
    "summary": """
        Update Currency based on CBE (Central Bank Of Egypt) Official Exchange rates and prices
        """,
    "description": """
         Using Odoo IAP to update currencies.
         """,
    "author": "GRANDTK",
    "website": "http://www.grandtk.com",
    "license": "LGPL-3",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Localization",
    "version": "14.0.0.1.0",
    'images': ['static/description/currency_rates_banner.jpeg'],
    # any module necessary for this one to work correctly
    "depends": ["base", "iap"],

    # always loaded
    "data": [
        'views/res_config_settings_views.xml',
        "data/cron.xml",
    ],
}

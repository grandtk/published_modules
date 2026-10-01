{
    "name": "Central Bank Of Egypt (CBE) Currency Updater",
    "summary": "Update currency rates from the official CBE exchange rates",
    "description": "Uses Odoo IAP to fetch the official CBE exchange rates and create daily currency rates.",
    "author": "GRANDTK",
    "website": "http://www.grandtk.com",
    "category": "Accounting/Localizations",
    "version": "18.0.1.0.0",
    "license": "LGPL-3",
    "depends": ["base", "base_setup", "iap"],
    "data": [
        "views/res_config_settings_views.xml",
        "data/cron.xml",
    ],
    "installable": True,
    "application": False,
}

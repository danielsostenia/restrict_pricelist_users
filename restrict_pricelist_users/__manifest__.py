# -*- coding: utf-8 -*-
{
    'name': 'Restrict Pricelist Users',
    'description': "This module restricts user access to specific pricelists in Odoo, "
                   "ensuring that only authorized users can view or manage pricelist data.",
    'version': '20.0.1.0.0',
    'author': 'Banica Daniel',
    'maintainers': ["banica-dev"],
    'license': 'OPL-1',
    'price': 10,
    'currency': "EUR",
    'installable': True,
    'data': [
        'security/pricelist_rules.xml',
        'views/product_pricelist_views.xml',
    ],
    'images': [
        'static/description/banner.png',
        'static/description/pricelist_allowed_users.png',
        'static/description/user_groups.png',
    ],
    'category': 'Sale',
    'depends': ['base', 'sale'],
    'live_test_url': 'https://www.youtube.com/watch?v=2kjrHfIb4Dc',
}

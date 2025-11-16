# -*- coding: utf-8 -*-
{
    'name': 'instant-ERP POS Branding',
    'version': '17.0.1.0.0',
    'category': 'Sales/Point of Sale',
    'sequence': 20,
    'summary': 'Rebrand Odoo POS to instant-ERP',
    'description': """
        instant-ERP POS Branding for Odoo 17.0
        =======================================

        Complete rebranding solution that replaces Odoo branding with instant-ERP:

        Features:
        ---------
        - Replace Odoo logo with instant-ERP logo in POS navbar
        - Remove all "Powered by Odoo" references from receipts
        - Add instant-ERP branding to receipt headers and footers
        - Custom instant-ERP color scheme and styling
        - Optional custom receipt header text per POS configuration
        - Uses inheritance only - no core file modifications
        - Fully compatible with Odoo upgrades

        Installation:
        ------------
        1. Place this module in custom-addons directory
        2. Update Apps List in Odoo
        3. Install "instant-ERP POS Branding" module
        4. Open POS to see instant-ERP branding

        Configuration:
        -------------
        - Optionally configure custom receipt text per POS in:
          Point of Sale > Configuration > Point of Sale > [Your POS] > instant-ERP Branding

        Technical:
        ---------
        - 100% inheritance-based customization
        - No modification of core Odoo files
        - Compatible with standard POS and POS extensions
        - Easy to maintain and upgrade
    """,
    'author': 'instant-ERP Development Team',
    'website': 'https://www.instant-erp.com',
    'license': 'LGPL-3',
    'depends': [
        'point_of_sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/pos_config_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            # XML Templates (must load before JS that uses them)
            'instant_erp_pos_branding/static/src/app/overrides/navbar.xml',
            'instant_erp_pos_branding/static/src/app/overrides/order_receipt.xml',
            'instant_erp_pos_branding/static/src/app/overrides/receipt_header.xml',

            # JavaScript
            'instant_erp_pos_branding/static/src/app/overrides/navbar.js',

            # Styles
            'instant_erp_pos_branding/static/src/scss/instant_erp_branding.scss',
        ],
    },
    'images': [
        'static/description/icon.png',
        'static/src/img/instant_erp_logo.svg',
        'static/src/img/instant_erp_receipt_logo.svg',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}

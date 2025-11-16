# -*- coding: utf-8 -*-
# Part of instant-ERP. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    enable_instant_erp_branding = fields.Boolean(
        string='Enable instant-ERP Branding',
        default=True,
        help='Enable instant-ERP custom branding in POS interface and receipts'
    )

    instant_erp_receipt_header = fields.Text(
        string='Custom Receipt Header',
        default='Welcome to instant-ERP\nThank you for your business!',
        help='Custom text to display at the top of receipts'
    )

    instant_erp_receipt_footer = fields.Text(
        string='Custom Receipt Footer',
        default='Visit us at www.instant-erp.com\nModern ERP. Simplified.',
        help='Custom text to display at the bottom of receipts'
    )

    def _get_pos_ui_data(self, params):
        """Add instant-ERP branding settings to POS UI data."""
        result = super()._get_pos_ui_data(params)
        result.update({
            'enable_instant_erp_branding': self.enable_instant_erp_branding,
            'instant_erp_receipt_header': self.instant_erp_receipt_header,
            'instant_erp_receipt_footer': self.instant_erp_receipt_footer,
        })
        return result

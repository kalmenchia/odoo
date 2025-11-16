# -*- coding: utf-8 -*-
# Part of instant-ERP. See LICENSE file for full copyright and licensing details.

from odoo import models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _export_for_ui(self, order):
        """Add instant-ERP branding data to order export."""
        result = super()._export_for_ui(order)

        # Add custom branding data if enabled
        if order.session_id.config_id.enable_instant_erp_branding:
            result.update({
                'instant_erp_header': order.session_id.config_id.instant_erp_receipt_header,
                'instant_erp_footer': order.session_id.config_id.instant_erp_receipt_footer,
            })

        return result

# -*- coding: utf-8 -*-
# Part of instant-ERP. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    instant_erp_pos_logo = fields.Binary(
        string='instant-ERP POS Logo',
        help='Custom logo to display in POS interface. If not set, default instant-ERP logo will be used.'
    )

    instant_erp_receipt_logo = fields.Binary(
        string='instant-ERP Receipt Logo',
        help='Custom logo to display on receipt printouts. If not set, default instant-ERP logo will be used.'
    )

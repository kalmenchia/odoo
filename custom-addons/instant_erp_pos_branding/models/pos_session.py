# -*- coding: utf-8 -*-

from odoo import models


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _get_pos_ui_res_users(self, params):
        """
        Override to add is_admin_user flag for instant-ERP branding debug access control.

        This extends the user data sent to the POS frontend to include whether the user
        has Administration/Settings access (base.group_system). This allows the frontend
        to restrict debug widget access to administrators only.
        """
        user = super()._get_pos_ui_res_users(params)

        # Check if current user has Administration / Settings access (base.group_system)
        is_admin = self.env.user.has_group('base.group_system')

        # Add the flag to user data
        user['is_admin_user'] = is_admin

        return user

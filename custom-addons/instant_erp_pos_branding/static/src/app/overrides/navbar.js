/** @odoo-module */

import { Navbar } from "@point_of_sale/app/navbar/navbar";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";

/**
 * Patch Navbar to provide custom logo URL for instant-ERP branding
 *
 * This patch provides the logo URL with proper fallback handling to ensure
 * the POS always has a logo to display, even if custom images are missing.
 */
patch(Navbar.prototype, {
    setup() {
        super.setup(...arguments);
        this.pos = usePos();
    },

    /**
     * Get instant-ERP logo URL with robust fallback logic
     *
     * Priority order:
     * 1. Company-specific instant-ERP POS logo (if configured)
     * 2. Default instant-ERP SVG logo from module
     * 3. Fallback to generic logo (if all else fails)
     *
     * @returns {string} URL to the logo image
     */
    get instantErpLogoUrl() {
        try {
            const company = this.pos?.company;

            // Priority 1: Company-specific instant-ERP logo
            if (company && company.instant_erp_pos_logo) {
                return `/web/image?model=res.company&id=${company.id}&field=instant_erp_pos_logo`;
            }

            // Priority 2: Default instant-ERP SVG logo (vector, scales better)
            return '/instant_erp_pos_branding/static/src/img/instant_erp_logo.svg';

        } catch (error) {
            // Fallback: If anything goes wrong, use the default SVG
            console.warn('instant-ERP: Error getting logo URL, using fallback', error);
            return '/instant_erp_pos_branding/static/src/img/instant_erp_logo.svg';
        }
    },

    /**
     * Get instant-ERP receipt logo URL with fallback
     *
     * This is exposed for use by other components if needed
     *
     * @returns {string} URL to the receipt logo image
     */
    get instantErpReceiptLogoUrl() {
        try {
            const company = this.pos?.company;

            if (company && company.instant_erp_receipt_logo) {
                return `/web/image?model=res.company&id=${company.id}&field=instant_erp_receipt_logo`;
            }

            return '/instant_erp_pos_branding/static/src/img/instant_erp_receipt_logo.svg';

        } catch (error) {
            console.warn('instant-ERP: Error getting receipt logo URL, using fallback', error);
            return '/instant_erp_pos_branding/static/src/img/instant_erp_receipt_logo.svg';
        }
    },
});

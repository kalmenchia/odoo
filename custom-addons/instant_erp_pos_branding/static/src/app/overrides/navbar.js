/** @odoo-module */

import { Navbar } from "@point_of_sale/app/navbar/navbar";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";

/**
 * Patch Navbar to provide custom logo URL for instant-ERP branding
 */
patch(Navbar.prototype, {
    setup() {
        super.setup(...arguments);
        this.pos = usePos();
    },

    /**
     * Get instant-ERP logo URL
     * Priority: Company custom logo > Default instant-ERP logo > Odoo logo
     */
    get instantErpLogoUrl() {
        const company = this.pos.company;

        // Use company-specific instant-ERP logo if available
        if (company.instant_erp_pos_logo) {
            return `/web/image?model=res.company&id=${company.id}&field=instant_erp_pos_logo`;
        }

        // Use default instant-ERP logo
        return '/instant_erp_pos_branding/static/src/img/instant_erp_logo.png';
    },
});

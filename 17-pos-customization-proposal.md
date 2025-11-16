# Odoo 17.0 Point of Sale Customization Guide

**Odoo Version:** 17.0
**Document Version:** 1.0
**Last Updated:** 2025-11-16

---

## Table of Contents

1. [Introduction](#introduction)
2. [Odoo 17.0 POS Architecture](#odoo-170-pos-architecture)
3. [Developer Guide for v17.0](#developer-guide-for-v170)
   - [Module Setup](#module-setup)
   - [Inheriting Python Models](#inheriting-python-models)
   - [Extending OWL Components](#extending-owl-components)
   - [Layout Customization](#layout-customization)
   - [Adding Custom Functions](#adding-custom-functions)
   - [Adding Custom Fields](#adding-custom-fields)
   - [Modifying Numpad/Keypad](#modifying-numpad-keypad)
   - [Payment Customization](#payment-customization)
   - [Receipt Customization](#receipt-customization)
4. [instant-ERP Debranding Proposal](#instant-erp-debranding-proposal)
5. [v17.0 Specific Best Practices](#v170-specific-best-practices)
6. [Troubleshooting v17.0](#troubleshooting-v170)

---

## Introduction

This guide provides **Odoo 17.0 specific** instructions for customizing the Point of Sale system. Odoo 17.0 uses the OWL (Odoo Web Library) framework with a refined component-based architecture.

### Prerequisites

Before using this guide, you should:
- Read [00-pos-customization-proposal.md](./00-pos-customization-proposal.md) for general concepts
- Have Odoo 17.0 installed and running
- Understand basic Python and JavaScript
- Be familiar with Odoo module development

### What's New in v17.0

- **Refined OWL Framework:** Latest version with performance improvements
- **Optimized Asset Loading:** Better bundle management
- **Enhanced Component System:** More intuitive inheritance patterns
- **Improved State Management:** Reactive stores with better APIs
- **Modern JavaScript:** Full ES6+ support with module imports

---

## Odoo 17.0 POS Architecture

### Directory Structure

```
addons/point_of_sale/
├── __manifest__.py
├── __init__.py
├── controllers/
│   └── main.py
├── models/
│   ├── __init__.py
│   ├── pos_config.py
│   ├── pos_session.py
│   ├── pos_order.py
│   ├── pos_payment.py
│   └── ...
├── static/src/
│   ├── app/                    # Main POS application
│   │   ├── main.js            # Entry point
│   │   ├── pos_app.js         # Root component
│   │   ├── navbar/            # Navigation components
│   │   │   ├── navbar.js
│   │   │   └── navbar.xml
│   │   ├── screens/           # Screen components
│   │   │   ├── product_screen/
│   │   │   ├── payment_screen/
│   │   │   ├── receipt_screen/
│   │   │   └── ...
│   │   ├── generic_components/
│   │   │   ├── numpad/
│   │   │   ├── orderline/
│   │   │   └── ...
│   │   ├── store/             # State management
│   │   │   ├── pos_store.js
│   │   │   └── ...
│   │   └── utils/             # Utilities
│   └── scss/                  # Styles
│       ├── pos_variables_extra.scss
│       └── ...
├── views/
└── ...
```

### Asset Loading in v17.0

Assets are declared in `__manifest__.py`:

```python
'assets': {
    'point_of_sale._assets_pos': [
        # Your custom files will be loaded here
        'custom_module/static/src/**/*',
    ],
}
```

### Key Components Location

| Component | Path |
|-----------|------|
| Navbar | `static/src/app/navbar/navbar.js` |
| Product Screen | `static/src/app/screens/product_screen/product_screen.js` |
| Payment Screen | `static/src/app/screens/payment_screen/payment_screen.js` |
| Receipt Screen | `static/src/app/screens/receipt_screen/receipt_screen.js` |
| Numpad | `static/src/app/generic_components/numpad/numpad.js` |
| Order Widget | `static/src/app/generic_components/order_widget/order_widget.js` |

---

## Developer Guide for v17.0

### Module Setup

#### 1. Create Module Structure

```bash
mkdir -p custom_pos_v17
cd custom_pos_v17
mkdir -p models static/src/app/overrides static/src/scss views data security
touch __init__.py __manifest__.py
```

#### 2. Create `__manifest__.py`

```python
# -*- coding: utf-8 -*-
{
    'name': 'Custom POS v17',
    'version': '17.0.1.0.0',
    'category': 'Sales/Point of Sale',
    'summary': 'POS Customizations for Odoo 17.0',
    'description': """
        Custom POS Module for Odoo 17.0
        ================================

        Features:
        - Custom layout modifications
        - Additional fields and functions
        - Custom payment methods
        - Receipt customizations
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'point_of_sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/pos_config_views.xml',
        'data/default_data.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            # JavaScript files
            'custom_pos_v17/static/src/app/overrides/**/*.js',
            # XML templates
            'custom_pos_v17/static/src/app/overrides/**/*.xml',
            # Styles
            'custom_pos_v17/static/src/scss/**/*.scss',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
```

#### 3. Create `__init__.py`

```python
# -*- coding: utf-8 -*-
from . import models
```

#### 4. Create `models/__init__.py`

```python
# -*- coding: utf-8 -*-
from . import pos_config
from . import pos_order
from . import res_partner
```

---

### Inheriting Python Models

#### Example 1: Extend pos.config

File: `models/pos_config.py`

```python
# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class PosConfig(models.Model):
    _inherit = 'pos.config'

    # Add custom fields
    enable_loyalty_system = fields.Boolean(
        string='Enable Loyalty System',
        default=False,
        help='Enable custom loyalty point system'
    )

    loyalty_rate = fields.Float(
        string='Loyalty Rate',
        default=1.0,
        help='Points earned per dollar spent'
    )

    custom_receipt_header = fields.Text(
        string='Custom Receipt Header',
        help='Custom text to display at top of receipt'
    )

    max_discount_percentage = fields.Float(
        string='Maximum Discount %',
        default=20.0,
        help='Maximum discount percentage allowed'
    )

    @api.constrains('max_discount_percentage')
    def _check_max_discount(self):
        """Validate discount percentage is reasonable."""
        for config in self:
            if config.max_discount_percentage < 0 or config.max_discount_percentage > 100:
                raise ValidationError(_('Maximum discount must be between 0 and 100%'))

    def _get_pos_ui_data(self, params):
        """Add custom fields to POS UI data."""
        result = super()._get_pos_ui_data(params)
        result['enable_loyalty_system'] = self.enable_loyalty_system
        result['loyalty_rate'] = self.loyalty_rate
        result['custom_receipt_header'] = self.custom_receipt_header
        result['max_discount_percentage'] = self.max_discount_percentage
        return result
```

#### Example 2: Extend pos.order

File: `models/pos_order.py`

```python
# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class PosOrder(models.Model):
    _inherit = 'pos.order'

    # Custom fields
    order_notes = fields.Text(
        string='Order Notes',
        help='Special instructions or notes for this order'
    )

    loyalty_points_earned = fields.Integer(
        string='Loyalty Points Earned',
        compute='_compute_loyalty_points',
        store=True
    )

    loyalty_points_used = fields.Integer(
        string='Loyalty Points Used',
        default=0
    )

    is_vip_order = fields.Boolean(
        string='VIP Order',
        compute='_compute_is_vip_order',
        store=True
    )

    @api.depends('partner_id', 'amount_total')
    def _compute_loyalty_points(self):
        """Calculate loyalty points based on order total."""
        for order in self:
            if order.session_id.config_id.enable_loyalty_system:
                # Points = amount * rate (e.g., $100 * 1.0 = 100 points)
                rate = order.session_id.config_id.loyalty_rate
                order.loyalty_points_earned = int(order.amount_total * rate)
            else:
                order.loyalty_points_earned = 0

    @api.depends('partner_id')
    def _compute_is_vip_order(self):
        """Determine if this is a VIP customer order."""
        for order in self:
            order.is_vip_order = (
                order.partner_id and
                hasattr(order.partner_id, 'is_vip') and
                order.partner_id.is_vip
            )

    def _export_for_ui(self, order):
        """Add custom fields to order data sent to POS UI."""
        result = super()._export_for_ui(order)
        result.update({
            'order_notes': order.order_notes,
            'loyalty_points_earned': order.loyalty_points_earned,
            'loyalty_points_used': order.loyalty_points_used,
            'is_vip_order': order.is_vip_order,
        })
        return result

    def _prepare_invoice_vals(self):
        """Override to include custom fields in invoice."""
        vals = super()._prepare_invoice_vals()
        if self.order_notes:
            vals['narration'] = self.order_notes
        return vals

    @api.model
    def sync_from_ui(self, orders):
        """Override to handle custom data from POS UI."""
        result = super().sync_from_ui(orders)

        # Process custom loyalty points logic
        for order_data in orders:
            if order_data.get('data', {}).get('loyalty_points_used'):
                order = self.browse(order_data.get('id'))
                if order:
                    order._process_loyalty_redemption(
                        order_data['data']['loyalty_points_used']
                    )

        return result

    def _process_loyalty_redemption(self, points_used):
        """Process loyalty points redemption."""
        self.ensure_one()
        if self.partner_id and points_used > 0:
            # Deduct points from partner's balance
            self.partner_id.sudo().write({
                'loyalty_points': self.partner_id.loyalty_points - points_used
            })
```

#### Example 3: Extend res.partner

File: `models/res_partner.py`

```python
# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Loyalty system fields
    loyalty_points = fields.Integer(
        string='Loyalty Points',
        default=0,
        help='Available loyalty points balance'
    )

    total_loyalty_earned = fields.Integer(
        string='Total Points Earned',
        compute='_compute_loyalty_stats',
        store=True
    )

    is_vip = fields.Boolean(
        string='VIP Customer',
        default=False
    )

    customer_tier = fields.Selection([
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ], string='Customer Tier', compute='_compute_customer_tier', store=True)

    @api.depends('loyalty_points')
    def _compute_customer_tier(self):
        """Compute customer tier based on loyalty points."""
        for partner in self:
            points = partner.loyalty_points
            if points >= 10000:
                partner.customer_tier = 'platinum'
            elif points >= 5000:
                partner.customer_tier = 'gold'
            elif points >= 1000:
                partner.customer_tier = 'silver'
            else:
                partner.customer_tier = 'bronze'

    @api.depends('loyalty_points')
    def _compute_loyalty_stats(self):
        """Compute loyalty statistics."""
        for partner in self:
            orders = self.env['pos.order'].search([
                ('partner_id', '=', partner.id)
            ])
            partner.total_loyalty_earned = sum(orders.mapped('loyalty_points_earned'))

    @api.model
    def get_loyalty_balance(self, partner_id):
        """API method to get loyalty balance from POS."""
        partner = self.browse(partner_id)
        return partner.loyalty_points if partner else 0
```

---

### Extending OWL Components

#### Understanding OWL in v17.0

Odoo 17.0 uses OWL (Odoo Web Library) for the POS frontend. Components are defined using:

```javascript
import { Component } from "@odoo/owl";

export class MyComponent extends Component {
    static template = "my_module.MyComponent";
    static props = {};

    setup() {
        // Component initialization
    }
}
```

#### Patching Existing Components

File: `static/src/app/overrides/navbar.js`

```javascript
/** @odoo-module */

import { Navbar } from "@point_of_sale/app/navbar/navbar";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";

patch(Navbar.prototype, {
    setup() {
        super.setup(...arguments);
        this.pos = usePos();
    },

    /**
     * Get custom logo URL
     */
    get customLogoUrl() {
        const config = this.pos.config;
        if (config.custom_logo) {
            return `/web/image?model=pos.config&id=${config.id}&field=custom_logo`;
        }
        return '/web/static/img/logo.png';
    },

    /**
     * Show custom notification
     */
    showWelcomeMessage() {
        const cashier = this.pos.get_cashier();
        this.notification.add(
            `Welcome back, ${cashier.name}!`,
            {
                type: 'success',
                duration: 3000
            }
        );
    },

    /**
     * Override session opening
     */
    async openSession() {
        await super.openSession(...arguments);
        this.showWelcomeMessage();
    }
});
```

#### Modifying Templates

File: `static/src/app/overrides/navbar.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates id="template" xml:space="preserve">

    <!-- Extend Navbar template -->
    <t t-inherit="point_of_sale.Navbar" t-inherit-mode="extension">

        <!-- Replace logo -->
        <xpath expr="//img[@class='pos-logo h-75 ms-3 me-auto align-self-center']" position="replace">
            <img class="pos-logo h-75 ms-3 me-auto align-self-center custom-logo"
                 t-att-src="customLogoUrl"
                 t-on-click="onLogoClick"
                 alt="Logo" />
        </xpath>

        <!-- Add custom menu item -->
        <xpath expr="//ul[@class='dropdown-menu sub-menu position-absolute d-flex flex-column align-items-stretch bg-white shadow-lg z-index-1']" position="inside">
            <li class="menu-item navbar-button custom-menu-item" t-on-click="onCustomMenuClick">
                <a class="dropdown-item py-2">
                    <i class="fa fa-star me-2" />
                    Loyalty Program
                </a>
            </li>
        </xpath>

    </t>

</templates>
```

---

### Layout Customization

#### Example: Customize Product Screen

File: `static/src/app/overrides/product_screen.js`

```javascript
/** @odoo-module */

import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { patch } from "@web/core/utils/patch";

patch(ProductScreen.prototype, {
    setup() {
        super.setup(...arguments);
    },

    /**
     * Add custom product filter
     */
    get customFilteredProducts() {
        const products = this.pos.db.get_product_by_category(this.selectedCategoryId);

        // Filter based on custom criteria
        if (this.pos.config.enable_loyalty_system) {
            return products.filter(product => {
                // Show only loyalty-eligible products if VIP customer
                const partner = this.currentOrder.get_partner();
                if (partner && partner.is_vip) {
                    return product.loyalty_eligible !== false;
                }
                return true;
            });
        }

        return products;
    },

    /**
     * Override product click to show custom info
     */
    async onClickProduct(product) {
        // Show loyalty points that will be earned
        if (this.pos.config.enable_loyalty_system) {
            const points = Math.floor(product.lst_price * this.pos.config.loyalty_rate);
            if (points > 0) {
                this.notification.add(
                    `Earn ${points} loyalty points with this purchase!`,
                    { type: 'info', duration: 2000 }
                );
            }
        }

        // Call original method
        return super.onClickProduct(...arguments);
    }
});
```

#### Example: Custom Product Screen Template

File: `static/src/app/overrides/product_screen.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates id="template" xml:space="preserve">

    <!-- Add loyalty badge to products -->
    <t t-inherit="point_of_sale.ProductCard" t-inherit-mode="extension">
        <xpath expr="//div[@class='product-content']" position="inside">
            <div t-if="props.product.loyalty_eligible" class="loyalty-badge">
                <i class="fa fa-star text-warning"/>
                <span class="ms-1">Earn Points!</span>
            </div>
        </xpath>
    </t>

</templates>
```

#### Custom Styling

File: `static/src/scss/custom_pos.scss`

```scss
// Custom POS Styles for v17.0

// Brand colors
$primary-color: #667eea;
$secondary-color: #764ba2;
$accent-color: #f59e0b;

// Navbar customization
.pos-topheader {
    background: linear-gradient(135deg, $primary-color 0%, $secondary-color 100%);

    .custom-logo {
        height: 50px;
        filter: brightness(1.1);
        transition: transform 0.3s ease;

        &:hover {
            transform: scale(1.05);
        }
    }
}

// Product card customization
.product {
    border-radius: 12px;
    overflow: hidden;
    transition: all 0.3s ease;

    &:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
    }

    .loyalty-badge {
        position: absolute;
        top: 10px;
        right: 10px;
        background: $accent-color;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
}

// Payment screen customization
.payment-screen {
    .btn-primary {
        background: linear-gradient(135deg, $primary-color 0%, $secondary-color 100%);
        border: none;

        &:hover {
            background: linear-gradient(135deg, darken($primary-color, 5%) 0%, darken($secondary-color, 5%) 100%);
        }
    }
}

// Custom numpad styling
.numpad {
    button {
        font-size: 1.2rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.2s ease;

        &:active {
            transform: scale(0.95);
        }

        &.btn-info {
            background-color: $primary-color;
            border-color: $primary-color;
            color: white;
        }
    }
}
```

---

### Adding Custom Functions

#### Creating Custom Service

File: `static/src/app/services/loyalty_service.js`

```javascript
/** @odoo-module */

import { registry } from "@web/core/registry";

export const loyaltyService = {
    dependencies: ["pos", "orm", "popup", "notification"],

    start(env, { pos, orm, popup, notification }) {
        return {
            /**
             * Calculate loyalty points for an order
             */
            calculateLoyaltyPoints(order) {
                if (!pos.config.enable_loyalty_system) {
                    return 0;
                }

                const total = order.get_total_with_tax();
                const rate = pos.config.loyalty_rate || 1.0;
                return Math.floor(total * rate);
            },

            /**
             * Show loyalty points popup
             */
            async showLoyaltyInfo(partner) {
                if (!partner) {
                    await popup.add('ErrorPopup', {
                        title: 'No Customer Selected',
                        body: 'Please select a customer to view loyalty points.'
                    });
                    return;
                }

                const points = partner.loyalty_points || 0;
                const tier = partner.customer_tier || 'bronze';

                await popup.add('ConfirmPopup', {
                    title: `Loyalty Program - ${partner.name}`,
                    body: `
                        Current Points: ${points}
                        Tier: ${tier.toUpperCase()}

                        Keep shopping to earn more points!
                    `
                });
            },

            /**
             * Redeem loyalty points
             */
            async redeemPoints(order) {
                const partner = order.get_partner();

                if (!partner) {
                    await popup.add('ErrorPopup', {
                        title: 'No Customer',
                        body: 'Please select a customer to redeem points.'
                    });
                    return false;
                }

                const availablePoints = partner.loyalty_points || 0;

                if (availablePoints === 0) {
                    await popup.add('ErrorPopup', {
                        title: 'No Points Available',
                        body: 'Customer has no loyalty points to redeem.'
                    });
                    return false;
                }

                // 100 points = $1 discount
                const maxDiscount = availablePoints / 100;
                const orderTotal = order.get_total_with_tax();
                const maxRedeemable = Math.min(maxDiscount, orderTotal);

                const { confirmed, payload } = await popup.add('NumberPopup', {
                    title: `Redeem Points (Available: ${availablePoints})`,
                    startingValue: 0,
                    body: `Enter points to redeem (Max: ${Math.floor(maxRedeemable * 100)})`
                });

                if (confirmed && payload > 0) {
                    if (payload > availablePoints) {
                        await popup.add('ErrorPopup', {
                            title: 'Insufficient Points',
                            body: `Customer only has ${availablePoints} points.`
                        });
                        return false;
                    }

                    const discountAmount = payload / 100;

                    // Apply discount to order
                    order.loyalty_points_redeemed = payload;

                    // Create discount line
                    const discountProduct = pos.db.get_product_by_id(
                        pos.config.discount_product_id?.[0]
                    );

                    if (discountProduct) {
                        order.add_product(discountProduct, {
                            price: -discountAmount,
                            quantity: 1,
                            merge: false
                        });
                    }

                    notification.add(
                        `Redeemed ${payload} points for $${discountAmount.toFixed(2)} discount`,
                        { type: 'success', duration: 3000 }
                    );

                    return true;
                }

                return false;
            },

            /**
             * Sync loyalty points to backend
             */
            async syncLoyaltyPoints(orderId, pointsEarned, pointsUsed) {
                try {
                    await orm.call('pos.order', 'update_loyalty_points', [
                        orderId,
                        pointsEarned,
                        pointsUsed
                    ]);
                    return true;
                } catch (error) {
                    console.error('Failed to sync loyalty points:', error);
                    return false;
                }
            }
        };
    }
};

registry.category("services").add("loyalty", loyaltyService);
```

---

### Adding Custom Fields

#### Backend: Session Loader

File: `models/pos_session.py`

```python
# -*- coding: utf-8 -*-
from odoo import models

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_res_partner(self):
        """Add custom fields to partner data loaded in POS."""
        result = super()._loader_params_res_partner()
        result['search_params']['fields'].extend([
            'loyalty_points',
            'total_loyalty_earned',
            'is_vip',
            'customer_tier',
        ])
        return result

    def _loader_params_product_product(self):
        """Add custom fields to product data loaded in POS."""
        result = super()._loader_params_product_product()
        result['search_params']['fields'].extend([
            'loyalty_eligible',
            'loyalty_points_multiplier',
        ])
        return result

    def _pos_ui_models_to_load(self):
        """Add custom models to load in POS."""
        result = super()._pos_ui_models_to_load()
        # Add any custom models needed
        return result
```

#### Frontend: Display Custom Fields

File: `static/src/app/overrides/partner_line.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates id="template" xml:space="preserve">

    <!-- Show loyalty info in partner list -->
    <t t-inherit="point_of_sale.PartnerLine" t-inherit-mode="extension">

        <!-- Add loyalty badge -->
        <xpath expr="//div[@class='partner-name']" position="after">
            <div class="partner-loyalty-info d-flex align-items-center gap-2 mt-1">

                <!-- VIP Badge -->
                <span t-if="props.partner.is_vip" class="badge bg-warning text-dark">
                    <i class="fa fa-star"/> VIP
                </span>

                <!-- Tier Badge -->
                <span t-if="props.partner.customer_tier"
                      t-attf-class="badge bg-{{ props.partner.customer_tier === 'platinum' ? 'dark' : props.partner.customer_tier === 'gold' ? 'warning' : props.partner.customer_tier === 'silver' ? 'secondary' : 'light' }}">
                    <t t-esc="props.partner.customer_tier.toUpperCase()"/>
                </span>

                <!-- Points Balance -->
                <span t-if="props.partner.loyalty_points" class="badge bg-info">
                    <i class="fa fa-trophy"/> <t t-esc="props.partner.loyalty_points"/> pts
                </span>

            </div>
        </xpath>

    </t>

</templates>
```

---

### Modifying Numpad (Keypad)

#### Custom Numpad Buttons

File: `static/src/app/overrides/payment_screen.js`

```javascript
/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {
    /**
     * Add custom quick amount buttons to numpad
     */
    getNumpadButtons() {
        const buttons = super.getNumpadButtons(...arguments);

        // Add quick cash buttons
        return [
            ...buttons,
            { text: '$5', value: 'quick_5', class: 'btn-success' },
            { text: '$10', value: 'quick_10', class: 'btn-success' },
            { text: '$20', value: 'quick_20', class: 'btn-success' },
            { text: '$50', value: 'quick_50', class: 'btn-success' },
            { text: 'Exact', value: 'exact', class: 'btn-primary' },
        ];
    },

    /**
     * Handle custom numpad clicks
     */
    _onNumpadClick(buttonValue) {
        const selectedPaymentLine = this.currentOrder.selected_paymentline;

        // Handle quick amount buttons
        if (buttonValue.startsWith('quick_')) {
            const amount = parseFloat(buttonValue.split('_')[1]);
            if (selectedPaymentLine) {
                selectedPaymentLine.set_amount(amount);
            }
            return;
        }

        // Handle "Exact" button
        if (buttonValue === 'exact') {
            const due = this.currentOrder.get_due();
            if (selectedPaymentLine && due > 0) {
                selectedPaymentLine.set_amount(due);
            }
            return;
        }

        // Call original method for other buttons
        super._onNumpadClick(...arguments);
    }
});
```

#### Complete Custom Numpad Component

File: `static/src/app/components/custom_numpad/custom_numpad.js`

```javascript
/** @odoo-module */

import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class CustomNumpad extends Component {
    static template = "custom_pos_v17.CustomNumpad";
    static props = {
        onClick: Function,
        value: { type: String, optional: true },
        class: { type: String, optional: true },
    };

    setup() {
        this.pos = usePos();
    }

    get buttons() {
        return [
            // Number buttons
            { value: '1', text: '1', class: 'btn-light' },
            { value: '2', text: '2', class: 'btn-light' },
            { value: '3', text: '3', class: 'btn-light' },
            { value: 'qty', text: 'Qty', class: 'btn-primary' },

            { value: '4', text: '4', class: 'btn-light' },
            { value: '5', text: '5', class: 'btn-light' },
            { value: '6', text: '6', class: 'btn-light' },
            { value: 'disc', text: 'Disc', class: 'btn-warning' },

            { value: '7', text: '7', class: 'btn-light' },
            { value: '8', text: '8', class: 'btn-light' },
            { value: '9', text: '9', class: 'btn-light' },
            { value: 'price', text: 'Price', class: 'btn-info' },

            { value: '+/-', text: '+/-', class: 'btn-secondary' },
            { value: '0', text: '0', class: 'btn-light' },
            { value: '.', text: '.', class: 'btn-light' },
            { value: 'Backspace', text: '⌫', class: 'btn-danger' },
        ];
    }

    onClick(value) {
        this.props.onClick(value);
    }
}
```

File: `static/src/app/components/custom_numpad/custom_numpad.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates id="template" xml:space="preserve">

    <t t-name="custom_pos_v17.CustomNumpad">
        <div t-attf-class="custom-numpad {{ props.class || '' }}">
            <div class="numpad-grid row g-2">
                <div t-foreach="buttons" t-as="button" t-key="button.value" class="col-3">
                    <button t-attf-class="numpad-btn btn w-100 py-3 {{ button.class }}"
                            t-on-click="() => this.onClick(button.value)">
                        <span class="fw-bold" t-esc="button.text"/>
                    </button>
                </div>
            </div>
        </div>
    </t>

</templates>
```

---

### Payment Customization

#### Custom Payment Method Handler

File: `static/src/app/overrides/payment_screen.js`

```javascript
/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

patch(PaymentScreen.prototype, {
    setup() {
        super.setup(...arguments);
        this.loyalty = useService("loyalty");
    },

    /**
     * Override to handle custom payment methods
     */
    async addNewPaymentLine(paymentMethod) {
        // Handle loyalty points payment
        if (paymentMethod.use_payment_terminal === 'loyalty_points') {
            return await this.handleLoyaltyPayment(paymentMethod);
        }

        // Handle gift card payment
        if (paymentMethod.use_payment_terminal === 'gift_card') {
            return await this.handleGiftCardPayment(paymentMethod);
        }

        // Handle mobile payment
        if (paymentMethod.use_payment_terminal === 'mobile_payment') {
            return await this.handleMobilePayment(paymentMethod);
        }

        // Default handling
        return super.addNewPaymentLine(...arguments);
    },

    /**
     * Handle loyalty points payment
     */
    async handleLoyaltyPayment(paymentMethod) {
        const partner = this.currentOrder.get_partner();

        if (!partner) {
            await this.popup.add('ErrorPopup', {
                title: 'Customer Required',
                body: 'Please select a customer to pay with loyalty points.'
            });
            return;
        }

        const success = await this.loyalty.redeemPoints(this.currentOrder);

        if (success) {
            // Payment line was added by loyalty service
            return;
        }
    },

    /**
     * Handle gift card payment
     */
    async handleGiftCardPayment(paymentMethod) {
        const { confirmed, payload: cardNumber } = await this.popup.add('TextInputPopup', {
            title: 'Gift Card Payment',
            startingValue: '',
            placeholder: 'Enter gift card number'
        });

        if (confirmed && cardNumber) {
            try {
                // Validate gift card
                const cardData = await this.orm.call(
                    'gift.card',
                    'validate_and_get_balance',
                    [cardNumber]
                );

                if (!cardData.valid) {
                    await this.popup.add('ErrorPopup', {
                        title: 'Invalid Gift Card',
                        body: cardData.message || 'This gift card is not valid.'
                    });
                    return;
                }

                // Add payment line
                const paymentLine = await super.addNewPaymentLine(paymentMethod);
                const due = this.currentOrder.get_due();
                const amount = Math.min(cardData.balance, due);

                paymentLine.set_amount(amount);
                paymentLine.card_number = cardNumber;
                paymentLine.card_balance = cardData.balance;

                this.notification.add(
                    `Gift card applied: $${amount.toFixed(2)}`,
                    { type: 'success', duration: 3000 }
                );

            } catch (error) {
                console.error('Gift card error:', error);
                await this.popup.add('ErrorPopup', {
                    title: 'Error',
                    body: 'Failed to process gift card. Please try again.'
                });
            }
        }
    },

    /**
     * Handle mobile payment (QR code)
     */
    async handleMobilePayment(paymentMethod) {
        const order = this.currentOrder;
        const amount = order.get_due();

        try {
            // Generate QR code for payment
            const qrData = await this.orm.call(
                'pos.payment',
                'generate_mobile_payment_qr',
                [order.name, amount]
            );

            // Show QR code popup
            const { confirmed } = await this.popup.add('ConfirmPopup', {
                title: 'Scan to Pay',
                body: `
                    <div class="text-center">
                        <img src="data:image/png;base64,${qrData.qr_code}"
                             style="max-width: 300px;"
                             alt="Payment QR Code"/>
                        <p class="mt-3">Amount: $${amount.toFixed(2)}</p>
                        <p>Scan with mobile app to complete payment</p>
                    </div>
                `,
                confirmText: 'Payment Received',
                cancelText: 'Cancel'
            });

            if (confirmed) {
                // Add payment line
                const paymentLine = await super.addNewPaymentLine(paymentMethod);
                paymentLine.set_amount(amount);
                paymentLine.transaction_id = qrData.transaction_id;
            }

        } catch (error) {
            console.error('Mobile payment error:', error);
            await this.popup.add('ErrorPopup', {
                title: 'Error',
                body: 'Failed to generate payment QR code.'
            });
        }
    },

    /**
     * Override validation to add custom checks
     */
    async validateOrder(isForceValidate) {
        const order = this.currentOrder;

        // Check maximum discount limit
        const totalDiscount = order.get_total_discount();
        const maxDiscount = order.get_total_without_tax() *
            (this.pos.config.max_discount_percentage / 100);

        if (totalDiscount > maxDiscount) {
            const { confirmed } = await this.popup.add('ConfirmPopup', {
                title: 'Discount Exceeds Limit',
                body: `Discount exceeds maximum allowed (${this.pos.config.max_discount_percentage}%). Manager approval required.`
            });

            if (!confirmed) {
                return;
            }
        }

        // Process loyalty points
        if (this.pos.config.enable_loyalty_system && order.get_partner()) {
            const pointsEarned = this.loyalty.calculateLoyaltyPoints(order);
            order.loyalty_points_earned = pointsEarned;

            if (pointsEarned > 0) {
                this.notification.add(
                    `Customer will earn ${pointsEarned} loyalty points!`,
                    { type: 'success', duration: 4000 }
                );
            }
        }

        return super.validateOrder(...arguments);
    }
});
```

---

### Receipt Customization

#### Custom Receipt Header

File: `static/src/app/overrides/receipt_header.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates id="template" xml:space="preserve">

    <!-- Customize receipt header -->
    <t t-inherit="point_of_sale.ReceiptHeader" t-inherit-mode="extension">

        <!-- Add custom header text -->
        <xpath expr="//div[@class='pos-receipt-contact']" position="before">
            <div t-if="props.data.custom_header" class="custom-receipt-header text-center mb-3">
                <div class="custom-header-text" style="white-space: pre-line;">
                    <t t-esc="props.data.custom_header"/>
                </div>
            </div>
        </xpath>

        <!-- Add QR code for digital receipt -->
        <xpath expr="//div[@class='pos-receipt-contact']" position="after">
            <div t-if="props.data.receipt_qr" class="receipt-qr text-center my-3">
                <img t-att-src="props.data.receipt_qr"
                     style="max-width: 150px;"
                     alt="Receipt QR Code"/>
                <p class="text-muted small">Scan for digital receipt</p>
            </div>
        </xpath>

    </t>

</templates>
```

#### Custom Receipt Body

File: `static/src/app/overrides/order_receipt.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates id="template" xml:space="preserve">

    <!-- Customize order receipt -->
    <t t-inherit="point_of_sale.OrderReceipt" t-inherit-mode="extension">

        <!-- Add loyalty points section -->
        <xpath expr="//div[@class='pos-receipt-amount receipt-change mt-2']" position="after">
            <t t-if="props.data.loyalty_points_earned or props.data.loyalty_points_used">
                <br/>
                <div class="loyalty-section">
                    <div class="section-header fw-bold">LOYALTY PROGRAM</div>

                    <t t-if="props.data.loyalty_points_used">
                        <div class="loyalty-line">
                            Points Redeemed:
                            <span class="pos-receipt-right-align">
                                -<t t-esc="props.data.loyalty_points_used"/>
                            </span>
                        </div>
                    </t>

                    <t t-if="props.data.loyalty_points_earned">
                        <div class="loyalty-line">
                            Points Earned:
                            <span class="pos-receipt-right-align text-success">
                                +<t t-esc="props.data.loyalty_points_earned"/>
                            </span>
                        </div>
                    </t>

                    <t t-if="props.data.partner_loyalty_balance">
                        <div class="loyalty-line fw-bold mt-2">
                            New Balance:
                            <span class="pos-receipt-right-align">
                                <t t-esc="props.data.partner_loyalty_balance"/>
                            </span>
                        </div>
                    </t>
                </div>
            </t>
        </xpath>

        <!-- Add customer tier info -->
        <xpath expr="//div[@class='before-footer']" position="inside">
            <t t-if="props.data.partner_tier">
                <div class="customer-tier-info text-center my-3">
                    <div class="tier-badge badge bg-primary">
                        <t t-esc="props.data.partner_tier.toUpperCase()"/> MEMBER
                    </div>
                    <p class="small text-muted mt-2">
                        Thank you for being a valued customer!
                    </p>
                </div>
            </t>
        </xpath>

        <!-- Remove Odoo branding, add custom branding -->
        <xpath expr="//div[@class='pos-receipt-order-data']/p[text()='Powered by Odoo']" position="replace">
            <p class="custom-branding">Powered by instant-ERP</p>
        </xpath>

        <!-- Add custom footer -->
        <xpath expr="//div[@class='after-footer']" position="after">
            <div class="custom-footer text-center mt-3">
                <p class="small">Visit us at www.instant-erp.com</p>
                <p class="small">Follow us @instantERP</p>
                <br/>
                <p class="small text-muted">
                    Thank you for your business!
                </p>
            </div>
        </xpath>

    </t>

</templates>
```

#### Backend Receipt Data

File: `models/pos_order.py` (add to previous example)

```python
def _export_for_ui(self, order):
    """Add custom receipt data."""
    result = super()._export_for_ui(order)

    # Add custom header
    if order.session_id.config_id.custom_receipt_header:
        result['custom_header'] = order.session_id.config_id.custom_receipt_header

    # Add loyalty data
    if order.partner_id:
        result['partner_loyalty_balance'] = order.partner_id.loyalty_points
        result['partner_tier'] = order.partner_id.customer_tier

    # Generate receipt QR code
    if order.pos_reference:
        result['receipt_qr'] = self._generate_receipt_qr(order.pos_reference)

    return result

def _generate_receipt_qr(self, reference):
    """Generate QR code for digital receipt."""
    import qrcode
    import base64
    from io import BytesIO

    # Create QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f"https://your-domain.com/receipt/{reference}")
    qr.make(fit=True)

    # Convert to image
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')

    return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"
```

---

## instant-ERP Debranding Proposal

Complete implementation for rebranding Odoo POS to instant-ERP.

### Module Structure

```
instant_erp_pos_branding/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── pos_config.py
│   └── res_company.py
├── static/
│   └── src/
│       ├── app/
│       │   └── overrides/
│       │       ├── navbar.js
│       │       ├── navbar.xml
│       │       ├── receipt_header.xml
│       │       └── order_receipt.xml
│       ├── img/
│       │   ├── instant_erp_logo.png
│       │   └── instant_erp_receipt_logo.png
│       └── scss/
│           └── instant_erp_branding.scss
└── views/
    └── pos_config_views.xml
```

### Implementation Files

#### 1. Manifest

File: `__manifest__.py`

```python
# -*- coding: utf-8 -*-
{
    'name': 'instant-ERP POS Branding',
    'version': '17.0.1.0.0',
    'category': 'Sales/Point of Sale',
    'summary': 'Rebrand Odoo POS to instant-ERP',
    'description': """
        instant-ERP POS Branding for Odoo 17.0
        =======================================

        Complete rebranding solution:
        - Replace Odoo logo with instant-ERP logo
        - Remove all Odoo references from receipts
        - Custom instant-ERP styling
        - Uses inheritance only - no core file modifications
    """,
    'author': 'instant-ERP Team',
    'website': 'https://www.instant-erp.com',
    'license': 'LGPL-3',
    'depends': ['point_of_sale'],
    'data': [
        'views/pos_config_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'instant_erp_pos_branding/static/src/app/overrides/**/*.js',
            'instant_erp_pos_branding/static/src/app/overrides/**/*.xml',
            'instant_erp_pos_branding/static/src/scss/**/*.scss',
        ],
    },
    'images': [
        'static/description/icon.png',
        'static/src/img/instant_erp_logo.png',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
```

#### 2. Replace Navbar Logo

File: `static/src/app/overrides/navbar.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates id="template" xml:space="preserve">

    <!-- Replace Odoo logo with instant-ERP logo -->
    <t t-inherit="point_of_sale.Navbar" t-inherit-mode="extension">
        <xpath expr="//img[@alt='Logo']" position="replace">
            <img class="pos-logo h-75 ms-3 me-auto align-self-center instant-erp-logo"
                 src="/instant_erp_pos_branding/static/src/img/instant_erp_logo.png"
                 alt="instant-ERP Logo" />
        </xpath>
    </t>

</templates>
```

#### 3. Rebrand Receipts

File: `static/src/app/overrides/order_receipt.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates id="template" xml:space="preserve">

    <!-- Remove Odoo branding from receipts -->
    <t t-inherit="point_of_sale.OrderReceipt" t-inherit-mode="extension">

        <!-- Replace "Powered by Odoo" -->
        <xpath expr="//p[text()='Powered by Odoo']" position="replace">
            <p class="instant-erp-powered-by">Powered by instant-ERP</p>
        </xpath>

        <!-- Add instant-ERP footer -->
        <xpath expr="//div[@class='after-footer']" position="after">
            <div class="instant-erp-footer text-center mt-3">
                <p>www.instant-erp.com</p>
                <p class="small">Modern ERP. Simplified.</p>
            </div>
        </xpath>

    </t>

</templates>
```

File: `static/src/app/overrides/receipt_header.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates id="template" xml:space="preserve">

    <!-- Add instant-ERP branding to receipt header -->
    <t t-inherit="point_of_sale.ReceiptHeader" t-inherit-mode="extension">

        <xpath expr="//img[@class='pos-receipt-logo']" position="before">
            <div class="instant-erp-receipt-header text-center mb-2">
                <img src="/instant_erp_pos_branding/static/src/img/instant_erp_receipt_logo.png"
                     alt="instant-ERP"
                     style="max-width: 180px; margin: 0 auto 10px;"/>
            </div>
        </xpath>

    </t>

</templates>
```

#### 4. Custom Styling

File: `static/src/scss/instant_erp_branding.scss`

```scss
// instant-ERP Branding for Odoo 17.0 POS

// Brand Colors
$instant-primary: #2563eb;
$instant-secondary: #7c3aed;
$instant-accent: #f59e0b;

// Navbar Logo
.instant-erp-logo {
    max-height: 50px;
    width: auto;
    object-fit: contain;
}

// Receipt Branding
.pos-receipt {
    .instant-erp-receipt-header {
        border-bottom: 2px solid $instant-primary;
        padding-bottom: 10px;
    }

    .instant-erp-powered-by {
        color: $instant-primary;
        font-weight: 600;
        font-size: 1.1em;
    }

    .instant-erp-footer {
        color: $instant-secondary;
        font-size: 0.9em;

        p {
            margin: 5px 0;
        }
    }
}

// Optional: Custom button colors
.pos-content {
    .btn-primary {
        background: linear-gradient(135deg, $instant-primary, $instant-secondary);
        border: none;

        &:hover {
            background: linear-gradient(135deg,
                darken($instant-primary, 5%),
                darken($instant-secondary, 5%)
            );
        }
    }
}
```

### Installation & Testing

1. **Place module in addons directory**
2. **Update Apps List** (Settings → Apps → Update Apps List)
3. **Install module** (Search "instant-ERP POS Branding" → Install)
4. **Open POS** and verify:
   - [ ] instant-ERP logo appears in navbar
   - [ ] Receipt shows instant-ERP branding
   - [ ] No "Powered by Odoo" text visible
   - [ ] Custom styling applied

---

## v17.0 Specific Best Practices

### 1. Use Modern JavaScript

```javascript
// ✅ Good: Use arrow functions and modern syntax
patch(Component.prototype, {
    async loadData() {
        const data = await this.orm.call('model', 'method', []);
        return data.filter(item => item.active);
    }
});

// ❌ Avoid: Old-style JavaScript
patch(Component.prototype, {
    loadData: function() {
        var self = this;
        return this.orm.call('model', 'method', []).then(function(data) {
            return data.filter(function(item) { return item.active; });
        });
    }
});
```

### 2. Proper Asset Declaration

```python
'assets': {
    'point_of_sale._assets_pos': [
        # Use wildcards for convenience
        'my_module/static/src/**/*.js',
        'my_module/static/src/**/*.xml',
        'my_module/static/src/**/*.scss',

        # Or specify exact order when needed
        'my_module/static/src/scss/variables.scss',
        'my_module/static/src/scss/components.scss',
    ],
}
```

### 3. Component Hooks

```javascript
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";

setup() {
    super.setup(...arguments);
    this.pos = usePos();
    this.orm = useService("orm");
    this.popup = useService("popup");
    this.notification = useService("pos_notification");
}
```

### 4. Error Handling

```javascript
async performAction() {
    try {
        const result = await this.orm.call('model', 'method', []);
        this.notification.add('Success!', { type: 'success' });
        return result;
    } catch (error) {
        console.error('Action failed:', error);
        await this.popup.add('ErrorPopup', {
            title: 'Error',
            body: error.message || 'Operation failed'
        });
        return false;
    }
}
```

---

## Troubleshooting v17.0

### JavaScript Not Loading

**Check:**
1. Asset declaration in `__manifest__.py`
2. File paths are correct
3. Module is upgraded: `odoo-bin -u module_name -d db`
4. Browser cache cleared

### Template Changes Not Visible

**Solution:**
```bash
# Clear assets
rm -rf ~/.local/share/Odoo/filestore/db_name/assets/*

# Restart with asset regeneration
./odoo-bin --dev=all -d db_name
```

### Import Errors

**Common fixes:**
```javascript
// Correct imports for v17.0
import { Component } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";
```

### Field Not Available in POS

**Add to loader:**
```python
def _loader_params_MODEL_NAME(self):
    result = super()._loader_params_MODEL_NAME()
    result['search_params']['fields'].append('your_field')
    return result
```

---

## Conclusion

This Odoo 17.0 guide provides complete, working examples for all common POS customizations. The instant-ERP debranding proposal demonstrates a real-world implementation following best practices.

**Remember:**
- Always use inheritance
- Test in development first
- Keep customizations modular
- Document your code
- Plan for future upgrades

For general concepts, see [00-pos-customization-proposal.md](./00-pos-customization-proposal.md).

---

**Last Updated:** 2025-11-16
**Odoo Version:** 17.0

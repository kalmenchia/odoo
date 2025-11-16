# Odoo Point of Sale (POS) Customization Guide & Proposal

**Document Version:** 1.0
**Odoo Version:** 17.0
**Last Updated:** 2025-11-16

---

## Table of Contents

1. [Introduction](#introduction)
2. [POS Architecture Overview](#pos-architecture-overview)
3. [Customization Fundamentals](#customization-fundamentals)
4. [Developer Guide: How to Customize Odoo POS](#developer-guide-how-to-customize-odoo-pos)
   - [Module Structure](#module-structure)
   - [Inheriting and Extending Components](#inheriting-and-extending-components)
   - [Layout Customization](#layout-customization)
   - [Adding Functions and Business Logic](#adding-functions-and-business-logic)
   - [Adding Custom Fields](#adding-custom-fields)
   - [Modifying Keypads/Numpads](#modifying-keypads-numpads)
   - [Payment Collection Customization](#payment-collection-customization)
   - [Receipt Template Customization](#receipt-template-customization)
5. [Version-Specific Guides](#version-specific-guides)
   - [Odoo 17.0](#odoo-170)
   - [Odoo 16.0](#odoo-160)
   - [Odoo 15.0](#odoo-150)
6. [Proposed Customization: Debranding for instant-ERP](#proposed-customization-debranding-for-instant-erp)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Introduction

This document provides a comprehensive guide for developers to customize the Odoo Point of Sale (POS) system. The guide emphasizes the use of **inheritance** and **modular customization** to ensure that customizations remain compatible with future Odoo upgrades.

### Key Principles

- **Never modify core Odoo files** - Always use inheritance
- **Create custom modules** - Keep customizations isolated and maintainable
- **Follow Odoo conventions** - Ensure compatibility and easier maintenance
- **Version awareness** - Different Odoo versions may require different approaches

---

## POS Architecture Overview

### Directory Structure

The Odoo POS module (`addons/point_of_sale/`) is structured as follows:

```
point_of_sale/
├── __manifest__.py           # Module manifest
├── controllers/              # HTTP controllers
├── data/                     # Data files
├── models/                   # Python models (backend)
│   ├── pos_config.py        # POS configuration
│   ├── pos_session.py       # POS session management
│   ├── pos_order.py         # Order management
│   ├── pos_payment.py       # Payment processing
│   └── ...
├── static/
│   └── src/
│       ├── app/             # POS Application (Frontend)
│       │   ├── navbar/      # Navigation bar components
│       │   ├── screens/     # Screen components
│       │   │   ├── product_screen/
│       │   │   ├── payment_screen/
│       │   │   ├── receipt_screen/
│       │   │   └── ...
│       │   ├── generic_components/  # Reusable components
│       │   │   ├── numpad/
│       │   │   └── ...
│       │   ├── store/       # State management
│       │   └── main.js      # Application entry point
│       └── scss/            # Styles
├── views/                   # Backend views (XML)
└── wizard/                  # Wizard views
```

### Technology Stack

- **Backend:** Python (Odoo ORM)
- **Frontend:** OWL (Odoo Web Library) - Component-based framework
- **Templates:** QWeb (XML-based templating)
- **Styling:** SCSS/CSS
- **State Management:** Reactive stores

### Key Components

1. **Models (Backend):**
   - `pos.config` - POS configuration settings
   - `pos.session` - Session management
   - `pos.order` - Order processing
   - `pos.payment` - Payment handling

2. **Frontend Components:**
   - `Navbar` - Top navigation bar (includes logo)
   - `ProductScreen` - Product selection
   - `PaymentScreen` - Payment processing
   - `ReceiptScreen` - Receipt display and printing
   - `Numpad` - Numeric input component

---

## Customization Fundamentals

### The Inheritance Pattern

Odoo uses inheritance to customize existing modules. There are three types:

1. **Class Inheritance** (Python): Extend existing models
2. **Template Inheritance** (XML): Extend or modify views
3. **Component Inheritance** (JavaScript/OWL): Extend frontend components

### Creating a Custom Module

Always create a separate module for customizations. Here's a minimal structure:

```
custom_pos_branding/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── pos_config.py
├── static/
│   └── src/
│       ├── app/
│       │   └── overrides/
│       │       ├── navbar.js
│       │       └── navbar.xml
│       └── scss/
│           └── custom_styles.scss
└── views/
    └── templates.xml
```

---

## Developer Guide: How to Customize Odoo POS

### Module Structure

#### 1. Create `__manifest__.py`

```python
# -*- coding: utf-8 -*-
{
    'name': 'Custom POS Branding',
    'version': '17.0.1.0.0',
    'category': 'Sales/Point of Sale',
    'summary': 'Custom branding for POS',
    'description': """
        This module customizes the POS interface:
        - Custom logo
        - Custom receipt templates
        - Custom branding
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': ['point_of_sale'],
    'data': [
        'views/templates.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'custom_pos_branding/static/src/app/overrides/**/*',
            'custom_pos_branding/static/src/scss/**/*',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
```

#### 2. Create `__init__.py`

```python
# -*- coding: utf-8 -*-
from . import models
```

---

### Inheriting and Extending Components

#### Extending Python Models

**Example: Add custom fields to `pos.config`**

File: `models/pos_config.py`

```python
# -*- coding: utf-8 -*-
from odoo import fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    # Add custom fields
    custom_logo = fields.Binary(
        string='Custom POS Logo',
        help='Custom logo to display in POS interface'
    )
    custom_footer_text = fields.Text(
        string='Custom Receipt Footer',
        help='Custom text to display on receipts'
    )
    enable_custom_branding = fields.Boolean(
        string='Enable Custom Branding',
        default=True
    )

    # Override existing methods
    def _get_custom_logo_url(self):
        """Return custom logo URL if available"""
        self.ensure_one()
        if self.custom_logo:
            return f'/web/image?model=pos.config&id={self.id}&field=custom_logo'
        return '/web/static/img/logo.png'
```

#### Extending JavaScript/OWL Components

**Example: Customize the Navbar component**

File: `static/src/app/overrides/navbar.js`

```javascript
/** @odoo-module */

import { Navbar } from "@point_of_sale/app/navbar/navbar";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";

// Patch the Navbar component to use custom logo
patch(Navbar.prototype, {
    setup() {
        super.setup(...arguments);
        this.pos = usePos();
    },

    get customLogoUrl() {
        // Get custom logo from config
        if (this.pos.config.custom_logo) {
            return `/web/image?model=pos.config&id=${this.pos.config.id}&field=custom_logo`;
        }
        return '/web/static/img/logo.png';
    },

    onLogoClick() {
        // Custom behavior when logo is clicked
        console.log('Custom logo clicked!');
        // You can add custom functionality here
    }
});
```

**Example: Override Navbar template**

File: `static/src/app/overrides/navbar.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates id="template" xml:space="preserve">

    <!-- Inherit and modify the navbar template -->
    <t t-inherit="point_of_sale.Navbar" t-inherit-mode="extension">
        <!-- Replace the logo -->
        <xpath expr="//img[@class='pos-logo h-75 ms-3 me-auto align-self-center']" position="replace">
            <img class="pos-logo h-75 ms-3 me-auto align-self-center"
                 t-att-src="customLogoUrl"
                 t-on-click="onLogoClick"
                 alt="Custom Logo" />
        </xpath>
    </t>

</templates>
```

---

### Layout Customization

#### Customizing Screen Layouts

**Example: Modify Payment Screen Layout**

File: `static/src/app/overrides/payment_screen.js`

```javascript
/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {
    // Add custom properties
    setup() {
        super.setup(...arguments);
        this.customMessage = "Thank you for your purchase!";
    },

    // Add custom methods
    showCustomNotification() {
        this.notification.add(this.customMessage, {
            type: 'success',
            duration: 3000
        });
    },

    // Override existing methods
    async validateOrder(isForceValidate) {
        // Add custom logic before validation
        this.showCustomNotification();

        // Call the original method
        return super.validateOrder(...arguments);
    }
});
```

#### Custom Styling

File: `static/src/scss/custom_pos_styles.scss`

```scss
// Custom POS Styles

// Customize navbar
.pos-topheader {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;

    .pos-logo {
        height: 60px !important;
        padding: 5px;
        background: white;
        border-radius: 8px;
    }
}

// Customize buttons
.payment-screen {
    .btn-primary {
        background-color: #667eea;
        border-color: #667eea;

        &:hover {
            background-color: #764ba2;
            border-color: #764ba2;
        }
    }
}

// Customize product cards
.product-list {
    .product {
        border: 2px solid #667eea;
        border-radius: 10px;
        transition: all 0.3s ease;

        &:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
    }
}

// Custom receipt styling
.pos-receipt {
    font-family: 'Courier New', monospace;

    .pos-receipt-logo {
        max-width: 200px;
        margin: 0 auto;
        display: block;
    }
}
```

---

### Adding Functions and Business Logic

#### Adding Custom Business Logic to Models

**Example: Add custom validation to orders**

File: `models/pos_order.py`

```python
# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class PosOrder(models.Model):
    _inherit = 'pos.order'

    # Add custom fields
    custom_reference = fields.Char(
        string='Custom Reference',
        help='Custom order reference number'
    )
    loyalty_points_earned = fields.Integer(
        string='Loyalty Points',
        compute='_compute_loyalty_points',
        store=True
    )

    @api.depends('amount_total')
    def _compute_loyalty_points(self):
        """Calculate loyalty points based on order total"""
        for order in self:
            # 1 point for every $10 spent
            order.loyalty_points_earned = int(order.amount_total / 10)

    @api.constrains('amount_total')
    def _check_order_limit(self):
        """Validate order doesn't exceed limit"""
        for order in self:
            if order.amount_total > 10000:
                raise ValidationError(_(
                    'Order total cannot exceed $10,000. '
                    'Please split into multiple orders.'
                ))

    def _prepare_invoice_vals(self):
        """Override to add custom fields to invoice"""
        vals = super()._prepare_invoice_vals()
        # Add custom reference to invoice
        vals['ref'] = self.custom_reference or vals.get('ref')
        return vals
```

#### Adding Custom JavaScript Services

File: `static/src/app/services/custom_service.js`

```javascript
/** @odoo-module */

import { registry } from "@web/core/registry";

export const customPosService = {
    dependencies: ["pos", "orm"],

    start(env, { pos, orm }) {
        return {
            /**
             * Custom service method to validate customer
             */
            async validateCustomer(partner) {
                if (!partner) {
                    return false;
                }

                // Add custom validation logic
                if (partner.credit_limit && partner.credit > partner.credit_limit) {
                    env.services.popup.add('ErrorPopup', {
                        title: 'Credit Limit Exceeded',
                        body: `Customer has exceeded their credit limit.`
                    });
                    return false;
                }

                return true;
            },

            /**
             * Calculate custom discount
             */
            calculateVIPDiscount(order) {
                const partner = order.get_partner();
                if (partner && partner.is_vip) {
                    return order.get_total_without_tax() * 0.1; // 10% discount
                }
                return 0;
            },

            /**
             * Send order to external system
             */
            async syncToExternalSystem(order) {
                try {
                    await orm.call('pos.order', 'sync_to_external', [order.id]);
                    return true;
                } catch (error) {
                    console.error('Failed to sync order:', error);
                    return false;
                }
            }
        };
    }
};

registry.category("services").add("custom_pos", customPosService);
```

---

### Adding Custom Fields

#### Backend: Add fields to POS models

**Example: Add customer type field**

File: `models/res_partner.py`

```python
# -*- coding: utf-8 -*-
from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_type = fields.Selection([
        ('regular', 'Regular'),
        ('vip', 'VIP'),
        ('wholesale', 'Wholesale'),
    ], string='Customer Type', default='regular')

    credit_limit = fields.Float(
        string='Credit Limit',
        help='Maximum credit allowed for this customer'
    )

    is_vip = fields.Boolean(
        string='VIP Customer',
        compute='_compute_is_vip',
        store=True
    )

    @fields.depends('customer_type')
    def _compute_is_vip(self):
        for partner in self:
            partner.is_vip = partner.customer_type == 'vip'
```

#### Frontend: Display custom fields in POS

File: `static/src/app/overrides/partner_line.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates id="template" xml:space="preserve">

    <!-- Add custom fields to partner display -->
    <t t-inherit="point_of_sale.PartnerLine" t-inherit-mode="extension">
        <xpath expr="//div[@class='partner-name']" position="after">
            <div t-if="props.partner.customer_type" class="customer-type-badge">
                <span t-if="props.partner.customer_type === 'vip'"
                      class="badge bg-warning">VIP</span>
                <span t-elif="props.partner.customer_type === 'wholesale'"
                      class="badge bg-info">Wholesale</span>
            </div>
        </xpath>
    </t>

</templates>
```

#### Making fields available to POS

File: `models/pos_session.py`

```python
# -*- coding: utf-8 -*-
from odoo import models

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_res_partner(self):
        """Add custom fields to partner data loaded in POS"""
        result = super()._loader_params_res_partner()
        # Add custom fields to the list
        result['search_params']['fields'].extend([
            'customer_type',
            'credit_limit',
            'is_vip'
        ])
        return result
```

---

### Modifying Keypads (Numpads)

#### Customizing Numpad Buttons

**Example: Add custom buttons to numpad**

File: `static/src/app/overrides/payment_screen.js`

```javascript
/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {
    /**
     * Override to add custom numpad buttons
     */
    getNumpadButtons() {
        const buttons = super.getNumpadButtons(...arguments);

        // Add custom quick amount buttons
        return [
            ...buttons,
            { text: '$5', value: 'custom_5', class: 'btn-info' },
            { text: '$10', value: 'custom_10', class: 'btn-info' },
            { text: '$20', value: 'custom_20', class: 'btn-info' },
            { text: '$50', value: 'custom_50', class: 'btn-info' },
        ];
    },

    /**
     * Handle custom numpad button clicks
     */
    _onNumpadClick(buttonValue) {
        // Handle custom buttons
        if (buttonValue.startsWith('custom_')) {
            const amount = parseFloat(buttonValue.split('_')[1]);
            const order = this.currentOrder;
            const selectedPaymentLine = order.selected_paymentline;

            if (selectedPaymentLine) {
                selectedPaymentLine.set_amount(amount);
            }
            return;
        }

        // Call original method for standard buttons
        super._onNumpadClick(...arguments);
    }
});
```

#### Creating Custom Numpad Component

File: `static/src/app/components/custom_numpad/custom_numpad.js`

```javascript
/** @odoo-module */

import { Component } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";

export class CustomNumpad extends Component {
    static template = "custom_pos_branding.CustomNumpad";
    static props = {
        onClick: Function,
        class: { type: String, optional: true },
    };

    setup() {
        this.pos = usePos();
    }

    get buttons() {
        return [
            { value: '1', text: '1' },
            { value: '2', text: '2' },
            { value: '3', text: '3' },
            { value: '4', text: '4' },
            { value: '5', text: '5' },
            { value: '6', text: '6' },
            { value: '7', text: '7' },
            { value: '8', text: '8' },
            { value: '9', text: '9' },
            { value: '.', text: '.' },
            { value: '0', text: '0' },
            { value: 'Backspace', text: '⌫', class: 'btn-danger' },
            { value: '+10', text: '+10', class: 'btn-success' },
            { value: '+20', text: '+20', class: 'btn-success' },
            { value: '+50', text: '+50', class: 'btn-success' },
            { value: 'clear', text: 'C', class: 'btn-warning' },
        ];
    }

    onClick(buttonValue) {
        this.props.onClick(buttonValue);
    }
}
```

File: `static/src/app/components/custom_numpad/custom_numpad.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates id="template" xml:space="preserve">

    <t t-name="custom_pos_branding.CustomNumpad">
        <div t-attf-class="custom-numpad {{ props.class || '' }}">
            <div class="numpad-grid">
                <button t-foreach="buttons" t-as="button" t-key="button.value"
                    t-attf-class="numpad-button btn {{ button.class || 'btn-light' }}"
                    t-on-click="() => this.onClick(button.value)">
                    <t t-esc="button.text" />
                </button>
            </div>
        </div>
    </t>

</templates>
```

---

### Payment Collection Customization

#### Adding Custom Payment Methods

**Example: Add custom payment method logic**

File: `models/pos_payment_method.py`

```python
# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    payment_type = fields.Selection(
        selection_add=[
            ('loyalty_points', 'Loyalty Points'),
            ('gift_card', 'Gift Card'),
        ],
        ondelete={
            'loyalty_points': 'set default',
            'gift_card': 'set default'
        }
    )

    requires_validation = fields.Boolean(
        string='Requires Validation',
        help='If true, payment requires manager validation'
    )
```

#### Custom Payment Processing

File: `static/src/app/overrides/payment_screen.js`

```javascript
/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {
    /**
     * Add custom payment method
     */
    async addNewPaymentLine(paymentMethod) {
        // Custom validation for specific payment methods
        if (paymentMethod.payment_type === 'loyalty_points') {
            return await this.handleLoyaltyPayment(paymentMethod);
        }

        if (paymentMethod.payment_type === 'gift_card') {
            return await this.handleGiftCardPayment(paymentMethod);
        }

        // Call original method for standard payments
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
                body: 'Please select a customer to use loyalty points.'
            });
            return;
        }

        // Get loyalty points balance
        const loyaltyBalance = await this.orm.call(
            'res.partner',
            'get_loyalty_balance',
            [partner.id]
        );

        // Show popup to enter points to use
        const { confirmed, payload } = await this.popup.add('NumberPopup', {
            title: `Loyalty Points (Available: ${loyaltyBalance})`,
            startingValue: 0,
        });

        if (confirmed && payload > 0) {
            if (payload > loyaltyBalance) {
                await this.popup.add('ErrorPopup', {
                    title: 'Insufficient Points',
                    body: `Customer only has ${loyaltyBalance} points available.`
                });
                return;
            }

            // Add payment line with points value
            // Assuming 1 point = $0.01
            const amount = payload * 0.01;
            const paymentLine = await super.addNewPaymentLine(paymentMethod);
            paymentLine.set_amount(amount);
            paymentLine.loyalty_points = payload;
        }
    },

    /**
     * Handle gift card payment
     */
    async handleGiftCardPayment(paymentMethod) {
        const { confirmed, payload: cardNumber } = await this.popup.add('TextInputPopup', {
            title: 'Gift Card',
            startingValue: '',
            placeholder: 'Enter gift card number...'
        });

        if (confirmed && cardNumber) {
            try {
                // Validate gift card
                const cardData = await this.orm.call(
                    'gift.card',
                    'validate_card',
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
                const amountToUse = Math.min(
                    cardData.balance,
                    this.currentOrder.get_due()
                );
                paymentLine.set_amount(amountToUse);
                paymentLine.gift_card_number = cardNumber;

            } catch (error) {
                await this.popup.add('ErrorPopup', {
                    title: 'Error',
                    body: 'Failed to validate gift card. Please try again.'
                });
            }
        }
    },

    /**
     * Override validation to handle custom payments
     */
    async validateOrder(isForceValidate) {
        const order = this.currentOrder;

        // Check for payments requiring validation
        const requiresValidation = order.paymentlines.some(
            line => line.payment_method.requires_validation
        );

        if (requiresValidation && !this.pos.get_cashier().role === 'manager') {
            const { confirmed } = await this.popup.add('NumberPopup', {
                title: 'Manager Approval Required',
                startingValue: '',
                placeholder: 'Enter manager PIN...',
                isPassword: true
            });

            if (!confirmed) {
                return;
            }
        }

        return super.validateOrder(...arguments);
    }
});
```

---

### Receipt Template Customization

#### Customizing Receipt Header

File: `static/src/app/overrides/receipt_header.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates id="template" xml:space="preserve">

    <!-- Override receipt header -->
    <t t-inherit="point_of_sale.ReceiptHeader" t-inherit-mode="extension">

        <!-- Replace company logo with custom logo -->
        <xpath expr="//img[@class='pos-receipt-logo']" position="replace">
            <img t-if="props.data.company.custom_logo"
                 t-attf-src="/web/image?model=res.company&amp;id={{props.data.company.id}}&amp;field=custom_logo"
                 alt="Logo"
                 class="pos-receipt-logo"/>
            <img t-else=""
                 t-attf-src="/web/image?model=res.company&amp;id={{props.data.company.id}}&amp;field=logo"
                 alt="Logo"
                 class="pos-receipt-logo"/>
        </xpath>

        <!-- Add custom header text -->
        <xpath expr="//div[@class='pos-receipt-contact']" position="before">
            <div class="custom-receipt-header text-center">
                <h2>Welcome to instant-ERP</h2>
                <p>Thank you for your business!</p>
            </div>
        </xpath>

    </t>

</templates>
```

#### Customizing Receipt Footer

File: `static/src/app/overrides/order_receipt.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates id="template" xml:space="preserve">

    <!-- Override receipt footer -->
    <t t-inherit="point_of_sale.OrderReceipt" t-inherit-mode="extension">

        <!-- Remove "Powered by Odoo" text -->
        <xpath expr="//div[@class='pos-receipt-order-data']/p[text()='Powered by Odoo']" position="replace">
            <p>Powered by instant-ERP</p>
        </xpath>

        <!-- Add custom footer content -->
        <xpath expr="//div[@class='pos-receipt-order-data']" position="before">
            <div class="custom-receipt-footer text-center">
                <t t-if="props.data.loyalty_points">
                    <div class="loyalty-info">
                        <strong>Loyalty Points Earned: </strong>
                        <span t-esc="props.data.loyalty_points"/>
                    </div>
                </t>
                <div class="follow-us mt-3">
                    <p>Follow us on social media!</p>
                    <p>@instantERP</p>
                </div>
            </div>
        </xpath>

    </t>

</templates>
```

#### Adding Custom Receipt Data

File: `models/pos_order.py`

```python
# -*- coding: utf-8 -*-
from odoo import models

class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _export_for_ui(self, order):
        """Add custom data to receipt"""
        result = super()._export_for_ui(order)

        # Add custom fields to receipt data
        result.update({
            'custom_reference': order.custom_reference,
            'loyalty_points': order.loyalty_points_earned,
            'custom_message': 'Thank you for shopping with instant-ERP!',
        })

        return result
```

---

## Version-Specific Guides

### Odoo 17.0

**Current Version - This Document**

Odoo 17.0 uses:
- **OWL Framework** (Odoo Web Library) for components
- **Reactive stores** for state management
- **Modern JavaScript** (ES6+ modules)
- **XML/QWeb templates**

Key Features:
- Component-based architecture
- Better performance with reactive state
- Improved modularity
- Enhanced inheritance patterns

**Asset Declaration (v17.0):**

```python
'assets': {
    'point_of_sale._assets_pos': [
        'custom_pos_branding/static/src/**/*',
    ],
}
```

**Component Inheritance (v17.0):**

```javascript
/** @odoo-module */
import { Component } from "@point_of_sale/app/component";
import { patch } from "@web/core/utils/patch";

patch(Component.prototype, {
    // Your customizations
});
```

---

### Odoo 16.0

**Differences from v17.0:**

Similar to 17.0 but with some API differences:

- Uses similar OWL framework
- State management slightly different
- Some component APIs may vary

**Migration Notes:**
- Most v16.0 customizations work in v17.0 with minor adjustments
- Check for deprecated methods
- Update asset paths if needed

---

### Odoo 15.0

**Differences from v17.0:**

Major architectural differences:

- Still uses **OWL framework** but earlier version
- Different component registration
- Some template syntax differences

**Asset Declaration (v15.0):**

```python
'assets': {
    'point_of_sale.assets': [  # Note: different bundle name
        'custom_pos_branding/static/src/js/**/*',
        'custom_pos_branding/static/src/xml/**/*',
    ],
}
```

**Component Extension (v15.0):**

Similar patterns but may require adjustments in import paths and some API calls.

---

## Proposed Customization: Debranding for instant-ERP

This section outlines the specific customizations needed to rebrand the Odoo POS to instant-ERP.

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
├── data/
│   └── company_data.xml
└── views/
    └── pos_config_views.xml
```

### 1. Manifest File

File: `__manifest__.py`

```python
# -*- coding: utf-8 -*-
{
    'name': 'instant-ERP POS Branding',
    'version': '17.0.1.0.0',
    'category': 'Sales/Point of Sale',
    'summary': 'Rebrand Odoo POS to instant-ERP',
    'description': """
        instant-ERP POS Branding
        =========================

        This module customizes the Odoo POS interface with instant-ERP branding:

        - Replaces Odoo logo with instant-ERP logo in POS navbar
        - Removes "Powered by Odoo" from receipts
        - Adds instant-ERP branding to all receipts
        - Custom colors and styling
        - Does not modify core Odoo files (uses inheritance only)
    """,
    'author': 'instant-ERP Team',
    'website': 'https://www.instant-erp.com',
    'license': 'LGPL-3',
    'depends': [
        'point_of_sale',
    ],
    'data': [
        'views/pos_config_views.xml',
        'data/company_data.xml',
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

### 2. Replace POS Navbar Logo

File: `static/src/app/overrides/navbar.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates id="template" xml:space="preserve">

    <!-- Replace Odoo logo with instant-ERP logo -->
    <t t-inherit="point_of_sale.Navbar" t-inherit-mode="extension">
        <xpath expr="//img[@class='pos-logo h-75 ms-3 me-auto align-self-center']" position="replace">
            <img class="pos-logo h-75 ms-3 me-auto align-self-center instant-erp-logo"
                 src="/instant_erp_pos_branding/static/src/img/instant_erp_logo.png"
                 alt="instant-ERP" />
        </xpath>
    </t>

</templates>
```

### 3. Remove Odoo Branding from Receipts

File: `static/src/app/overrides/order_receipt.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates id="template" xml:space="preserve">

    <!-- Remove "Powered by Odoo" and add instant-ERP branding -->
    <t t-inherit="point_of_sale.OrderReceipt" t-inherit-mode="extension">

        <!-- Remove "Powered by Odoo" text -->
        <xpath expr="//div[@class='pos-receipt-order-data']/p[text()='Powered by Odoo']" position="replace">
            <p class="instant-erp-branding">Powered by instant-ERP</p>
        </xpath>

        <!-- Optionally add instant-ERP URL -->
        <xpath expr="//div[@class='pos-receipt-order-data']" position="inside">
            <div class="instant-erp-footer text-center mt-2">
                <small>www.instant-erp.com</small>
            </div>
        </xpath>

    </t>

</templates>
```

### 4. Customize Receipt Header

File: `static/src/app/overrides/receipt_header.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates id="template" xml:space="preserve">

    <!-- Customize receipt header with instant-ERP branding -->
    <t t-inherit="point_of_sale.ReceiptHeader" t-inherit-mode="extension">

        <!-- Add instant-ERP watermark or header -->
        <xpath expr="//div[@class='pos-receipt-contact']" position="before">
            <div class="instant-erp-receipt-header text-center mb-3">
                <img src="/instant_erp_pos_branding/static/src/img/instant_erp_receipt_logo.png"
                     alt="instant-ERP"
                     class="instant-erp-receipt-logo"
                     style="max-width: 150px; margin: 0 auto;"/>
            </div>
        </xpath>

    </t>

</templates>
```

### 5. Custom Styling

File: `static/src/scss/instant_erp_branding.scss`

```scss
// instant-ERP POS Branding Styles

// Brand colors
$instant-erp-primary: #2563eb;    // Blue
$instant-erp-secondary: #7c3aed;  // Purple
$instant-erp-accent: #f59e0b;     // Orange

// Navbar customization
.pos-topheader {
    .instant-erp-logo {
        height: 50px !important;
        width: auto;
        object-fit: contain;
    }
}

// Receipt customization
.pos-receipt {
    .instant-erp-receipt-header {
        border-bottom: 2px solid $instant-erp-primary;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }

    .instant-erp-receipt-logo {
        display: block;
        margin: 0 auto 10px;
    }

    .instant-erp-branding {
        color: $instant-erp-primary;
        font-weight: bold;
        font-size: 14px;
    }

    .instant-erp-footer {
        color: $instant-erp-secondary;
        font-size: 12px;
        margin-top: 10px;
    }
}

// Button customization (optional)
.pos-content {
    .btn-primary {
        background-color: $instant-erp-primary;
        border-color: $instant-erp-primary;

        &:hover {
            background-color: darken($instant-erp-primary, 10%);
            border-color: darken($instant-erp-primary, 10%);
        }
    }

    .btn-secondary {
        background-color: $instant-erp-secondary;
        border-color: $instant-erp-secondary;

        &:hover {
            background-color: darken($instant-erp-secondary, 10%);
            border-color: darken($instant-erp-secondary, 10%);
        }
    }
}

// Optional: Customize product screen
.product-screen {
    .product-list {
        .product {
            &:hover {
                border-color: $instant-erp-primary;
            }

            &.selected {
                border-color: $instant-erp-primary;
                background-color: rgba($instant-erp-primary, 0.1);
            }
        }
    }
}
```

### 6. Backend Configuration View (Optional)

File: `views/pos_config_views.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_pos_config_form_instant_erp" model="ir.ui.view">
        <field name="name">pos.config.form.instant_erp</field>
        <field name="model">pos.config</field>
        <field name="inherit_id" ref="point_of_sale.pos_config_view_form"/>
        <field name="arch" type="xml">
            <xpath expr="//group[@name='loyalty']" position="after">
                <group string="instant-ERP Branding" name="instant_erp_branding">
                    <field name="enable_instant_erp_branding"/>
                    <field name="instant_erp_custom_receipt_text"
                           widget="text"
                           attrs="{'invisible': [('enable_instant_erp_branding', '=', False)]}"/>
                </group>
            </xpath>
        </field>
    </record>
</odoo>
```

File: `models/pos_config.py`

```python
# -*- coding: utf-8 -*-
from odoo import fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    enable_instant_erp_branding = fields.Boolean(
        string='Enable instant-ERP Branding',
        default=True,
        help='Enable instant-ERP custom branding in POS'
    )

    instant_erp_custom_receipt_text = fields.Text(
        string='Custom Receipt Message',
        default='Thank you for shopping with instant-ERP!',
        help='Custom message to display on receipts'
    )
```

### 7. Advanced: Dynamic Logo from Company Settings

File: `models/res_company.py`

```python
# -*- coding: utf-8 -*-
from odoo import fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    instant_erp_pos_logo = fields.Binary(
        string='instant-ERP POS Logo',
        help='Custom logo for POS interface (instant-ERP branding)'
    )

    instant_erp_receipt_logo = fields.Binary(
        string='instant-ERP Receipt Logo',
        help='Custom logo for receipt printouts (instant-ERP branding)'
    )
```

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

    get instantErpLogoUrl() {
        // Use company custom logo if available, otherwise use default
        const company = this.pos.company;
        if (company.instant_erp_pos_logo) {
            return `/web/image?model=res.company&id=${company.id}&field=instant_erp_pos_logo`;
        }
        return '/instant_erp_pos_branding/static/src/img/instant_erp_logo.png';
    }
});
```

Update `navbar.xml` to use the dynamic logo:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates id="template" xml:space="preserve">

    <t t-inherit="point_of_sale.Navbar" t-inherit-mode="extension">
        <xpath expr="//img[@class='pos-logo h-75 ms-3 me-auto align-self-center']" position="replace">
            <img class="pos-logo h-75 ms-3 me-auto align-self-center instant-erp-logo"
                 t-att-src="instantErpLogoUrl"
                 alt="instant-ERP" />
        </xpath>
    </t>

</templates>
```

### 8. Installation Instructions

1. **Copy the module** to your Odoo addons directory:
   ```bash
   cp -r instant_erp_pos_branding /path/to/odoo/addons/
   ```

2. **Update the addons list:**
   - Go to Apps menu
   - Click "Update Apps List"

3. **Install the module:**
   - Search for "instant-ERP POS Branding"
   - Click Install

4. **Configure (Optional):**
   - Go to Point of Sale > Configuration > Point of Sale
   - Open your POS configuration
   - Navigate to "instant-ERP Branding" section
   - Customize settings as needed

5. **Add custom logos:**
   - Go to Settings > Companies
   - Upload instant-ERP logos to the company record
   - Or place logo files in `static/src/img/` directory

### 9. Testing Checklist

- [ ] POS navbar shows instant-ERP logo instead of Odoo logo
- [ ] Receipt header displays instant-ERP branding
- [ ] "Powered by Odoo" replaced with "Powered by instant-ERP"
- [ ] Custom colors applied (if configured)
- [ ] Receipt prints correctly with new branding
- [ ] No references to "Odoo" visible in POS interface
- [ ] Module can be installed/uninstalled without errors
- [ ] Original Odoo files remain unchanged

---

## Best Practices

### 1. Always Use Inheritance

✅ **Do:**
```python
class PosOrder(models.Model):
    _inherit = 'pos.order'
    # Your customizations
```

❌ **Don't:**
```python
# Don't modify core files directly
# /addons/point_of_sale/models/pos_order.py
```

### 2. Use Proper Module Dependencies

```python
'depends': ['point_of_sale'],
```

Ensure your module depends on all modules it inherits from.

### 3. Use XPath for Template Modifications

```xml
<xpath expr="//element" position="replace|after|before|inside|attributes">
    <!-- Your content -->
</xpath>
```

### 4. Keep Customizations Modular

Create separate files for different concerns:
- `models/` for Python logic
- `static/src/app/` for JavaScript components
- `views/` for backend views
- `data/` for default data

### 5. Use Version-Specific Code Carefully

```python
import odoo
from odoo.release import version_info

if version_info[0] >= 17:
    # v17+ specific code
else:
    # v16 and below code
```

### 6. Test in Development First

- Always test customizations in a development environment
- Create backups before deploying to production
- Test upgrades with custom modules installed

### 7. Document Your Code

```python
def custom_method(self):
    """
    Brief description of what this method does.

    :return: Description of return value
    :rtype: type
    """
    pass
```

### 8. Handle Errors Gracefully

```javascript
try {
    await this.orm.call('model', 'method', [args]);
} catch (error) {
    console.error('Error:', error);
    await this.popup.add('ErrorPopup', {
        title: 'Error',
        body: 'Something went wrong. Please try again.'
    });
}
```

---

## Troubleshooting

### Issue: Changes Not Visible After Module Update

**Solution:**
1. Clear browser cache (Ctrl+Shift+R)
2. Restart Odoo server
3. Update module:
   ```bash
   ./odoo-bin -u custom_pos_branding -d database_name
   ```
4. Check browser console for JavaScript errors

### Issue: Logo Not Displaying

**Solution:**
1. Verify image path is correct
2. Check file permissions
3. Clear browser cache
4. Verify image is in correct format (PNG, JPG)
5. Check network tab in browser dev tools

### Issue: Receipt Template Not Updating

**Solution:**
1. Clear POS cache: Settings > Point of Sale > POS Config > "Clear POS Cache"
2. Close and reopen POS session
3. Check for XML syntax errors in logs

### Issue: JavaScript Errors in Console

**Solution:**
1. Check import paths are correct
2. Verify component names match
3. Check for typos in method names
4. Review Odoo logs: `/var/log/odoo/odoo-server.log`

### Issue: Module Won't Install

**Solution:**
1. Check `__manifest__.py` syntax
2. Verify all dependencies are installed
3. Check Odoo logs for specific errors
4. Ensure module is in correct addons path

### Issue: Custom Fields Not Showing in POS

**Solution:**
1. Add fields to `_loader_params` method
2. Restart POS session
3. Check field permissions
4. Verify field is in correct model

---

## Additional Resources

### Official Documentation

- [Odoo Documentation](https://www.odoo.com/documentation/17.0/)
- [OWL Framework Guide](https://github.com/odoo/owl)
- [POS Module Source Code](https://github.com/odoo/odoo/tree/17.0/addons/point_of_sale)

### Community Resources

- [Odoo Community Forums](https://www.odoo.com/forum)
- [Odoo GitHub Repository](https://github.com/odoo/odoo)
- [OCA (Odoo Community Association)](https://odoo-community.org/)

### Development Tools

- **Browser DevTools** - Inspect elements, debug JavaScript
- **Odoo Shell** - Test Python code: `./odoo-bin shell -d database_name`
- **Developer Mode** - Enable in Settings for additional options
- **Debug Mode** - Add `?debug=1` to URL for frontend debugging

---

## Conclusion

This guide provides comprehensive instructions for customizing the Odoo Point of Sale system using inheritance patterns that preserve compatibility with future updates. The proposed instant-ERP debranding customizations demonstrate these principles in practice, showing how to:

1. Replace branding elements (logos, text)
2. Customize templates without modifying core files
3. Add custom styling and behavior
4. Maintain upgrade compatibility

By following these patterns and best practices, developers can create robust, maintainable POS customizations that will continue to work across Odoo version upgrades.

---

**Document End**

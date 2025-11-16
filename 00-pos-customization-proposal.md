# Odoo Point of Sale (POS) Customization - Overview & Analysis

**Document Version:** 1.0
**Last Updated:** 2025-11-16
**Applies to:** All Odoo Versions (General Overview)

---

## Table of Contents

1. [Introduction](#introduction)
2. [Document Structure](#document-structure)
3. [POS Architecture Overview](#pos-architecture-overview)
4. [Customization Fundamentals](#customization-fundamentals)
5. [Version Comparison Matrix](#version-comparison-matrix)
6. [General Best Practices](#general-best-practices)
7. [Common Troubleshooting](#common-troubleshooting)
8. [Migration Guidelines](#migration-guidelines)

---

## Introduction

This document provides a **version-agnostic overview** of the Odoo Point of Sale (POS) system customization. It covers the fundamental concepts, architecture, and best practices that apply across all Odoo versions.

### Purpose

This documentation suite helps developers:
- Understand the POS architecture
- Learn inheritance-based customization patterns
- Maintain customizations across version upgrades
- Implement branding and functional customizations
- Follow industry best practices

### Key Principles

- **Never modify core Odoo files** - Always use inheritance
- **Create custom modules** - Keep customizations isolated and maintainable
- **Follow Odoo conventions** - Ensure compatibility and easier maintenance
- **Version awareness** - Different Odoo versions may require different approaches
- **Upgrade compatibility** - Design with future upgrades in mind

---

## Document Structure

This documentation is organized into version-specific guides:

```
Documentation Structure:
├── 00-pos-customization-proposal.md    # This file - General overview
├── 17-pos-customization-proposal.md    # Odoo 17.0 specific guide
├── 16-pos-customization-proposal.md    # Odoo 16.0 specific guide (TBD)
├── 15-pos-customization-proposal.md    # Odoo 15.0 specific guide (TBD)
└── 14-pos-customization-proposal.md    # Odoo 14.0 specific guide (TBD)
```

### How to Use This Documentation

1. **Start here (00-*)** - Read this document for general understanding
2. **Choose your version** - Go to your specific version guide (e.g., 17-*)
3. **Implement** - Follow version-specific code examples
4. **Test** - Verify in development environment
5. **Deploy** - Roll out to production

---

## POS Architecture Overview

### High-Level Architecture

The Odoo POS module is a hybrid application with:

```
┌─────────────────────────────────────────────────────┐
│                    POS System                        │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐         ┌──────────────┐         │
│  │   Frontend   │ ◄─────► │   Backend    │         │
│  │  (Browser)   │  HTTP   │  (Python)    │         │
│  └──────────────┘         └──────────────┘         │
│        │                         │                  │
│        │                         │                  │
│   ┌────▼─────┐            ┌─────▼──────┐          │
│   │ OWL/JS   │            │ Odoo ORM   │          │
│   │ QWeb     │            │ PostgreSQL │          │
│   └──────────┘            └────────────┘          │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Directory Structure (General Pattern)

All Odoo versions follow a similar structure:

```
point_of_sale/
├── __manifest__.py           # Module manifest
├── __init__.py
├── controllers/              # HTTP controllers
├── data/                     # Data files (XML)
├── models/                   # Python models (backend)
│   ├── pos_config.py        # POS configuration
│   ├── pos_session.py       # Session management
│   ├── pos_order.py         # Order management
│   ├── pos_payment.py       # Payment processing
│   └── ...
├── static/
│   └── src/
│       ├── app/             # Frontend application
│       ├── js/              # JavaScript files (varies by version)
│       ├── xml/             # QWeb templates (varies by version)
│       ├── css/             # Stylesheets
│       └── scss/            # SCSS files
├── views/                   # Backend views (XML)
├── report/                  # Report templates
├── security/                # Access rights
└── wizard/                  # Wizard views
```

### Technology Stack

#### Backend
- **Language:** Python 3.7+
- **Framework:** Odoo ORM
- **Database:** PostgreSQL
- **API:** RPC, HTTP Controllers

#### Frontend
- **Framework:**
  - v17.0: OWL (Odoo Web Library)
  - v16.0: OWL
  - v15.0: OWL
  - v14.0 and earlier: Backbone.js / Custom framework
- **Templating:** QWeb (XML-based)
- **Styling:** SCSS/CSS, Bootstrap
- **State Management:** Varies by version

### Core Components

#### 1. Backend Models

| Model | Purpose |
|-------|---------|
| `pos.config` | POS configuration and settings |
| `pos.session` | Session management (opening/closing) |
| `pos.order` | Order processing and storage |
| `pos.order.line` | Individual order items |
| `pos.payment` | Payment line records |
| `pos.payment.method` | Payment method configuration |
| `product.product` | Product catalog |
| `res.partner` | Customer information |

#### 2. Frontend Components

| Component | Purpose |
|-----------|---------|
| Navbar | Top navigation and menu |
| ProductScreen | Product selection interface |
| PaymentScreen | Payment processing |
| ReceiptScreen | Receipt display and printing |
| TicketScreen | Order history and retrieval |
| Numpad | Numeric input component |
| OrderWidget | Shopping cart display |

#### 3. Key Features

- **Offline Mode:** Works without constant internet connection
- **Session Management:** Opening/closing cash register sessions
- **Multi-payment:** Split payments across methods
- **Product Catalog:** Visual product selection
- **Receipt Printing:** Thermal and standard printers
- **Hardware Integration:** Barcode scanners, cash drawers, scales
- **Customer Management:** Customer selection and loyalty programs

---

## Customization Fundamentals

### The Inheritance Pattern

Odoo's power lies in its **inheritance system**. There are three types of inheritance:

#### 1. Class Inheritance (Python)

Extend existing models without modifying original code:

```python
class PosOrder(models.Model):
    _inherit = 'pos.order'  # Inherit from existing model

    # Add new fields
    custom_field = fields.Char('Custom Field')

    # Override existing methods
    def _export_for_ui(self, order):
        result = super()._export_for_ui(order)
        result['custom_field'] = order.custom_field
        return result
```

#### 2. Template Inheritance (XML/QWeb)

Modify views without changing original templates:

```xml
<t t-inherit="point_of_sale.OrderReceipt" t-inherit-mode="extension">
    <xpath expr="//div[@class='header']" position="after">
        <!-- Your custom content -->
    </xpath>
</t>
```

#### 3. Component Inheritance (JavaScript)

Extend frontend components using the patch mechanism:

```javascript
import { Component } from "@point_of_sale/...";
import { patch } from "@web/core/utils/patch";

patch(Component.prototype, {
    // Override or add methods
    customMethod() {
        // Your logic
    }
});
```

### Custom Module Structure

Always create a separate module for customizations:

```
custom_pos_module/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── [inherited_models].py
├── static/
│   └── src/
│       ├── app/ or js/
│       │   └── [components].js
│       ├── xml/ (v15 and below)
│       │   └── [templates].xml
│       └── scss/
│           └── [styles].scss
├── views/
│   └── [view_files].xml
├── data/
│   └── [data_files].xml
└── security/
    ├── ir.model.access.csv
    └── [security_rules].xml
```

### Module Manifest (`__manifest__.py`)

Essential elements:

```python
{
    'name': 'Custom POS Module',
    'version': 'X.0.1.0.0',  # X = Odoo version
    'category': 'Sales/Point of Sale',
    'depends': ['point_of_sale'],  # Required dependencies
    'data': [
        'security/ir.model.access.csv',
        'views/pos_views.xml',
    ],
    'assets': {
        # Asset loading (version-specific)
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
```

---

## Version Comparison Matrix

### Major Differences Across Versions

| Feature | v17.0 | v16.0 | v15.0 | v14.0 |
|---------|-------|-------|-------|-------|
| **Frontend Framework** | OWL | OWL | OWL | Backbone.js |
| **Asset Bundle** | `_assets_pos` | `_assets_pos` | `assets` | `assets` |
| **Component System** | OWL Components | OWL Components | OWL Components | Widget Classes |
| **State Management** | Reactive Stores | Reactive Stores | Reactive Stores | Model/Collection |
| **Template Format** | QWeb/XML | QWeb/XML | QWeb/XML | QWeb/XML |
| **Python Version** | 3.10+ | 3.8+ | 3.7+ | 3.7+ |
| **PostgreSQL** | 12+ | 10+ | 10+ | 10+ |

### Framework Evolution

```
v14.0 and earlier
    ↓
[Backbone.js Framework]
- Widget-based architecture
- jQuery dependencies
- Classic inheritance patterns
    ↓
v15.0
    ↓
[OWL Framework Introduction]
- Component-based architecture
- Reactive programming
- Modern JavaScript (ES6+)
    ↓
v16.0
    ↓
[OWL Refinement]
- Improved performance
- Better state management
- Enhanced developer experience
    ↓
v17.0
    ↓
[Latest OWL]
- Most refined OWL implementation
- Best practices established
- Optimized asset loading
```

### Migration Complexity

| Migration Path | Complexity | Notes |
|----------------|------------|-------|
| v17.0 → v17.x | Low | Minor version updates |
| v16.0 → v17.0 | Low-Medium | Similar architecture |
| v15.0 → v17.0 | Medium | Some API changes |
| v14.0 → v17.0 | High | Complete framework change |

---

## General Best Practices

### 1. Module Design

#### ✅ Do:
- Create focused, single-purpose modules
- Use clear, descriptive module names
- Document your code thoroughly
- Include version numbers in module version
- List all dependencies explicitly

#### ❌ Don't:
- Create monolithic modules doing everything
- Modify core Odoo files directly
- Skip documentation
- Forget to handle upgrade paths
- Ignore security implications

### 2. Code Organization

```python
# Good: Clear, documented, maintainable
class PosOrder(models.Model):
    """Extended POS Order with custom features."""
    _inherit = 'pos.order'

    custom_reference = fields.Char(
        string='Custom Reference',
        help='Internal reference for tracking'
    )

    def _prepare_invoice_vals(self):
        """Override to add custom reference to invoice."""
        vals = super()._prepare_invoice_vals()
        vals['ref'] = self.custom_reference or vals.get('ref')
        return vals
```

### 3. Performance Considerations

- **Minimize Database Queries:** Use `read()` and batch operations
- **Optimize Frontend:** Limit DOM manipulations
- **Cache Wisely:** Use Odoo's caching mechanisms
- **Lazy Load:** Don't load unnecessary data to POS
- **Test with Real Data:** Performance varies with data volume

### 4. Security Best Practices

```python
# Always check permissions
@api.model
def custom_method(self):
    self.check_access_rights('write')
    self.check_access_rule('write')
    # Your logic here
```

```xml
<!-- Define proper access rights -->
<record id="access_custom_model_user" model="ir.model.access">
    <field name="name">Custom Model Access</field>
    <field name="model_id" ref="model_custom_model"/>
    <field name="group_id" ref="point_of_sale.group_pos_user"/>
    <field name="perm_read" eval="1"/>
    <field name="perm_write" eval="1"/>
    <field name="perm_create" eval="1"/>
    <field name="perm_unlink" eval="0"/>
</record>
```

### 5. Testing Strategy

1. **Unit Tests:** Test Python methods in isolation
2. **Integration Tests:** Test model interactions
3. **Tour Tests:** Test frontend workflows
4. **Manual Tests:** Test with real hardware
5. **Upgrade Tests:** Test after version upgrades

### 6. Documentation Standards

```python
def complex_method(self, param1, param2):
    """
    Brief one-line description.

    Detailed explanation of what this method does,
    including any important behavior or side effects.

    :param param1: Description of param1
    :type param1: type
    :param param2: Description of param2
    :type param2: type
    :return: Description of return value
    :rtype: return_type
    :raises ExceptionType: When this exception is raised

    Example:
        >>> self.complex_method('value1', 42)
        'result'
    """
    pass
```

### 7. Version Control

- Use Git or similar VCS
- Create feature branches
- Write meaningful commit messages
- Tag releases properly
- Maintain CHANGELOG.md

### 8. Deployment Best Practices

1. **Development → Staging → Production**
2. Always backup before deploying
3. Test in staging environment
4. Plan deployment during low-traffic periods
5. Have rollback plan ready
6. Monitor logs after deployment

---

## Common Troubleshooting

### Issue Categories

#### 1. Module Installation Issues

**Symptoms:**
- Module won't install
- Dependency errors
- Import errors

**Solutions:**
```bash
# Check module syntax
python3 -m py_compile models/*.py

# Verify dependencies
grep depends __manifest__.py

# Check Odoo logs
tail -f /var/log/odoo/odoo-server.log

# Restart Odoo
sudo systemctl restart odoo

# Update module
./odoo-bin -u module_name -d database_name
```

#### 2. Frontend Issues

**Symptoms:**
- JavaScript errors
- Components not rendering
- Styles not applying

**Solutions:**
1. **Clear browser cache** (Ctrl+Shift+R)
2. **Check browser console** for errors
3. **Verify asset loading:**
   ```bash
   # Regenerate assets
   ./odoo-bin --dev=all
   ```
4. **Check asset manifest** in `__manifest__.py`
5. **Verify import paths** match your version

#### 3. Template Inheritance Issues

**Symptoms:**
- Templates not updating
- XPath not matching
- Content not appearing

**Solutions:**
```xml
<!-- Use precise XPath expressions -->
<xpath expr="//div[@class='exact-class-name']" position="after">
    <!-- Your content -->
</xpath>

<!-- Verify template exists -->
<xpath expr="//t[@t-name='template.name']" position="inside">
    <!-- Your content -->
</xpath>
```

#### 4. Python Inheritance Issues

**Symptoms:**
- Methods not being called
- Fields not appearing
- Override not working

**Solutions:**
```python
# Ensure _inherit is set correctly
class MyModel(models.Model):
    _inherit = 'pos.order'  # Not _name!

# Always call super() for overrides
def my_method(self):
    result = super().my_method()
    # Your additional logic
    return result

# Check model registration
from odoo import models
print(models.MetaModel._module_data_uninstall)
```

#### 5. Data Loading Issues

**Symptoms:**
- POS data not loading
- Fields missing in frontend
- Slow POS startup

**Solutions:**
```python
# Add fields to loader params
class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_res_partner(self):
        result = super()._loader_params_res_partner()
        result['search_params']['fields'].extend([
            'custom_field_1',
            'custom_field_2',
        ])
        return result
```

### Debug Mode Tools

#### Enable Debug Mode
- URL: Add `?debug=1`
- Settings → Activate Developer Mode

#### Useful Debug Commands

```bash
# Start Odoo in development mode
./odoo-bin --dev=all

# Shell access for testing
./odoo-bin shell -d database_name

# Run specific tests
./odoo-bin -d database_name -i module_name --test-enable --stop-after-init

# Check module dependencies
./odoo-bin -d database_name --modules=module_name
```

#### Browser DevTools

1. **Console:** Check for JavaScript errors
2. **Network:** Verify RPC calls and responses
3. **Elements:** Inspect DOM structure
4. **Sources:** Debug JavaScript with breakpoints
5. **Application:** Check localStorage/sessionStorage

---

## Migration Guidelines

### Planning Version Upgrades

#### 1. Pre-Migration Checklist

- [ ] Backup database completely
- [ ] Backup custom modules
- [ ] Document current customizations
- [ ] Review Odoo upgrade notes
- [ ] Test in isolated environment
- [ ] Plan downtime window
- [ ] Prepare rollback procedure

#### 2. Migration Process

```bash
# 1. Backup
pg_dump database_name > backup_$(date +%Y%m%d).sql

# 2. Create test database
createdb test_database
psql test_database < backup_$(date +%Y%m%d).sql

# 3. Test upgrade
./odoo-bin -d test_database -u all --stop-after-init

# 4. Test custom modules
./odoo-bin -d test_database -u custom_module --test-enable

# 5. If successful, upgrade production
# (During scheduled downtime)
./odoo-bin -d production_database -u all
```

#### 3. Post-Migration Tasks

- [ ] Verify all modules loaded
- [ ] Test critical workflows
- [ ] Check custom functionalities
- [ ] Verify reports and receipts
- [ ] Test hardware integration
- [ ] Monitor error logs
- [ ] User acceptance testing

### Handling Breaking Changes

#### Strategy 1: Version Detection

```python
from odoo.release import version_info

if version_info[0] >= 17:
    # v17+ code
    from odoo.addons.point_of_sale.models.pos_session import PosSession
else:
    # v16 and below code
    from odoo.addons.point_of_sale.models.pos import PosSession
```

#### Strategy 2: Try/Except Import

```python
try:
    # Try new location (v17+)
    from odoo.addons.point_of_sale.app.component import Component
except ImportError:
    # Fall back to old location
    from odoo.addons.point_of_sale.static.src.js.component import Component
```

#### Strategy 3: Separate Branches

Maintain separate Git branches for each major version:
```
main (latest version)
├── branch-17.0
├── branch-16.0
├── branch-15.0
└── branch-14.0
```

---

## Additional Resources

### Official Documentation

- [Odoo Documentation](https://www.odoo.com/documentation/)
- [OWL Framework](https://github.com/odoo/owl)
- [Odoo GitHub Repository](https://github.com/odoo/odoo)

### Community Resources

- [Odoo Community Forums](https://www.odoo.com/forum)
- [Odoo Community Association (OCA)](https://odoo-community.org/)
- [Stack Overflow - Odoo Tag](https://stackoverflow.com/questions/tagged/odoo)

### Learning Resources

- [Odoo eLearning](https://www.odoo.com/slides)
- [Odoo Official Training](https://www.odoo.com/training)
- YouTube channels with Odoo tutorials

### Development Tools

- **Odoo Studio:** No-code customization tool
- **VSCode Odoo Plugin:** IDE support
- **PyCharm Odoo Plugin:** IDE support
- **Browser DevTools:** Frontend debugging
- **pgAdmin:** Database management

---

## Next Steps

After reading this overview document:

1. **Choose Your Version:** Navigate to the version-specific guide
   - [17-pos-customization-proposal.md](./17-pos-customization-proposal.md) for Odoo 17.0
   - [16-pos-customization-proposal.md](./16-pos-customization-proposal.md) for Odoo 16.0 (TBD)
   - [15-pos-customization-proposal.md](./15-pos-customization-proposal.md) for Odoo 15.0 (TBD)

2. **Review Examples:** Study the code examples in your version guide

3. **Plan Customization:** Design your module structure

4. **Implement:** Follow the patterns from version-specific guide

5. **Test:** Thoroughly test in development environment

6. **Deploy:** Roll out to production with proper backups

---

## Contributing

To contribute to this documentation:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Documentation Standards

- Use clear, concise language
- Include code examples for concepts
- Test all code examples before committing
- Update version-specific guides when needed
- Maintain consistent formatting

---

## Conclusion

This overview provides the foundation for understanding Odoo POS customization across all versions. The inheritance-based approach ensures your customizations remain compatible with future updates while allowing extensive functionality modifications.

**Key Takeaways:**
- Always use inheritance, never modify core files
- Understand your version's architecture
- Follow best practices for maintainability
- Plan for version upgrades from the start
- Document everything thoroughly

Proceed to your version-specific guide for detailed implementation instructions.

---

**Document Version:** 1.0
**Last Updated:** 2025-11-16
**Next Review:** When new Odoo version is released

---

**Related Documents:**
- [17-pos-customization-proposal.md](./17-pos-customization-proposal.md) - Odoo 17.0 Guide
- [16-pos-customization-proposal.md](./16-pos-customization-proposal.md) - Odoo 16.0 Guide (TBD)
- [15-pos-customization-proposal.md](./15-pos-customization-proposal.md) - Odoo 15.0 Guide (TBD)

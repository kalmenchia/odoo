# instant-ERP POS Branding

Complete rebranding solution for Odoo 17.0 Point of Sale that replaces Odoo branding with instant-ERP.

## Features

✅ **Replace Odoo Logo** - instant-ERP logo in POS navbar
✅ **Custom Receipts** - Remove "Powered by Odoo", add instant-ERP branding
✅ **Configurable** - Custom header/footer text per POS
✅ **No Core Modifications** - 100% inheritance-based
✅ **Upgrade Safe** - Compatible with Odoo upgrades

## Installation

### 1. Place Module in custom-addons

```bash
# This module should already be in:
/path/to/odoo/custom-addons/instant_erp_pos_branding/
```

### 2. Update Odoo Configuration

Ensure `custom-addons` is in your addons path (`odoo.conf`):

```ini
[options]
addons_path = /path/to/odoo/addons,/path/to/odoo/custom-addons
```

### 3. Restart Odoo

```bash
sudo systemctl restart odoo
# OR
./odoo-bin -c /path/to/odoo.conf
```

### 4. Install Module

1. Go to **Apps** menu
2. Click **Update Apps List**
3. Search for **instant-ERP POS Branding**
4. Click **Install**

## Usage

### Basic Usage

After installation, instant-ERP branding is automatically applied:

- ✅ POS navbar shows instant-ERP logo
- ✅ Receipts show "Powered by instant-ERP"
- ✅ Custom header and footer on receipts

### Configuration

#### Per-POS Configuration

Go to: **Point of Sale → Configuration → Point of Sale → [Your POS]**

Scroll to **instant-ERP Branding** section:

- **Enable instant-ERP Branding**: Toggle branding on/off
- **Custom Receipt Header**: Text shown at top of receipts
- **Custom Receipt Footer**: Text shown at bottom of receipts

#### Company-Wide Logo Configuration

Go to: **Settings → Companies → [Your Company]**

- **instant-ERP POS Logo**: Custom logo for POS interface
- **instant-ERP Receipt Logo**: Custom logo for receipts

If not set, default instant-ERP logos are used.

## Customization

### Change Brand Colors

Edit: `static/src/scss/instant_erp_branding.scss`

```scss
// Brand Colors
$instant-primary: #2563eb;      // Change to your color
$instant-secondary: #7c3aed;    // Change to your color
$instant-accent: #f59e0b;       // Change to your color
```

### Add Your Own Logos

Replace images in:
- `static/src/img/instant_erp_logo.png` (150x50px recommended)
- `static/src/img/instant_erp_receipt_logo.png` (300x100px recommended)

### Custom Styling

Uncomment sections in `instant_erp_branding.scss` to enable:
- Custom button colors
- Product card styling
- Payment screen colors

## File Structure

```
instant_erp_pos_branding/
├── __init__.py
├── __manifest__.py
├── README.md                          # This file
├── models/
│   ├── __init__.py
│   ├── pos_config.py                  # POS configuration
│   ├── pos_order.py                   # Order branding data
│   └── res_company.py                 # Company logos
├── views/
│   └── pos_config_views.xml           # Backend views
├── static/
│   ├── description/
│   │   └── icon.png                   # Module icon
│   └── src/
│       ├── app/
│       │   └── overrides/
│       │       ├── navbar.js          # Logo URL logic
│       │       ├── navbar.xml         # Replace navbar logo
│       │       ├── receipt_header.xml # Receipt header branding
│       │       └── order_receipt.xml  # Receipt footer branding
│       ├── img/
│       │   ├── instant_erp_logo.png          # POS logo
│       │   └── instant_erp_receipt_logo.png  # Receipt logo
│       └── scss/
│           └── instant_erp_branding.scss     # Styling
└── security/
    └── ir.model.access.csv            # Access rights (if needed)
```

## Technical Details

### How It Works

#### Backend (Python)
- Extends `pos.config` with branding settings
- Extends `pos.order` to export branding data to UI
- Extends `res.company` for custom logo fields

#### Frontend (JavaScript/OWL)
- Patches `Navbar` component to provide logo URL
- Template inheritance to replace Odoo branding

#### Inheritance Pattern
```python
class PosConfig(models.Model):
    _inherit = 'pos.config'  # Extend, don't replace
    # Add fields...
```

```javascript
patch(Navbar.prototype, {
    // Add or override methods
});
```

```xml
<t t-inherit="point_of_sale.Navbar" t-inherit-mode="extension">
    <!-- Modify template -->
</t>
```

### No Core Files Modified

✅ All customizations use **inheritance**
✅ No changes to `/addons/point_of_sale/`
✅ Safe to upgrade Odoo

## Troubleshooting

### Logo Not Showing

1. **Clear browser cache**: Ctrl+Shift+R
2. **Check image files exist**:
   ```bash
   ls -la custom-addons/instant_erp_pos_branding/static/src/img/
   ```
3. **Regenerate assets**:
   ```bash
   ./odoo-bin --dev=all -d your_database
   ```

### Receipts Still Show "Powered by Odoo"

1. **Module installed?** Check Apps → Installed Applications
2. **POS cache**: Clear browser cache completely
3. **Close and reopen POS session**

### Changes Not Visible

```bash
# Update module
./odoo-bin -u instant_erp_pos_branding -d your_database

# Restart Odoo
sudo systemctl restart odoo
```

### JavaScript Errors

1. Check browser console (F12)
2. Verify file paths in `__manifest__.py`
3. Check Odoo server logs:
   ```bash
   tail -f /var/log/odoo/odoo-server.log
   ```

## Uninstallation

1. Go to **Apps**
2. Search for **instant-ERP POS Branding**
3. Click **Uninstall**

All Odoo branding will be restored.

## Support

For issues or questions:
- Check documentation: `/path/to/odoo/17-pos-customization-proposal.md`
- Review Odoo logs
- Consult Odoo community forums

## Version

- **Module Version**: 17.0.1.0.0
- **Odoo Version**: 17.0
- **Last Updated**: 2025-11-16

## License

LGPL-3

## Author

instant-ERP Development Team
https://www.instant-erp.com

---

**Perfect for:**
- Rebranding Odoo POS for your business
- White-label POS solutions
- Learning Odoo customization patterns
- Understanding inheritance-based development

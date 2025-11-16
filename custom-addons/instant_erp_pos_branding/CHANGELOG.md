# Changelog - instant-ERP POS Branding

All notable changes to this module will be documented in this file.

## [17.0.1.0.0] - 2025-11-16

### ✨ Initial Release

#### Added
- Complete Odoo POS debranding solution
- instant-ERP logo in POS navbar
- instant-ERP branding on receipts
- Removal of all "Powered by Odoo" references
- Configurable receipt header and footer text per POS
- Company-specific logo upload capability
- SVG logo support for better quality
- Robust error handling and fallback logic
- Security access rights configuration
- Comprehensive documentation

#### Features

**Frontend (JavaScript/OWL):**
- Navbar component patching with logo URL logic
- Try-catch error handling for logo retrieval
- Fallback to default SVG logos
- Optional receipt logo URL getter

**Backend (Python):**
- Custom fields on `pos.config`:
  - `enable_instant_erp_branding`
  - `instant_erp_receipt_header`
  - `instant_erp_receipt_footer`
- Custom fields on `res.company`:
  - `instant_erp_pos_logo`
  - `instant_erp_receipt_logo`
- Order export customization for receipt data

**Templates:**
- Navbar logo replacement with precise XPath
- Receipt header with instant-ERP branding
- Receipt footer with instant-ERP branding
- Conditional rendering based on configuration

**Styling:**
- Custom SCSS with instant-ERP brand colors
- Professional receipt formatting
- Optional button and UI color customization

**Assets:**
- High-quality SVG logos (navbar and receipt)
- Scalable vector graphics for all screen sizes
- Fallback handling for missing images

#### Technical

**Architecture:**
- 100% inheritance-based implementation
- No core Odoo files modified
- Upgrade-safe design
- Modular and maintainable code structure

**Security:**
- Access rights for POS users and managers
- Input sanitization
- XSS prevention
- Proper permission checks

**Error Handling:**
- Try-catch blocks in JavaScript
- Null-safe operations with optional chaining
- Fallback logo URLs
- Console warnings for debugging

**Documentation:**
- Comprehensive README.md
- Detailed INSTALLATION.md guide
- Complete TESTING.md procedures
- Inline code comments
- HTML description page for Odoo Apps

#### Quality Assurance

**Code Quality:**
- Clean, documented code
- Following Odoo conventions
- Proper module structure
- Version-specific implementation

**Testing:**
- XPath expressions verified against v17.0 source
- All receipt templates checked
- Edge cases handled
- Browser compatibility considered

**Performance:**
- Minimal performance impact
- Efficient asset loading
- Optimized image formats (SVG)
- No unnecessary computations

### Technical Details

**Module Structure:**
```
instant_erp_pos_branding/
├── __init__.py
├── __manifest__.py
├── README.md
├── INSTALLATION.md
├── TESTING.md
├── CHANGELOG.md
├── models/
│   ├── __init__.py
│   ├── pos_config.py
│   ├── pos_order.py
│   └── res_company.py
├── views/
│   └── pos_config_views.xml
├── security/
│   └── ir.model.access.csv
└── static/
    ├── description/
    │   └── index.html
    └── src/
        ├── app/overrides/
        │   ├── navbar.js
        │   ├── navbar.xml
        │   ├── order_receipt.xml
        │   └── receipt_header.xml
        ├── img/
        │   ├── instant_erp_logo.svg
        │   └── instant_erp_receipt_logo.svg
        └── scss/
            └── instant_erp_branding.scss
```

**Dependencies:**
- `point_of_sale` (Odoo 17.0)

**Assets Loaded:**
- 4 XML template files
- 1 JavaScript file
- 1 SCSS file
- 2 SVG images

**Debranding Coverage:**
- ✅ POS navbar logo
- ✅ Receipt header
- ✅ Receipt footer "Powered by Odoo" text
- ✅ All order receipts
- ✅ Reprint receipts
- ✅ Cash move receipts (via ReceiptHeader)

### Known Limitations

- Module is specific to Odoo 17.0
- Requires OWL framework (not compatible with v14 and earlier)
- POS module must be installed
- Custom logos should be uploaded via backend

### Future Enhancements (Potential)

- [ ] Support for additional Odoo versions (16.0, 18.0)
- [ ] Logo upload directly from POS config
- [ ] Additional color scheme presets
- [ ] Multilingual branding text
- [ ] QR code customization
- [ ] Email receipt template branding

### Upgrade Path

From a fresh Odoo 17.0 installation:
1. Install `point_of_sale` module
2. Install `instant_erp_pos_branding` module
3. Configure as needed

No data migration required for initial installation.

### License

LGPL-3

### Author

instant-ERP Development Team
https://www.instant-erp.com

### Support

For issues or questions:
- Review documentation in module folder
- Check INSTALLATION.md and TESTING.md
- Consult Odoo community forums
- Contact instant-ERP support

---

## Version Numbering

Format: `ODOO_VERSION.MAJOR.MINOR.PATCH`

- `17.0` - Odoo version
- `1` - Major version (breaking changes)
- `0` - Minor version (features)
- `0` - Patch version (bug fixes)

---

**Latest Version:** 17.0.1.0.0
**Release Date:** 2025-11-16
**Status:** Stable ✅

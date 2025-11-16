# Testing Guide - instant-ERP POS Branding

This document provides comprehensive testing procedures to ensure the module is working correctly.

## Pre-Installation Testing

### 1. Module Structure Validation

**Check file structure:**
```bash
cd /path/to/odoo/custom-addons/instant_erp_pos_branding
find . -type f | sort
```

**Expected files:**
- ✅ `__init__.py`
- ✅ `__manifest__.py`
- ✅ `models/__init__.py`
- ✅ `models/pos_config.py`
- ✅ `models/pos_order.py`
- ✅ `models/res_company.py`
- ✅ `views/pos_config_views.xml`
- ✅ `security/ir.model.access.csv`
- ✅ `static/src/app/overrides/navbar.js`
- ✅ `static/src/app/overrides/navbar.xml`
- ✅ `static/src/app/overrides/order_receipt.xml`
- ✅ `static/src/app/overrides/receipt_header.xml`
- ✅ `static/src/img/instant_erp_logo.svg`
- ✅ `static/src/img/instant_erp_receipt_logo.svg`
- ✅ `static/src/scss/instant_erp_branding.scss`

### 2. Syntax Validation

**Check Python syntax:**
```bash
python3 -m py_compile models/*.py
echo $?  # Should output 0 (success)
```

**Check XML syntax:**
```bash
xmllint --noout views/*.xml
xmllint --noout static/src/app/overrides/*.xml
```

**Check JavaScript syntax:**
```bash
node --check static/src/app/overrides/*.js 2>&1 || echo "OK"
```

## Post-Installation Testing

### 1. Module Installation

**Test Steps:**
1. Open Odoo
2. Go to Apps
3. Update Apps List
4. Search "instant-ERP POS Branding"
5. Click Install

**Expected Result:**
- ✅ Module installs without errors
- ✅ No errors in Odoo logs
- ✅ Module shows as "Installed"

**Verify in logs:**
```bash
tail -f /var/log/odoo/odoo-server.log | grep -i "instant_erp"
```

Should see: `Module instant_erp_pos_branding: installation succeeded`

### 2. POS Navbar Branding

**Test Steps:**
1. Go to Point of Sale → Dashboard
2. Click "New Session"
3. Inspect navbar (top-left corner)

**Expected Results:**
- ✅ instant-ERP logo visible (blue with lightning bolt)
- ✅ NO Odoo logo visible
- ✅ Logo is clear and not distorted
- ✅ Logo fits properly in navbar height

**Browser Console Check:**
- Press F12
- Check for JavaScript errors
- Should see no errors related to instant-ERP

### 3. Receipt Branding - Header

**Test Steps:**
1. In POS, add a product
2. Click Payment
3. Select payment method
4. Click Validate
5. View receipt

**Expected Results:**
- ✅ instant-ERP logo appears at top of receipt
- ✅ Custom header text visible (if configured)
- ✅ "Welcome to instant-ERP" text (default header)
- ✅ Separator line below header

### 4. Receipt Branding - Footer

**Test Steps:**
1. Scroll to bottom of receipt
2. Check footer section

**Expected Results:**
- ✅ "Powered by instant-ERP" text visible
- ✅ "Powered by Odoo" text NOT visible
- ✅ Custom footer text visible (default: "Visit us at www.instant-erp.com")
- ✅ No Odoo.com links or references

**Critical Test:**
```grep
Search receipt for "Odoo" (case-insensitive)
- Should ONLY find: "Powered by instant-ERP"
- Should NOT find standalone "Odoo" references
```

### 5. Receipt Printing

**Test Steps:**
1. Complete a sale
2. Print receipt (if printer configured)
3. Examine printed receipt

**Expected Results:**
- ✅ Prints without errors
- ✅ instant-ERP branding visible on print
- ✅ No Odoo branding visible on print
- ✅ Layout is clean and readable

### 6. Configuration Options

**Test Steps:**
1. Go to Point of Sale → Configuration → Point of Sale
2. Open a POS configuration
3. Scroll to "instant-ERP Branding" section

**Expected Results:**
- ✅ "Enable instant-ERP Branding" checkbox visible
- ✅ "Custom Receipt Header" field visible
- ✅ "Custom Receipt Footer" field visible
- ✅ Default values populated

**Test Custom Text:**
1. Enter custom header: "Test Header Text"
2. Enter custom footer: "Test Footer Text"
3. Save
4. Open POS and make a sale
5. Check receipt

**Expected:**
- ✅ Custom header appears on receipt
- ✅ Custom footer appears on receipt

### 7. Company Logo Upload

**Test Steps:**
1. Go to Settings → Companies
2. Select company
3. Upload image to "instant-ERP POS Logo" field
4. Save
5. Open POS

**Expected Results:**
- ✅ Custom logo appears in POS navbar
- ✅ No errors during upload
- ✅ Logo displays correctly

**Test with different image formats:**
- ✅ PNG image works
- ✅ JPG image works
- ✅ SVG image works

### 8. Error Handling

**Test missing logo files:**
1. Temporarily rename logo SVG files
2. Open POS

**Expected Result:**
- ✅ POS still opens (doesn't crash)
- ✅ Fallback logo or placeholder shown
- ✅ Warning in console (expected)
- ✅ POS remains functional

**Restore files after test.**

### 9. Multi-Company Testing

If you have multiple companies:

**Test Steps:**
1. Switch between companies
2. Open POS for each company
3. Check branding

**Expected Results:**
- ✅ Each company can have different logos
- ✅ Branding changes per company
- ✅ No conflicts between companies

### 10. Receipt Types Testing

**Test different receipt scenarios:**

**A. Regular Sale:**
- ✅ Full receipt with instant-ERP branding

**B. Reprinted Receipt:**
1. Click Orders in menu
2. Select an order
3. Click Reprint Receipt

**Expected:**
- ✅ instant-ERP branding on reprint
- ✅ No Odoo branding

**C. Cash In/Out Receipt:**
1. Click Cash In/Out in menu
2. Enter amount and reason
3. Check receipt

**Expected:**
- ✅ instant-ERP header (if configured)
- ✅ Uses ReceiptHeader component

### 11. Browser Compatibility

Test in multiple browsers:

**Chrome/Chromium:**
- ✅ Logo displays correctly
- ✅ No console errors

**Firefox:**
- ✅ Logo displays correctly
- ✅ No console errors

**Safari (if applicable):**
- ✅ Logo displays correctly
- ✅ No console errors

**Edge:**
- ✅ Logo displays correctly
- ✅ No console errors

### 12. Performance Testing

**Test Steps:**
1. Open POS
2. Note loading time
3. Navigate between screens
4. Process multiple sales

**Expected Results:**
- ✅ No noticeable performance degradation
- ✅ Logo loads quickly
- ✅ No lag when switching screens
- ✅ Receipts generate quickly

### 13. Upgrade Safety

**Test module upgrade:**
```bash
./odoo-bin -u instant_erp_pos_branding -d test_database
```

**Expected Results:**
- ✅ Upgrades without errors
- ✅ All branding preserved
- ✅ No data loss
- ✅ Configuration maintained

### 14. Uninstallation Testing

**Test Steps:**
1. Go to Apps
2. Find "instant-ERP POS Branding"
3. Click Uninstall
4. Confirm
5. Open POS

**Expected Results:**
- ✅ Uninstalls cleanly
- ✅ Odoo branding restored
- ✅ "Powered by Odoo" back on receipts
- ✅ Odoo logo back in navbar
- ✅ No orphaned data

**Reinstall to continue testing.**

## Edge Cases & Stress Testing

### Edge Case 1: Empty Configuration

**Test:**
1. Clear all custom text fields
2. Set to empty strings
3. Open POS and make sale

**Expected:**
- ✅ Receipt still shows basic instant-ERP branding
- ✅ No errors or crashes
- ✅ Falls back to defaults

### Edge Case 2: Very Long Custom Text

**Test:**
1. Enter 1000+ characters in header/footer
2. Save and test

**Expected:**
- ✅ Text displays (may wrap)
- ✅ No layout breakage
- ✅ Receipt still readable

### Edge Case 3: Special Characters

**Test:**
1. Enter special chars: `<>&"'©®™`
2. Save and test

**Expected:**
- ✅ Characters escaped properly
- ✅ No XSS vulnerabilities
- ✅ Displays correctly

### Edge Case 4: Network Issues

**Test:**
1. Disconnect network during POS operation
2. Try to print receipt

**Expected:**
- ✅ Offline functionality maintained
- ✅ Branding still works
- ✅ Receipt generates locally

## Regression Testing

After any changes to the module:

1. [ ] POS navbar logo
2. [ ] Receipt header
3. [ ] Receipt footer
4. [ ] Configuration options
5. [ ] Custom logo upload
6. [ ] Receipt printing
7. [ ] No Odoo references
8. [ ] Performance
9. [ ] Browser compatibility
10. [ ] Installation/Uninstallation

## Security Testing

### 1. Access Rights

**Test as POS User:**
- ✅ Can see branding
- ✅ Can view configuration (read-only)
- ✅ Cannot modify configuration

**Test as POS Manager:**
- ✅ Can see branding
- ✅ Can view configuration
- ✅ Can modify configuration
- ✅ Can upload logos

### 2. XSS Prevention

**Test:**
1. Enter `<script>alert('XSS')</script>` in custom text
2. Save and view receipt

**Expected:**
- ✅ Script does NOT execute
- ✅ Text is escaped/sanitized
- ✅ Receipt displays safely

### 3. SQL Injection Prevention

**Test:**
1. Enter SQL commands in text fields
2. Try to save

**Expected:**
- ✅ No SQL errors
- ✅ Input sanitized
- ✅ Database safe

## Automated Testing (Optional)

**Create test file: `tests/test_instant_erp_branding.py`**

```python
from odoo.tests import TransactionCase

class TestInstantErpBranding(TransactionCase):

    def setUp(self):
        super().setUp()
        self.pos_config = self.env['pos.config'].create({
            'name': 'Test POS',
        })

    def test_module_installed(self):
        """Test module is installed"""
        module = self.env['ir.module.module'].search([
            ('name', '=', 'instant_erp_pos_branding')
        ])
        self.assertTrue(module)
        self.assertEqual(module.state, 'installed')

    def test_pos_config_fields(self):
        """Test custom fields exist on pos.config"""
        self.assertTrue(hasattr(self.pos_config, 'enable_instant_erp_branding'))
        self.assertTrue(hasattr(self.pos_config, 'instant_erp_receipt_header'))
        self.assertTrue(hasattr(self.pos_config, 'instant_erp_receipt_footer'))

    def test_default_values(self):
        """Test default values are set"""
        self.assertTrue(self.pos_config.enable_instant_erp_branding)
        self.assertIn('instant-ERP', self.pos_config.instant_erp_receipt_header)
```

**Run tests:**
```bash
./odoo-bin -d test_database --test-enable --stop-after-init -u instant_erp_pos_branding
```

## Final Validation Checklist

Before marking module as production-ready:

- [ ] All tests pass
- [ ] No errors in logs
- [ ] No JavaScript console errors
- [ ] POS navbar shows instant-ERP logo
- [ ] NO "Powered by Odoo" on receipts
- [ ] "Powered by instant-ERP" visible
- [ ] Custom text configurable
- [ ] Custom logos uploadable
- [ ] Works in all tested browsers
- [ ] Performance is acceptable
- [ ] Module installs cleanly
- [ ] Module uninstalls cleanly
- [ ] Module upgrades cleanly
- [ ] Documentation complete
- [ ] Security validated
- [ ] Edge cases handled
- [ ] No regressions introduced

## Bug Tracking

If issues are found during testing:

1. Document the issue
2. Include steps to reproduce
3. Include expected vs actual behavior
4. Include screenshots if applicable
5. Include browser/Odoo version
6. Fix and retest

---

**Testing Version:** 17.0.1.0.0
**Last Updated:** 2025-11-16
**Status:** All tests should pass before production deployment

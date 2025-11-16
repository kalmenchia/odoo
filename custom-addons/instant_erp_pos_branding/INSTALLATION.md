# Installation Guide - instant-ERP POS Branding

## Prerequisites

- Odoo 17.0 installed and running
- Access to Odoo configuration file (`odoo.conf`)
- Permissions to restart Odoo service
- Point of Sale module installed

## Installation Steps

### Step 1: Configure custom-addons Directory

Ensure the `custom-addons` directory exists and is in your Odoo addons path.

**Edit `odoo.conf`:**

```ini
[options]
addons_path = /path/to/odoo/addons,/path/to/odoo/custom-addons
```

Replace `/path/to/odoo` with your actual Odoo installation path.

### Step 2: Verify Module Files

Ensure all module files are present:

```bash
cd /path/to/odoo/custom-addons/instant_erp_pos_branding
ls -la
```

You should see:
```
├── __init__.py
├── __manifest__.py
├── README.md
├── INSTALLATION.md
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

### Step 3: Restart Odoo

```bash
sudo systemctl restart odoo
```

Or if running manually:
```bash
./odoo-bin -c /path/to/odoo.conf
```

### Step 4: Update Apps List

1. Open Odoo in your browser
2. Go to **Apps** menu
3. Remove the "Apps" filter (click the ✕ on the filter)
4. Click **Update Apps List**
5. Click **Update** in the confirmation popup
6. Wait for the update to complete

### Step 5: Install the Module

1. In the Apps menu, search for "instant-ERP POS Branding"
2. Click **Install** button
3. Wait for installation to complete

### Step 6: Verify Installation

1. Go to **Point of Sale** → **Dashboard**
2. Click **New Session** or open an existing POS
3. Verify:
   - instant-ERP logo appears in top-left navbar (not Odoo logo)
   - Make a test sale and print receipt
   - Receipt shows "Powered by instant-ERP" (not "Powered by Odoo")

## Configuration (Optional)

### Configure Custom Receipt Text

**Per POS Configuration:**

1. Go to **Point of Sale** → **Configuration** → **Point of Sale**
2. Select your POS
3. Scroll to **instant-ERP Branding** section
4. Configure:
   - **Enable instant-ERP Branding**: Check to enable (default: enabled)
   - **Custom Receipt Header**: Enter custom text for receipt header
   - **Custom Receipt Footer**: Enter custom text for receipt footer
5. Click **Save**

**Default Values:**
- Header: "Welcome to instant-ERP\nThank you for your business!"
- Footer: "Visit us at www.instant-erp.com\nModern ERP. Simplified."

### Upload Custom Logos (Optional)

**Company-Specific Logos:**

1. Go to **Settings** → **Companies** → **Manage Companies**
2. Select your company
3. Upload:
   - **instant-ERP POS Logo**: Logo for POS navbar (recommended: 150x50px)
   - **instant-ERP Receipt Logo**: Logo for receipts (recommended: 300x100px)
4. Click **Save**

If no custom logos are uploaded, the module uses default SVG logos.

## Troubleshooting

### Module Not Visible in Apps List

**Solution:**
1. Check that module is in correct location: `/path/to/odoo/custom-addons/instant_erp_pos_branding/`
2. Verify `odoo.conf` has correct `addons_path`
3. Restart Odoo
4. Update Apps List again
5. Remove "Apps" filter in Apps menu

### Logo Not Showing in POS

**Solution:**
1. Clear browser cache: **Ctrl + Shift + R** (or Cmd + Shift + R on Mac)
2. Close and reopen POS session
3. Check browser console (F12) for errors
4. Verify SVG files exist in `static/src/img/` directory

### Receipt Still Shows "Powered by Odoo"

**Solution:**
1. Ensure module is **installed** (not just visible in Apps list)
2. Update the module:
   ```bash
   ./odoo-bin -u instant_erp_pos_branding -d your_database
   ```
3. Clear browser cache completely
4. Close POS and reopen
5. Clear assets cache:
   ```bash
   rm -rf ~/.local/share/Odoo/filestore/your_database/assets/*
   ```
6. Restart Odoo

### Permission Errors

**Solution:**
1. Check file permissions:
   ```bash
   sudo chown -R odoo:odoo /path/to/odoo/custom-addons/instant_erp_pos_branding
   sudo chmod -R 755 /path/to/odoo/custom-addons/instant_erp_pos_branding
   ```
2. Restart Odoo

### JavaScript Errors in Console

**Solution:**
1. Check Odoo logs:
   ```bash
   tail -f /var/log/odoo/odoo-server.log
   ```
2. Look for asset compilation errors
3. Verify all JS/XML files have correct syntax
4. Update module to reload assets
5. Run Odoo in development mode for better error messages:
   ```bash
   ./odoo-bin --dev=all -c odoo.conf
   ```

## Uninstallation

If you need to remove the module:

1. Go to **Apps**
2. Search for "instant-ERP POS Branding"
3. Click **Uninstall**
4. Confirm uninstallation

**Note:** All Odoo branding will be restored after uninstallation.

## Verification Checklist

After installation, verify:

- [ ] Module appears in Apps list
- [ ] Module is installed (shows "Installed" status)
- [ ] POS navbar shows instant-ERP logo
- [ ] Test receipt shows "Powered by instant-ERP"
- [ ] No "Powered by Odoo" text visible
- [ ] Custom header text appears on receipts (if configured)
- [ ] Custom footer text appears on receipts (if configured)
- [ ] No errors in browser console
- [ ] No errors in Odoo server logs
- [ ] Receipt prints correctly

## Support

If you encounter issues:

1. Check this installation guide
2. Review module README.md
3. Check Odoo logs for errors
4. Verify all prerequisites are met
5. Try reinstalling the module
6. Contact support or review Odoo community forums

## Production Deployment

Before deploying to production:

1. ✅ Test thoroughly in development environment
2. ✅ Test in staging environment
3. ✅ Backup production database
4. ✅ Schedule deployment during low-traffic period
5. ✅ Have rollback plan ready
6. ✅ Monitor logs after deployment
7. ✅ Verify branding in production POS

---

**Version:** 17.0.1.0.0
**Last Updated:** 2025-11-16

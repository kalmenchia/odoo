# Custom Addons Directory

This directory contains all custom Odoo modules for this installation.

## ⚠️ IMPORTANT

**ALL custom modules MUST be placed in this directory.**

Never modify files in the core `addons/` directory. Always use inheritance to customize Odoo functionality.

## 📁 Directory Structure

```
custom-addons/
├── README.md                          # This file
├── instant_erp_pos_branding/          # Example: instant-ERP POS debranding
├── your_custom_module/                # Your custom modules here
└── ...
```

## 🚀 Creating a New Module

### 1. Create Module Directory

```bash
cd /path/to/odoo/custom-addons
mkdir my_custom_module
cd my_custom_module
```

### 2. Create Basic Structure

```bash
# Create essential files
touch __init__.py
touch __manifest__.py

# Create directories
mkdir models
mkdir views
mkdir static
mkdir security
mkdir data
```

### 3. Minimum Required Files

#### `__init__.py`
```python
# -*- coding: utf-8 -*-
from . import models
```

#### `__manifest__.py`
```python
# -*- coding: utf-8 -*-
{
    'name': 'My Custom Module',
    'version': '17.0.1.0.0',
    'category': 'Customization',
    'summary': 'Brief description',
    'depends': ['base'],
    'data': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
```

## 📝 Module Naming Conventions

- Use lowercase with underscores: `my_custom_module`
- Be descriptive: `instant_erp_pos_branding` not `pos_mod`
- Include version if needed: `custom_module_v17`

## 🔧 Configuration

### Add to Odoo Configuration

Edit your `odoo.conf` file:

```ini
[options]
addons_path = /path/to/odoo/addons,/path/to/odoo/custom-addons
```

### Restart Odoo

```bash
sudo systemctl restart odoo
# OR
./odoo-bin -c /path/to/odoo.conf
```

## 📦 Installing Custom Modules

1. **Update Apps List**
   - Go to Apps menu (activate Developer Mode if needed)
   - Click "Update Apps List"
   - Click "Update" in the popup

2. **Install Module**
   - Search for your module name
   - Click "Install"

3. **Upgrade Module** (after making changes)
   ```bash
   ./odoo-bin -u module_name -d database_name
   ```

## 🎯 Available Custom Modules

### instant_erp_pos_branding
Complete POS debranding solution for Odoo 17.0
- Replaces Odoo branding with instant-ERP
- Custom logo in POS interface
- Custom receipt templates
- No core file modifications

**Status**: ✅ Active
**Version**: 17.0.1.0.0
**Documentation**: See [17-pos-customization-proposal.md](../17-pos-customization-proposal.md)

## 📋 Best Practices

### 1. Always Use Inheritance

```python
# ✅ Good
class ResPartner(models.Model):
    _inherit = 'res.partner'
    custom_field = fields.Char('Custom')

# ❌ Bad - Never do this
class ResPartner(models.Model):
    _name = 'res.partner'  # This will break things!
```

### 2. Proper Dependencies

List all modules you inherit from:

```python
'depends': [
    'base',
    'point_of_sale',
    'sale',
],
```

### 3. Version Numbering

Format: `ODOO_VERSION.MAJOR.MINOR.PATCH`
- `17.0.1.0.0` - First version for Odoo 17.0
- `17.0.1.1.0` - Minor update
- `17.0.2.0.0` - Major update

### 4. Security

Always include security rules:

```
security/
├── ir.model.access.csv
└── security_rules.xml
```

### 5. Translations

Support multiple languages:

```
i18n/
├── fr.po
├── es.po
└── de.po
```

## 🔍 Module Development Checklist

- [ ] Module structure is correct
- [ ] `__manifest__.py` has all required fields
- [ ] Dependencies are listed
- [ ] Security rules defined
- [ ] Code follows Odoo conventions
- [ ] Tested in development environment
- [ ] Documentation included
- [ ] Version control (Git) used

## 🐛 Debugging

### Enable Developer Mode

Add to URL: `?debug=1`

Or: Settings → Activate Developer Mode

### Check Logs

```bash
# View live logs
tail -f /var/log/odoo/odoo-server.log

# Search for errors
grep ERROR /var/log/odoo/odoo-server.log
```

### Development Mode

```bash
# Run with auto-reload and debugging
./odoo-bin --dev=all -d database_name
```

### Odoo Shell

```bash
# Interactive Python shell
./odoo-bin shell -d database_name

# Example usage:
>>> self.env['res.partner'].search([])
```

## 📚 Documentation

For detailed customization guides, see:
- [POS Customization README](../POS-CUSTOMIZATION-README.md)
- [General Overview](../00-pos-customization-proposal.md)
- [Odoo 17.0 Guide](../17-pos-customization-proposal.md)

## 🚫 What NOT to Do

### Never Modify Core Files

❌ Don't edit files in `/addons/`
❌ Don't change base Odoo modules
❌ Don't skip inheritance

### Never Hardcode

❌ Database credentials
❌ File paths
❌ API keys
❌ Company-specific data

Use configuration, environment variables, or database records instead.

## 🔒 Security Notes

- Always validate user input
- Check access rights
- Use `sudo()` carefully
- Sanitize data before display
- Never trust frontend data

## 📦 Module Distribution

### For Internal Use

Keep in this directory and back up regularly.

### For Distribution

```bash
# Create module archive
cd custom-addons
zip -r my_module.zip my_module/ -x "*.pyc" -x "__pycache__/*"
```

### Git Repository

```bash
cd custom-addons
git init
git add my_module/
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

## 🆘 Getting Help

1. Check module logs
2. Review Odoo documentation
3. Search Odoo forums
4. Check module dependencies
5. Verify file permissions

## 📊 Module Status

| Module Name | Version | Status | Last Updated |
|-------------|---------|--------|--------------|
| instant_erp_pos_branding | 17.0.1.0.0 | ✅ Active | 2025-11-16 |

---

**Last Updated**: 2025-11-16
**Odoo Version**: 17.0

---

For questions or issues, refer to the main documentation or Odoo community resources.

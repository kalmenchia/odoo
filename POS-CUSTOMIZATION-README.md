# Odoo POS Customization Documentation

Welcome to the Odoo Point of Sale Customization Documentation Suite.

## 📚 Documentation Structure

This documentation is organized into version-specific guides to help you customize Odoo POS across different versions:

### Overview Document
- **[00-pos-customization-proposal.md](./00-pos-customization-proposal.md)** - General overview, architecture, and best practices (applies to all versions)

### Version-Specific Guides
- **[17-pos-customization-proposal.md](./17-pos-customization-proposal.md)** - Odoo 17.0 specific implementation guide
- **[16-pos-customization-proposal.md](./16-pos-customization-proposal.md)** - Odoo 16.0 guide (To Be Created)
- **[15-pos-customization-proposal.md](./15-pos-customization-proposal.md)** - Odoo 15.0 guide (To Be Created)

## 🚀 Quick Start

1. **Start Here**: Read [00-pos-customization-proposal.md](./00-pos-customization-proposal.md) for general concepts
2. **Choose Your Version**: Navigate to your specific Odoo version guide
3. **Follow Examples**: All guides include working code examples
4. **Test**: Always test in development before production

## 📁 Custom Addons Directory

**IMPORTANT**: All custom modules MUST be placed in the `custom-addons/` directory at the root of the Odoo installation.

```
odoo/
├── addons/              # Core Odoo modules (DO NOT MODIFY)
├── custom-addons/       # Your custom modules go here
│   ├── instant_erp_pos_branding/
│   ├── custom_pos_module/
│   └── ...
├── odoo-bin
└── ...
```

### Why Use custom-addons/?

✅ **Separation of Concerns**: Keeps custom code separate from core Odoo
✅ **Easy Upgrades**: Core Odoo can be upgraded without affecting custom modules
✅ **Version Control**: Easy to track and manage custom code
✅ **Clean Organization**: Clear distinction between core and custom functionality

### Setting Up custom-addons Directory

1. **Create the directory** (if it doesn't exist):
   ```bash
   mkdir -p /path/to/odoo/custom-addons
   ```

2. **Add to Odoo configuration** (`odoo.conf`):
   ```ini
   [options]
   addons_path = /path/to/odoo/addons,/path/to/odoo/custom-addons
   ```

3. **Restart Odoo**:
   ```bash
   sudo systemctl restart odoo
   # or
   ./odoo-bin -c odoo.conf
   ```

4. **Update Apps List**:
   - Go to Apps menu
   - Click "Update Apps List"
   - Your custom modules will appear

## 🎯 Featured Implementation

### instant-ERP POS Branding

A complete working example of POS debranding is included in the v17.0 guide:
- Replaces Odoo logo with instant-ERP branding
- Removes all Odoo references from receipts
- Custom styling and colors
- Fully inheritance-based (no core file modifications)

See [17-pos-customization-proposal.md - instant-ERP Debranding](./17-pos-customization-proposal.md#instant-erp-debranding-proposal) for complete implementation.

## 📖 What's Covered

Each version-specific guide includes:

### Backend Customization
- ✅ Inheriting Python models
- ✅ Adding custom fields
- ✅ Custom business logic
- ✅ Data loading and processing

### Frontend Customization
- ✅ Extending OWL components (v15+)
- ✅ Template inheritance (QWeb)
- ✅ Custom screens and popups
- ✅ Layout modifications

### Specific Examples
- ✅ Layout customization
- ✅ Adding custom functions
- ✅ Modifying numpad/keypad
- ✅ Payment method customization
- ✅ Receipt template customization
- ✅ Loyalty system implementation
- ✅ Complete debranding solution

## 🛠️ Development Workflow

### 1. Development Environment

```bash
# Create custom module
cd /path/to/odoo/custom-addons
mkdir my_custom_module
cd my_custom_module

# Create basic structure
touch __init__.py __manifest__.py
mkdir models static views
```

### 2. Development Mode

```bash
# Run Odoo in development mode
./odoo-bin --dev=all -d your_database -c odoo.conf
```

### 3. Testing

```bash
# Update module
./odoo-bin -u my_custom_module -d your_database

# Run tests
./odoo-bin -d your_database -i my_custom_module --test-enable --stop-after-init
```

### 4. Deployment

1. ✅ Test thoroughly in development
2. ✅ Test in staging environment
3. ✅ Backup production database
4. ✅ Deploy during low-traffic period
5. ✅ Monitor logs after deployment

## 📋 Version Compatibility Matrix

| Odoo Version | Frontend Framework | Python | PostgreSQL | Status |
|--------------|-------------------|--------|------------|---------|
| 17.0 | OWL | 3.10+ | 12+ | ✅ Documented |
| 16.0 | OWL | 3.8+ | 10+ | 📝 TBD |
| 15.0 | OWL | 3.7+ | 10+ | 📝 TBD |
| 14.0 | Backbone.js | 3.7+ | 10+ | 📝 TBD |

## 🔑 Key Principles

### Always Use Inheritance

```python
# ✅ CORRECT: Inherit and extend
class PosOrder(models.Model):
    _inherit = 'pos.order'
    custom_field = fields.Char('Custom')

# ❌ WRONG: Never modify core files
# /addons/point_of_sale/models/pos_order.py
```

### Keep Custom Code Separate

```
✅ /custom-addons/my_module/      # Good
❌ /addons/point_of_sale/          # Never modify
```

### Document Everything

```python
def custom_method(self):
    """
    Clear description of what this does.

    :return: Description of return value
    """
    pass
```

## 🆘 Getting Help

### Check Documentation
1. Read the overview document first
2. Check your version-specific guide
3. Review troubleshooting sections

### Debug Tools
```bash
# Enable debug mode
?debug=1

# Check logs
tail -f /var/log/odoo/odoo-server.log

# Odoo shell
./odoo-bin shell -d database_name
```

### Common Issues
- Module won't install → Check dependencies and syntax
- Changes not visible → Clear cache and restart
- JavaScript errors → Check browser console
- Template not updating → Clear assets cache

## 📚 Additional Resources

- [Odoo Official Documentation](https://www.odoo.com/documentation/)
- [OWL Framework Guide](https://github.com/odoo/owl)
- [Odoo Community Forums](https://www.odoo.com/forum)
- [Odoo GitHub Repository](https://github.com/odoo/odoo)

## 🤝 Contributing

To add documentation for other Odoo versions:

1. Follow the structure of existing version guides
2. Include working code examples
3. Test all examples before documenting
4. Update this README with new version info

## 📄 License

This documentation is provided as-is for educational and development purposes.

---

**Last Updated**: 2025-11-16
**Current Version Coverage**: Odoo 17.0
**Next Update**: When new versions are released or significant changes are made

---

## Quick Navigation

- [General Overview](./00-pos-customization-proposal.md)
- [Odoo 17.0 Guide](./17-pos-customization-proposal.md)
- [Custom Addons Folder](./custom-addons/README.md)

**Happy Customizing! 🎉**

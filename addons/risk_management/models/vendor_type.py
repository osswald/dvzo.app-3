from odoo import models, fields


class VendorType(models.Model):
    _name = "risk_management.vendor_type"
    _description = "Vendor type"

    name = fields.Char("Label", required=True)
    active = fields.Boolean("Active", default=True)

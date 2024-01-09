from odoo import models, fields


class InventoryType(models.Model):
    _name = "inventory.type"
    _description = "Inventory type"

    name = fields.Char("Department", required=True)
    short_name = fields.Char("Short Name", required=True)
    active = fields.Boolean("Active", default=True)

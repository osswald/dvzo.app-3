from odoo import models, fields


class InventoryStatus(models.Model):
    _name = "inventory.status"
    _description = "Inventory status"

    name = fields.Char("Status", required=True)
    label = fields.Char("not used")
    auto_update = fields.Boolean("Auto update")
    active = fields.Boolean("Active", default=True)

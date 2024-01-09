from odoo import models, fields, api


class InventoryLocation(models.Model):
    _name = "inventory.location"
    _description = "Inventory location"

    name = fields.Char("Location", required=True)
    active = fields.Boolean("Active", default=True)

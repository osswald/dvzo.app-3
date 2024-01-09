from odoo import models, fields


class InventoryManufacturer(models.Model):
    _name = "inventory.manufacturer"
    _description = "Inventory manufacturer"

    name = fields.Char("Manufacturer", required=True)
    partner = fields.Many2one("res.partner")
    active = fields.Boolean("Active", default=True)

from odoo import models, fields


class InventoryPlace(models.Model):
    _name = "inventory.place"
    _description = "Inventory place"

    name = fields.Char("Place", required=True)
    short_name = fields.Char("Short Name", required=True)
    active = fields.Boolean("Active", default=True)

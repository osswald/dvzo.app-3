from odoo import models, fields, api


class ExtentOfDamage(models.Model):
    _name = "risk_management.extent_of_damage"
    _description = "Extent of damage"

    name = fields.Char("Label", required=True)

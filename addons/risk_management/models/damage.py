from odoo import models, fields, api


class Damage(models.Model):
    _name = "risk_management.damage"
    _description = "Damage"

    name = fields.Char("Label", required=True)

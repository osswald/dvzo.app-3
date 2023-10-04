from odoo import models, fields, api


class RiskZone(models.Model):
    _name = "risk_management.risk_zone"
    _description = "Risk zone"

    name = fields.Char("Label", required=True)

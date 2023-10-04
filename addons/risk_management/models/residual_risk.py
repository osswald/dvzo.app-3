from odoo import models, fields


class ResidualRisk(models.Model):
    _name = "risk_management.residual_risk"
    _description = "Residual risk"

    name = fields.Char("Label", required=True)

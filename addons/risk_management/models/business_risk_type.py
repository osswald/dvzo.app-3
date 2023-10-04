from odoo import models, fields, api


class BusinessRiskType(models.Model):
    _name = "risk_management.business_risk_type"
    _description = "Business risk type"

    name = fields.Char("Label", required=True)

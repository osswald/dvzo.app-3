from odoo import models, fields


class BusinessRisk(models.Model):
    _name = "risk_management.business_risk"
    _description = "Business risk"

    name = fields.Char("Label", required=True)
    business_risk_type = fields.Many2one("risk_management.business_risk_type", "Business risk type", required=True)
    description = fields.Html("Description")
    risk_assessment_ids = fields.One2many("risk_management.risk_assessment", "business_risk_id", string="Risk assessments")

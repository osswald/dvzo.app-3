from odoo import models, fields


class Asset(models.Model):
    _name = "risk_management.asset"
    _description = "Asset"

    name = fields.Char("Label", required=True)
    asset_type = fields.Many2one("risk_management.asset_type", "Asset type", required=True)
    description = fields.Html("Description")
    risk_assessment_ids = fields.One2many("risk_management.risk_assessment", "asset_id", string="Risk assessments")

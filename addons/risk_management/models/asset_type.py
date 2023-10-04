from odoo import models, fields


class AssetType(models.Model):
    _name = "risk_management.asset_type"
    _description = "Asset type"

    name = fields.Char("Label", required=True)

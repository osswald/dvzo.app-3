from odoo import fields, models


class Partner(models.Model):
    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = "res.partner"

    # --------------------------------------- Fields Declaration ----------------------------------

    # Relational
    risk_assessment_ids = fields.One2many(
        "risk_management.risk_assessment",
        "res_partner_id",
        string="Risk assessments",
        groups="risk_management.group_risk_management_user,risk_management.group_risk_management_manager"
    )

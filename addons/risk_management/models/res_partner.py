from odoo import fields, models


class Partner(models.Model):
    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = "res.partner"

    # --------------------------------------- Fields Declaration ----------------------------------
    is_vendor = fields.Boolean(string="Vendor", default=False)
    vendor_type = fields.Many2many("risk_management.vendor_type", string="Vendor Type")
    risk_assessment = fields.Boolean(string="Risk Assessment", default=False)
    certification = fields.Selection(
        selection=[
            ("na", "Not applicable"),
            ("yes", "Yes"),
            ("no", "No"),
        ],
        string="Certification",
        default="na",
        required=True,
        copy=False)
    certification_valid_until = fields.Date(string="Certification Valid Until")
    responsible = fields.Many2one('res.partner', string="Responsible", domain=[('is_company', '=', False)])

    # Relational
    risk_assessment_ids = fields.One2many(
        "risk_management.risk_assessment",
        "res_partner_id",
        string="Risk assessments",
        groups="risk_management.group_risk_management_user,risk_management.group_risk_management_manager"
    )
    certification_ids = fields.One2many('risk_management.certification', 'vendor')

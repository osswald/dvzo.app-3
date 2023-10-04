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
        #   groups="emergency_contact.group_emergency_contact_user,emergency_contact.group_emergency_contact_manager"
        # TODO: Add groups for module
    )

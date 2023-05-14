from odoo import fields, models


class Partner(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = "res.partner"

    # --------------------------------------- Fields Declaration ----------------------------------

    # Relational
    emergency_contact_ids = fields.One2many("emergency_contact.emergency_contact", "res_partner", string="Emergency "
                                                                                                         "contact")
    has_emergency_contact = fields.Selection(
        selection=[
            ("yes", "Yes"),
            ("no", "No"),
            ("open", "Open"),
        ],
        string="Has emergency contact",
        default="open",
        required=True,
        copy=False
    )

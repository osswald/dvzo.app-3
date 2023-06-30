from odoo import fields, models


class Partner(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = "res.partner"

    # --------------------------------------- Fields Declaration ----------------------------------

    phone_publish = fields.Selection(
        selection=[
            ("unknown", "Unknown"),
            ("yes", "Yes"),
            ("no", "No"),
        ],
        string="Phone publish",
        default="unknown",
        required=True,
    )

    # Relational
    shift_ids = fields.One2many(
        "train_management.day_planning_shift",
        "person",
        groups="train_management.group_train_management_readonly_day_planning"
    )

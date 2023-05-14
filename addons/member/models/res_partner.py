from odoo import fields, models


class Partner(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = "res.partner"

    # --------------------------------------- Fields Declaration ----------------------------------

    date_of_birth = fields.Date("Date of birth")
    gender = fields.Selection(
        selection=[
            ("female", "Female"),
            ("male", "Male"),
            ("divers", "Divers"),
        ],
        string="Gender",
        copy=False
    )
    nationality = fields.Many2one("res.country", string="Nationality")
    membership_id = fields.Char("Membership ID")

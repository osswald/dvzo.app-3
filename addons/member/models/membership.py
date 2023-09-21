from odoo import models, fields, api


class Membership(models.Model):
    _name = "member.membership"
    _description = "Membership"

    res_partner = fields.Many2one("res.partner", required=True)
    membership_type = fields.Many2one("member.membership_type", required=True)
    membership_status = fields.Selection(
        selection=[
            ("active", "Active"),
            ("resigned", "Resigned"),
            ("changed_type", "Changed type"),
        ],
        string="Membership status",
        default="active",
        required=True,
        copy=False
    )
    joining_date = fields.Date("Joining date")
    leaving_date = fields.Date("Leaving date")

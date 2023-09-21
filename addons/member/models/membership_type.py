from odoo import models, fields, api


class MembershipType(models.Model):
    _name = "member.membership_type"
    _description = "Membership Type"

    name = fields.Char("Membership type", required=True)

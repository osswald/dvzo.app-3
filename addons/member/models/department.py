from odoo import models, fields, api


class Department(models.Model):
    _name = "member.department"
    _description = "Department"

    name = fields.Char("Department", required=True)

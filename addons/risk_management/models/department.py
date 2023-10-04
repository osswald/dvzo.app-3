from odoo import models, fields, api


class Department(models.Model):
    _name = "risk_management.department"
    _description = "Department"

    name = fields.Char("Label", required=True)

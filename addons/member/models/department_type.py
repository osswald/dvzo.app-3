from odoo import models, fields, api


class DepartmentType(models.Model):
    _name = "member.department_type"
    _description = "Department type"

    name = fields.Char("Department type", required=True)

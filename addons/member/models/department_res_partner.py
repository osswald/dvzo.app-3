from odoo import models, fields, api


class DepartmentResPartner(models.Model):
    _name = "member.department_res_partner"
    _description = "Department Res Partner"

    name = fields.Char(compute='_compute_department_name', store=True)
    person = fields.Many2one("res.partner", required=True)
    department = fields.Many2one("member.department", required=True)
    department_type = fields.Many2one("member.department_type", required=True)

    @api.depends('department', 'department_type')
    def _compute_department_name(self):
        for record in self:
            record.name = f"{record.department.name} - {record.department_type.name}"

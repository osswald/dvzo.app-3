from odoo import fields, models, api


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
    departments = fields.Text(compute='_compute_departments')
    membership_id = fields.Char("Membership ID")
    department_ids = fields.One2many("member.department_res_partner", "person", string="Departments")

    @api.depends('department_ids')
    def _compute_departments(self):
        for partner in self:
            department_lines = []
            for department_res_partner in partner.department_ids:
                department_line = department_res_partner.name
                department_lines.append(department_line)
            partner.departments = '\n'.join(department_lines)

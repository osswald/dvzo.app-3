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
    membership_ids = fields.One2many("member.membership", "res_partner", string="Memberships")
    mailing_ids = fields.Many2many("member.mailing")
    department_hidden = fields.Many2many("member.department", relation="rel_partner_department_hidden",
                                         column1="partner_id", column2="department_id",
                                         compute="_compute_department_hidden", store=True, string="Department member")
    department_admin = fields.Many2many("member.department", relation="rel_partner_department_admin",
                                        column1="partner_id", column2="department_id",
                                        compute="_compute_department_admin", store=True, string="Department Admin")

    @api.depends('department_ids')
    def _compute_departments(self):
        for partner in self:
            department_lines = []
            for department_res_partner in partner.department_ids:
                department_line = department_res_partner.name
                department_lines.append(department_line)
            partner.departments = '\n'.join(department_lines)

    @api.depends('department_ids')
    def _compute_department_hidden(self):
        for partner in self:
            partner.department_hidden = partner.department_ids.mapped('department')

    @api.depends('department_ids')
    def _compute_department_admin(self):
        for partner in self:
            partner.department_admin = partner.department_ids.filtered(lambda r: r.department_type.admin).mapped(
                'department')

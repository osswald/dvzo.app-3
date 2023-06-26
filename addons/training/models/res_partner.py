from odoo import fields, models, api


class Partner(models.Model):
    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = "res.partner"

    # --------------------------------------- Fields Declaration ----------------------------------

    medical_assessment_valid_until = fields.Date("Medical assessment valid until",
                                                 compute="_compute_medical_valid_until", store=True)
    license_valid_until = fields.Date("License valid until")
    exam_valid_until = fields.Date("Exam valid until", compute="_compute_exam_valid_until", store=True)
    has_locomotive = fields.Boolean("Locomotive knowledge")
    license_nr = fields.Char("License number")
    railway_company = fields.Char("Railway company (Employer)")

    # Relational
    locomotive = fields.Many2many("training.vte.locomotive")
    training_ids = fields.One2many("training.participant", "participant", string="Training")
    medical_assessment_ids = fields.One2many("training.medical_assessment", "person", string="Medical assessment")
    exam_ids = fields.One2many("training.exam", "person", string="Exams")
    in_training_ids = fields.Many2many(
        'res.partner.category',
        'partner_in_training_rel',
        'partner_id',
        'category_id',
        string='In training'
    )

    @api.depends('exam_ids.valid_until')
    def _compute_exam_valid_until(self):
        for partner in self:
            highest_valid_until = False
            for exam in partner.exam_ids:
                if not highest_valid_until or exam.valid_until > highest_valid_until:
                    highest_valid_until = exam.valid_until
            partner.exam_valid_until = highest_valid_until

    @api.depends('medical_assessment_ids.valid_until')
    def _compute_medical_valid_until(self):
        for partner in self:
            highest_valid_until = False
            for exam in partner.medical_assessment_ids:
                if not highest_valid_until or exam.valid_until > highest_valid_until:
                    highest_valid_until = exam.valid_until
            partner.medical_assessment_valid_until = highest_valid_until

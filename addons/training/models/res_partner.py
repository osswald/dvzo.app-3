from odoo import fields, models, api


class Partner(models.Model):
    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = "res.partner"
    _order = "lastname,firstname"

    # --------------------------------------- Fields Declaration ----------------------------------

    medical_assessment_valid_until = fields.Date(
        "Medical assessment valid until",
        compute="_compute_medical_valid_until",
        store=True,
        groups="training.group_training_readonly_all, training.group_training_manager"
    )
    license_valid_until = fields.Date(
        "License valid until",
        groups="training.group_training_readonly_all, training.group_training_manager"
    )
    exam_valid_until = fields.Date(
        "Exam valid until",
        compute="_compute_exam_valid_until",
        store=True,
        groups="training.group_training_readonly_all, training.group_training_manager"
    )
    has_locomotive = fields.Boolean(
        "Locomotive knowledge",
        groups="training.group_training_readonly_all, training.group_training_manager"
    )
    license_nr = fields.Char(
        "License number",
        groups="training.group_training_readonly_all, training.group_training_manager"
    )
    railway_company = fields.Char(
        "Railway company (Employer)",
        groups="training.group_training_readonly_all, training.group_training_manager"
    )

    # Relational
    locomotive = fields.Many2many(
        "training.vte.locomotive",
        groups="training.group_training_readonly_all, training.group_training_manager"
    )
    training_ids = fields.One2many(
        "training.participant",
        "participant",
        string="Training",
        groups="training.group_training_readonly_courses, training.group_training_teacher"
    )
    medical_assessment_ids = fields.One2many(
        "training.medical_assessment",
        "person",
        string="Medical assessment",
        groups="training.group_training_readonly_all, training.group_training_manager"
    )
    exam_ids = fields.One2many(
        "training.exam",
        "person",
        string="Exams",
        groups="training.group_training_readonly_all, training.group_training_manager"
    )
    minimal_hours_ids = fields.One2many(
        "training.min_hours",
        "person",
        string="Minimal hours",
    )
    in_training_ids = fields.Many2many(
        'res.partner.category',
        'partner_in_training_rel',
        'partner_id',
        'category_id',
        string='In training'
    )

    trainer_ids = fields.Many2many(
        'res.partner.category',
        'partner_trainer_rel',
        'partner_id',
        'category_id',
        string='Trainer'
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

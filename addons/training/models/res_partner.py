from odoo import fields, models


class Partner(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = "res.partner"

    # --------------------------------------- Fields Declaration ----------------------------------

    medical_assessment_valid_until = fields.Date("Medical assessment valid until")
    license_valid_until = fields.Date("License valid until")
    exam_valid_until = fields.Date("Exam valid until")
    has_locomotive = fields.Boolean("Locomotive knowledge")

    # Relational
    locomotive = fields.Many2many("training.vte.locomotive")
    training_ids = fields.One2many("training.participant", "participant", string="Training")
    medical_assessment_ids = fields.One2many("training.medical_assessment", "person", string="Medical assessment")
    exam_ids = fields.One2many("training.exam", "person", string="Exams")

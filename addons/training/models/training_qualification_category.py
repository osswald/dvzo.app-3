from odoo import models, fields


class TrainingQualificationCategory(models.Model):
    _name = "training.qualification.category"
    _description = "Qualification Category"

    name = fields.Char("Label", required=True)
    type = fields.Many2one("training.qualification.type", required=True)

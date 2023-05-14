from odoo import models, fields


class TrainingQualificationType(models.Model):
    _name = "training.qualification.type"
    _description = "Qualification Type"

    name = fields.Char("Label", required=True)

from odoo import models, fields


class TrainingQualification(models.Model):
    _name = "training.qualification"
    _description = "Qualification"

    name = fields.Char("Label", required=True)
    description = fields.Text("Description")
    type = fields.Many2one("training.qualification.type", required=True)
    valid_years = fields.Integer("Valid (Years)", default=5)
    category = fields.Many2one("training.qualification.category", required=True)

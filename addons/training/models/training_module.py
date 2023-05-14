from odoo import models, fields


class TrainingModule(models.Model):
    _name = "training.module"
    _description = "Modules in training"

    name = fields.Char("Short name", required=True)
    label = fields.Char("Label", required=True)
    training_ids = fields.One2many("training.training", "module", string="Trainings")

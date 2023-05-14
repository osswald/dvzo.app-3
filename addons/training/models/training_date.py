from odoo import models, fields


class TrainingDate(models.Model):
    _name = "training.date"
    _description = "Dates for trainings"

    start = fields.Datetime("Start", required=True)
    end = fields.Datetime("End", required=True)
    name = fields.Char("Label")
    responsible = fields.Many2one("res.partner", string="Responsable",  copy=False, required=True)
    training = fields.Many2one("training.training", required=True, readonly=True)

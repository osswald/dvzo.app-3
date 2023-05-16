from odoo import models, fields


class TrainingVteLocomotive(models.Model):
    _name = "training.vte.locomotive"
    _description = "VTE Locomotive"

    name = fields.Char("Label", required=True)

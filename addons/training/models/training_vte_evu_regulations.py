from odoo import models, fields


class TrainingVteEvuRegulations(models.Model):
    _name = "training.vte.evu.regulations"
    _description = "VTE EVU regulations"

    name = fields.Char("Label", required=True)

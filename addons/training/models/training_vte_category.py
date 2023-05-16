from odoo import models, fields


class TrainingVteCategory(models.Model):
    _name = "training.vte.category"
    _description = "VTE category"

    name = fields.Char("Label", required=True)

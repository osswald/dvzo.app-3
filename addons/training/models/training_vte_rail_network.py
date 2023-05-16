from odoo import models, fields


class TrainingVteRailNetwork(models.Model):
    _name = "training.vte.rail.network"
    _description = "VTE rail network"

    name = fields.Char("Label", required=True)

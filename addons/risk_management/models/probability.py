from odoo import models, fields, api


class Probability(models.Model):
    _name = "risk_management.probability"
    _description = "Probability"

    name = fields.Char("Label", required=True)

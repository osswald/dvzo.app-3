from odoo import models, fields


class RailwayCompany(models.Model):
    _name = "train_management.railway_company"
    _description = "Railway company"
    _order = "name"

    name = fields.Char("Label", required=True)
    debi_code = fields.Char("Debi-Code")

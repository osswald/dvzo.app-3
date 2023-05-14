from odoo import models, fields


class KeyLending(models.Model):
    _name = "key_management.lending"
    _description = "Key lending"

    lender = fields.Many2one("res.partner", string="Lender",  copy=False, required=True)
    key = fields.Many2one("key_management.key", required=True)
    lending_date = fields.Date(copy=False, default=fields.Date.today())
    return_date = fields.Date(copy=False)


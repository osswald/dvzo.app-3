from odoo import models, fields, api


class KeyLending(models.Model):
    _name = "key_management.lending"
    _description = "Key lending"
    _rec_name = "computed_name"

    lender = fields.Many2one("res.partner", string="Lender",  copy=False, required=True)
    key = fields.Many2one("key_management.key", required=True)
    lending_date = fields.Date(copy=False, default=fields.Date.today())
    return_date = fields.Date(copy=False)
    computed_name = fields.Char(compute="_compute_name", store=True)

    @api.depends('lender', 'key')
    def _compute_name(self):
        for record in self:
            if record.lender and record.key:
                record.computed_name = f"{record.key.name} - {record.lender.name}"
            else:
                record.computed_name = record.lender.name

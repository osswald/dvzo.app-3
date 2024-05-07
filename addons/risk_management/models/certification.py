from odoo import models, fields


class Certification(models.Model):
    _name = "risk_management.certification"
    _description = "Certification"

    date = fields.Date(string="Date", default=fields.Date.today)
    end_date = fields.Date(string="End Date")
    checked_by = fields.Many2one("res.partner", string="Checked By", default=lambda self: self.env.user.partner_id.id)
    file = fields.Binary(string="File", attachment=True)
    vendor = fields.Many2one("res.partner", string="Partner ID")

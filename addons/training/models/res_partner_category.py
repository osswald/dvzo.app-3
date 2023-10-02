from odoo import fields, models, api


class PartnerCategory(models.Model):
    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = "res.partner.category"

    # --------------------------------------- Fields Declaration ----------------------------------

    minimal_hours_vte = fields.Integer()
    minimal_hours_zstebv = fields.Integer()
    minimal_shifts = fields.Integer()

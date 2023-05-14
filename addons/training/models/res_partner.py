from odoo import fields, models


class Partner(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = "res.partner"

    # --------------------------------------- Fields Declaration ----------------------------------

    # Relational
    training_ids = fields.One2many("training.participant", "participant", string="Training")

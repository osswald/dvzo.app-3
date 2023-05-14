from odoo import models, fields


class CopyRecipient(models.Model):
    _name = "train_management.copy_recipient"
    _description = "Copy recipient"

    name = fields.Char("Label", required=True)
    email = fields.Char("E-Mail")

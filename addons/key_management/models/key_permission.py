from odoo import models, fields


class KeyPermission(models.Model):
    _name = "key_management.permission"
    _description = "Key permission"

    name = fields.Char("Label", required=True)

from odoo import models, fields


class Key(models.Model):
    _name = "key_management.key"
    _description = "Key"

    name = fields.Char("Number", required=True)
    key_group = fields.Many2one("key_management.group", required=True)

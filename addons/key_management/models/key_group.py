from odoo import models, fields


class KeyGroup(models.Model):
    _name = "key_management.group"
    _description = "Key group"

    short_name = fields.Char("Short Name", required=True)
    name = fields.Char("Label", required=True)
    comment = fields.Html("Comment")
    key_permission = fields.Many2many("key_management.permission")
    key_system = fields.Many2one("key_management.system", required=True)

    key_ids = fields.One2many("key_management.key", "key_group", string="Keys")

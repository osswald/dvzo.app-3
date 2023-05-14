from odoo import models, fields


class KeySystem(models.Model):
    _name = "key_management.system"
    _description = "Key system"

    short_name = fields.Char("Short Name", required=True)
    name = fields.Char("Label", required=True)
    comment = fields.Html("Comment")
    manufacturer = fields.Selection(
        string='Type',
        selection=[
            ('sea', 'SEA'),
            ('keso', 'KESO'),
            ('kaba', 'DormaKABA'),
        ], )


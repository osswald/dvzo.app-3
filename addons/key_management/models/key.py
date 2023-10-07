from odoo import models, fields, api


class Key(models.Model):
    _name = "key_management.key"
    _description = "Key"
    _rec_name = "computed_name"

    name = fields.Char("Number", required=True)
    key_group = fields.Many2one("key_management.group", required=True)
    computed_name = fields.Char(compute="_compute_name", store=True)

    @api.depends('name', 'key_group.name', 'key_group.key_system.name')
    def _compute_name(self):
        for record in self:
            if record.name and record.key_group.name:
                record.computed_name = f"{record.key_group.key_system.name} - {record.key_group.name} - {record.name}"
            else:
                record.computed_name = record.name

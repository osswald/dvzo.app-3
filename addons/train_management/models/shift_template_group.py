from odoo import models, fields


class ShiftTemplateGroup(models.Model):
    _name = "train_management.shift_template_group"
    _description = "Shift template group"

    name = fields.Char("Label", required=True)
    active = fields.Boolean("Active", default=True, copy=False)
    sequence = fields.Integer(string='Sequence', default=1)


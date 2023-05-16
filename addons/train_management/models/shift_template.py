from odoo import models, fields


class ShiftTemplate(models.Model):
    _name = "train_management.shift_template"
    _description = "Shift template"

    name = fields.Char("Shift number", required=True)
    label = fields.Char("Label")
    description = fields.Text()
    category = fields.Many2many("res.partner.category", required=True)
    valid_from = fields.Date()
    valid_until = fields.Date()
    approximate_times = fields.Boolean()
    approximate_start_time = fields.Float()
    approximate_end_time = fields.Float()
    shift_position_ids = fields.One2many("train_management.shift_position", "shift_template", "Shift positions")

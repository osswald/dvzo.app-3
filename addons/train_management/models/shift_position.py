from odoo import models, fields


class ShiftPosition(models.Model):
    _name = "train_management.shift_position"
    _description = "Shift position"
    _order = "sequence"

    name = fields.Char("Label")
    type = fields.Many2one("train_management.shift_position_type", required=True)
    start_time = fields.Float()
    end_time = fields.Float()
    start_station = fields.Many2one("train_management.station")
    end_station = fields.Many2one("train_management.station")
    comment = fields.Text()
    shift_template = fields.Many2one("train_management.shift_template", required=True, readonly=True)
    sequence = fields.Integer(string='Sequence', default=1)

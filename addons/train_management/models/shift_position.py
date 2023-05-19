from odoo import models, fields, api


class ShiftPosition(models.Model):
    _name = "train_management.shift_position"
    _description = "Shift position"
    _order = "sequence"

    name = fields.Char("Label")
    start_time = fields.Float()
    end_time = fields.Float()
    comment = fields.Text()
    sequence = fields.Integer(string='Sequence', default=1)

    shift_position_duration = fields.Float(compute='_compute_shift_position_duration', store=True)

    start_station = fields.Many2one("train_management.station")
    end_station = fields.Many2one("train_management.station")
    type = fields.Many2one("train_management.shift_position_type", required=True)
    shift_template = fields.Many2one("train_management.shift_template", required=True, readonly=True)

    @api.depends('start_time', 'end_time')
    def _compute_shift_position_duration(self):
        for record in self:
            record.shift_position_duration = record.end_time - record.start_time


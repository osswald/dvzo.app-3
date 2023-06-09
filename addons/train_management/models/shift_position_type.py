from odoo import models, fields


class ShiftPositionType(models.Model):
    _name = "train_management.shift_position_type"
    _description = "Shift position type"
    _order = "name"

    name = fields.Char("Label", required=True)
    work_time = fields.Integer("Percentage work time")
    is_work_time = fields.Boolean("Is work time", default=True)

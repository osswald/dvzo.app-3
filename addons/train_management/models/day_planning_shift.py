from odoo import models, fields


class DayPlanningShift(models.Model):
    _name = "train_management.day_planning_shift"
    _description = "Day planning shift"
    _rec_name = 'shift'

    day_planning = fields.Many2one("train_management.day_planning", string="Day planning", required=True)
    shift = fields.Many2one("train_management.shift_template", required=True)
    shift_label = fields.Char(string='Shift Label', related='shift.label', readonly=True)
    person = fields.Many2one("res.partner", string="Person", copy=False)
    comment = fields.Char("Comment")

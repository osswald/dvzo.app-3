from odoo import models, fields, api


class DayPlanningShift(models.Model):
    _name = "train_management.day_planning_shift"
    _description = "Day planning shift"
    _rec_name = 'shift'

    day_planning = fields.Many2one("train_management.day_planning", string="Day planning", required=True)
    day_planning_date = fields.Date("Date", related="day_planning.date")
    shift = fields.Many2one(
        "train_management.shift_template",
        required=True,
        domain="[('valid_from', '<=', day_planning_date), ('valid_until', '>=', day_planning_date)]"
    )
    shift_categories = fields.Many2many(related="shift.category")
    shift_label = fields.Char(string='Shift Label', related='shift.label', readonly=True)
    person = fields.Many2one("res.partner", string="Person", copy=False)
    comment = fields.Char("Comment")
    sequence = fields.Integer(string='Sequence', default=1)


class AddShiftsWizard(models.TransientModel):
    _name = 'train_management.add.shifts.wizard'
    _description = "Add shifts wizard"

    shift_templates = fields.Many2many('train_management.shift_template',
                                       relation="train_management_shift_wizard_templates", string='Shift Templates')

    def add_shifts(self):
        active_day_planning = self.env['train_management.day_planning'].browse(self._context.get('active_id'))
        for template in self.shift_templates:
            day_planning_shift_data = {
                'day_planning': active_day_planning.id,
                'shift': template.id,
            }
            self.env['train_management.day_planning_shift'].create(day_planning_shift_data)
        return {'type': 'ir.actions.act_window_close'}

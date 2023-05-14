from odoo import models, fields


class DayPlanningText(models.Model):
    _name = "train_management.day_planning_text"
    _description = "Day planning text"
    _order = "sequence"

    name = fields.Char("Label", required=True)
    text = fields.Html("Text")
    sequence = fields.Integer(string='Sequence', default=1)
    day_planning = fields.Many2one("train_management.day_planning", required=True, readonly=True)

from odoo import models, fields, api


class DayPlanningShiftOffer(models.Model):
    _name = "train_management.day_planning_shift_offer"
    _description = "Day planning shift offer"
    _rec_name = 'day_planning_shift'

    day_planning_shift = fields.Many2one("train_management.day_planning_shift")
    day_planning = fields.Many2one("train_management.day_planning", compute="_compute_day_planning", store=True)
    day_planning_date = fields.Date("Date", related="day_planning.date")
    person = fields.Many2one("res.partner", string="Person", copy=False)
    comment = fields.Char("Comment")
    offer = fields.Selection(
        selection=[
            ("yes", "Yes"),
            ("possible", "Possible"),
            ("no", "No"),
        ],
        string="Offer",
        default="no",
        required=True,
    )

    @api.depends('day_planning_shift')
    def _compute_day_planning(self):
        for day_planning_shift_offer in self:
            day_planning_shift_offer.day_planning = day_planning_shift_offer.day_planning_shift.day_planning

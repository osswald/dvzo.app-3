from odoo import models, fields


class MinHours(models.Model):
    _name = "training.min_hours"
    _description = "Minimal hours"
    _rec_name = "year"

    year = fields.Integer("Year", required=True)
    person = fields.Many2one("res.partner", required=True)
    min_hours_vte = fields.Integer("Minimal hours VTE")
    min_hours_zstebv = fields.Integer("Minimal hours ZSTEBV")
    hours_worked_vte = fields.Integer("Hours worked VTE")
    hours_worked_zstebv = fields.Integer("Hours worked ZSTEBV")
    hours_planned_vte = fields.Integer("Hours planned VTE")
    hours_planned_zstebv = fields.Integer("Hours planned ZSTEBV")
    goal_reached_vte = fields.Selection(
        selection=[
            ("unknown", "Unknown"),
            ("not_reachable", "Not reachable"),
            ("reachable", "Reachable"),
            ("reached", "Reached"),
        ],
        string="Goal reached VTE",
        default="unknown",
        required=True,
    )
    goal_reached_zstebv = fields.Selection(
        selection=[
            ("unknown", "Unknown"),
            ("not_reachable", "Not reachable"),
            ("reachable", "Reachable"),
            ("reached", "Reached"),
        ],
        string="Goal reached ZSTEBV",
        default="unknown",
        required=True,
    )




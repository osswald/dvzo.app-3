from odoo import fields, models, api
from datetime import date


class Partner(models.Model):
    # ---------------------------------------- Private Attributes ---------------------------------

    _inherit = "res.partner"

    # --------------------------------------- Fields Declaration ----------------------------------

    min_hours_category = fields.Integer(compute='_compute_min_hours_category', default=0)
    min_shifts_category = fields.Integer(compute='_compute_min_shifts_category', default=0)
    hours_worked_current_year = fields.Integer(compute='_compute_hours_worked_current_year', default=0)
    hours_planned_current_year = fields.Integer(compute='_compute_hours_planned_current_year', default=0)
    shifts_worked_current_year = fields.Integer(compute='_compute_shifts_worked_current_year', default=0)
    shifts_planned_current_year = fields.Integer(compute='_compute_shifts_planned_current_year', default=0)
    goal_reached_current_year = fields.Selection(
        selection=[
            ("unknown", "Unknown"),
            ("not_reachable", "Not reachable"),
            ("reachable", "Reachable"),
            ("reached", "Reached"),
        ],
        string="Goal reached VTE",
        default="unknown",
        required=True,
        compute='_compute_goal_reached_current_year'
    )
    hours_worked_last_year = fields.Integer(compute='_compute_hours_worked_last_year', default=0)
    hours_planned_last_year = fields.Integer(readonly=True, default=0)
    shifts_worked_last_year = fields.Integer(compute='_compute_shifts_worked_last_year', default=0)
    shifts_planned_last_year = fields.Integer(readonly=True, default=0)
    goal_reached_last_year = fields.Selection(
        selection=[
            ("unknown", "Unknown"),
            ("not_reachable", "Not reachable"),
            ("reachable", "Reachable"),
            ("reached", "Reached"),
        ],
        string="Goal reached VTE",
        default="unknown",
        required=True,
        compute='_compute_goal_reached_last_year'
    )

    @api.depends('category_id.minimal_hours_vte', 'category_id')
    def _compute_min_hours_category(self):
        for partner in self:
            if partner.category_id:
                partner.min_hours_category = max(
                    category.minimal_hours_vte
                    for category in partner.category_id
                )
            else:
                partner.min_hours_category = 0

    @api.depends('category_id.minimal_shifts', 'category_id')
    def _compute_min_shifts_category(self):
        for partner in self:
            if partner.category_id:
                partner.min_shifts_category = max(
                    category.minimal_shifts
                    for category in partner.category_id
                )
            else:
                partner.min_shifts_category = 0

    @api.depends('shift_ids.shift.time_accountable', 'shift_ids', 'shift_ids.shift')
    def _compute_hours_worked_current_year(self):
        for partner in self:
            current_year = date.today().year
            total_hours = sum(
                shift.shift.time_accountable
                for shift in partner.shift_ids
                if shift.day_planning_date.year == current_year and shift.day_planning_date < date.today()
            )
            partner.hours_worked_current_year = total_hours

    @api.depends('shift_ids.shift.time_accountable', 'shift_ids', 'shift_ids.shift')
    def _compute_hours_planned_current_year(self):
        for partner in self:
            current_year = date.today().year
            total_hours = sum(
                shift.shift.time_accountable
                for shift in partner.shift_ids
                if shift.day_planning_date.year == current_year and shift.day_planning_date >= date.today()
            )
            partner.hours_planned_current_year = total_hours

    @api.depends('shift_ids.shift.time_accountable', 'shift_ids', 'shift_ids.shift')
    def _compute_hours_worked_last_year(self):
        for partner in self:
            current_year = date.today().year
            last_year = current_year - 1
            total_hours = sum(
                shift.shift.time_accountable
                for shift in partner.shift_ids
                if shift.day_planning_date.year == last_year
            )
            partner.hours_worked_last_year = total_hours

    @api.depends('shift_ids.shift.time_accountable', 'shift_ids', 'shift_ids.shift')
    def _compute_shifts_worked_current_year(self):
        for partner in self:
            current_year = date.today().year
            today_date = date.today()

            shifts_worked = partner.shift_ids.filtered(
                lambda shift: shift.day_planning_date.year == current_year
                              and shift.day_planning_date < today_date
            )
            partner.shifts_worked_current_year = len(shifts_worked)

    @api.depends('shift_ids.shift.time_accountable', 'shift_ids', 'shift_ids.shift')
    def _compute_shifts_planned_current_year(self):
        for partner in self:
            current_year = date.today().year
            today_date = date.today()

            shifts_planned = partner.shift_ids.filtered(
                lambda shift: shift.day_planning_date.year == current_year
                              and shift.day_planning_date >= today_date
            )
            partner.shifts_planned_current_year = len(shifts_planned)

    @api.depends('shift_ids.shift.time_accountable', 'shift_ids', 'shift_ids.shift')
    def _compute_shifts_worked_last_year(self):
        for partner in self:
            current_year = date.today().year
            last_year = current_year - 1

            shifts_worked_last_year = partner.shift_ids.filtered(
                lambda shift: shift.day_planning_date.year == last_year
            )
            partner.shifts_worked_last_year = len(shifts_worked_last_year)

    @api.depends(
        'shifts_worked_current_year',
        'shifts_planned_current_year',
        'min_hours_category',
        'min_shifts_category'
    )
    def _compute_goal_reached_current_year(self):
        for partner in self:
            if partner.min_hours_category == 0 and partner.min_shifts_category == 0:
                partner.goal_reached_current_year = 'unknown'
            elif (
                partner.shifts_worked_current_year >= partner.min_shifts_category
                and partner.min_hours_category == 0
            ) or (
                    partner.hours_worked_current_year >= partner.min_hours_category > 0
            ):
                partner.goal_reached_current_year = 'reached'
            elif (
                partner.shifts_worked_current_year + partner.shifts_planned_current_year >= partner.min_shifts_category
                and partner.min_hours_category == 0
            ) or (
                    partner.hours_worked_current_year + partner.hours_planned_current_year >= partner.min_hours_category > 0
            ):
                partner.goal_reached_current_year = 'reachable'
            else:
                partner.goal_reached_current_year = 'not_reachable'

    def _compute_goal_reached_last_year(self):
        for partner in self:
            if partner.min_hours_category == 0 and partner.min_shifts_category == 0:
                partner.goal_reached_last_year = 'unknown'
            elif (
                partner.shifts_worked_last_year >= partner.min_shifts_category
                and partner.min_hours_category == 0
            ) or (
                    partner.hours_worked_last_year >= partner.min_hours_category > 0
            ):
                partner.goal_reached_last_year = 'reached'
            elif (
                partner.shifts_worked_last_year + partner.shifts_planned_last_year >= partner.min_shifts_category
                and partner.min_hours_category == 0
            ) or (
                    partner.hours_worked_last_year + partner.hours_planned_last_year >= partner.min_hours_category > 0
            ):
                partner.goal_reached_last_year = 'reachable'
            else:
                partner.goal_reached_last_year = 'not_reachable'

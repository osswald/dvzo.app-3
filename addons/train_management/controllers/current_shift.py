from odoo.http import request
from odoo.http import Controller
from odoo.http import route
from datetime import date
from werkzeug.exceptions import NotFound


class CurrentShiftController(Controller):

    @route("/my/shift/current/", website=True, auth="user")
    def list_view(self):
        past_dayplanning_shifts = request.env['train_management.day_planning_shift'].sudo().search([
            ("person", "=", request.env.user.partner_id.id),
            ("day_planning_date", ">=", date.today())])
        current_shifts = []
        for day_planning_shift in past_dayplanning_shifts:
            shift = day_planning_shift.shift
            current_shifts.append({
                "day_planning": day_planning_shift.day_planning,
                "shift": shift
                })
        current_shifts = sorted(current_shifts, key=lambda shift: shift['day_planning'].date)
        return request.render("train_management.web_current_shifts_list_view", {
            'current_shifts': current_shifts,
        })


class SingleDayPlanningController(Controller):

    @route("/my/shift/<int:day_planning_id>", website=True, auth="user")
    def single_view(self, day_planning_id):
        day_planning = request.env['train_management.day_planning'].sudo().search([
            ("id", "=", day_planning_id),
        ], limit=1)

        if not day_planning:
            raise NotFound()

        return request.render("train_management.web_single_day_planning_detail_view", {
            'day_planning': day_planning,
        })

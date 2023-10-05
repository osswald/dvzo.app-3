from odoo.http import request
from odoo.http import Controller
from odoo.http import route
from datetime import datetime


class ShiftController(Controller):

    @route("/my/shift/past/", website=True, auth="user")
    def list_view(self):
        past_dayplanning_shifts = request.env['train_management.day_planning_shift'].sudo().search([
            ("person", "=", request.env.user.partner_id.id)])
        past_shifts = []
        for day_planning_shift in past_dayplanning_shifts:
            shift = day_planning_shift.shift
            past_shifts.append({
                "day_planning": day_planning_shift.day_planning,
                "shift": shift
                })
        return request.render("train_management.web_shifts_list_view", {
            'past_shifts': past_shifts,
        })

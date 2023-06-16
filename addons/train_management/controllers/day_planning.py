from odoo import http
from datetime import datetime


class DayPlanningController(http.Controller):

    @http.route("/my/day-planning/", website=True, auth="user")
    def list_view(self):
        day_plannings = http.request.env['train_management.day_planning'].sudo().search(
            [('date', '>=', ((datetime.now()).strftime('%Y-%m-%d')))])
        print("Day Plannings", day_plannings)
        return http.request.render("train_management.web_day_planning_list_view", {
            'day_plannings': day_plannings
        })

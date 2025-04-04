from odoo.http import request
from odoo.http import Controller
from odoo.http import route

from datetime import date
import logging

log = logging.getLogger(__name__)


class ShiftsAllocationController(Controller):

    @route("/my/shifts-allocation/", website=True, auth="user")
    def list_view(self):
        day_plannings = request.env["train_management.day_planning"].sudo().search([
            ("date", ">=", date.today()),
            ("personnel_disposition", "=", "disposed")
        ]).sorted("date")

        entries = []
        for day_planning in day_plannings:
            allocated_shifts = request.env["train_management.day_planning_shift"].sudo().search([
                ("day_planning", "=", day_planning.id),
            ]).sorted("sequence")

            shifts = []
            for shift in allocated_shifts:
                shifts.append({
                    "shift": shift,
                })

                # Add the day planning entry only if there are qualifying shifts
            if shifts:
                entries.append({
                    "day_planning": day_planning,
                    "shifts": shifts,
                })
            log.info(entries)

        return request.render("train_management.web_shifts_allocation_list_view",
                              {"needed_shifts": entries})


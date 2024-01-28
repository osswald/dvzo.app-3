from odoo.http import request
from odoo.http import Controller
from odoo.http import route

from datetime import date
import logging

log  = logging.getLogger(__name__)

class ShiftsNeededController(Controller):

    @route("/my/shifts-needed/", website=True, auth="user")
    def list_view(self):
        day_plannings = request.env["train_management.day_planning"].sudo().search([
            ("date", ">=", date.today()),
            ("personnel_disposition", "=", "open")
            ])

        entries = []
        for day_planning in day_plannings:
            needed_shifts = request.env["train_management.day_planning_shift"].sudo().search([
                ("day_planning", "=", day_planning.id),
                ])
            
            shifts = []
            for shift in needed_shifts:
                offer = request.env["train_management.day_planning_shift_offer"].sudo().search([
                    ("day_planning_shift", "=", shift.id),
                    ("person", "=", request.env.user.partner_id.id),
                ])
                offer = offer[0] if len(offer) > 0 else None
                shifts.append({
                    "shift": shift,
                    "day_planning_shift_offer": offer
                    })

            entries.append({
                "day_planning": day_planning,
                "shifts": shifts,
                })
            log.info(entries)

        return request.render("train_management.web_shifts_needed_list_view",
                {"needed_shifts": entries})

    @route("/my/shifs-needed/set_shift_offer", type="json", methods=["POST"], auth="user")
    def set_shift_offer(self, offer_id, shift_id, choice, comment):
        if offer_id == "new":
            log.info("Creating new shift offer")
            shift_offer = request.env["train_management.day_planning_shift_offer"].create({
                "day_planning_shift": shift_id,
                "day_planning": None,
                "day_planning_date": None,
                "person": request.env.user.partner_id.id,
                "comment": comment,
                "offer": choice
            })
            request.env.cr.commit()
        else:
            shift_offer = request.env["train_management.day_planning_shift_offer"].sudo().search([
                ("id", "=", offer_id),
                ("person", "=", request.env.user.partner_id.id),
            ])
            shift_offer.offer = choice

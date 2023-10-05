from odoo.http import request
from odoo.http import Controller
from odoo.http import route


class ShiftsNeededController(Controller):

    @route("/my/shifts-needed/", website=True, auth="user")
    def list_view(self):
        return request.render("train_management.web_shifts_needed_list_view")

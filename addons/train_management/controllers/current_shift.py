from odoo.http import request
from odoo.http import Controller
from odoo.http import route


class CurrentShiftController(Controller):

    @route("/my/shift/current/", website=True, auth="user")
    def list_view(self):
        return request.render("train_management.web_current_shifts_list_view")

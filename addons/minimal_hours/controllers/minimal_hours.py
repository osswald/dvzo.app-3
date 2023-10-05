from odoo.http import request
from odoo.http import Controller
from odoo.http import route


class MinimalHoursController(Controller):

    @route("/my/hours", website=True, auth="user")
    def list_view(self):
        return request.render("minimal_hours.web_minimal_hours_list_view")

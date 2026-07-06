from odoo import models, fields


class StopCode(models.Model):
    _name = "train_management.stop_code"
    _description = "Stop code"
    _order = "name"

    name = fields.Char("Label", required=True)
    code = fields.Char("Code", required=True)
    type = fields.Selection(
        selection=[
            ("commercial", "Commercial stop"),
            ("non_commercial", "Non-commercial stop"),
            ("infra", "Infrastructure stop"),
        ],
        string="Type",
        required=True,
    )

    _rec_names_search = ["name", "code"]


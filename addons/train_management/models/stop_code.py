from odoo import models, fields, api


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

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        partners = self.search(['|', ('name', operator, name), ('code', operator, name)])
        return partners.name_get()

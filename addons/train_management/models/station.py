from odoo import models, fields, api


class Station(models.Model):
    _name = "train_management.station"
    _description = "Station"
    _order = "name"

    name = fields.Char("Label", required=True)
    didok = fields.Char("Didok")
    bpuic = fields.Char("BPUIC")
    short_name = fields.Char("Short Name")

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        partners = self.search(['|', ('name', operator, name), ('short_name', operator, name)])
        return partners.name_get()

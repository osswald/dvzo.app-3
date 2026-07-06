from odoo import models, fields


class Station(models.Model):
    _name = "train_management.station"
    _description = "Station"
    _order = "name"

    name = fields.Char("Label", required=True)
    didok = fields.Char("Didok")
    bpuic = fields.Char("BPUIC")
    short_name = fields.Char("Short Name")

    _rec_names_search = ["name", "short_name"]


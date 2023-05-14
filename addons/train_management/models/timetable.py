from odoo import models, fields


class Timetable(models.Model):
    _name = "train_management.timetable"
    _description = "Timetable"

    station = fields.Many2one("train_management.station", required=True)
    train = fields.Many2one("train_management.train", required=True)
    sequence = fields.Integer(string='Sequence', default=1)
    departure_time = fields.Float()
    arrival_time = fields.Float()
    stop_code = fields.Many2one("train_management.stop_code", required=True)

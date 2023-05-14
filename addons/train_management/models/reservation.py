from odoo import models, fields, api


class Reservation(models.Model):
    _name = "train_management.reservation"
    _description = "Reservation"

    name = fields.Char("Label", required=True)
    commission_nr = fields.Char("Commission Nr.")
    phone_number = fields.Char("Phone number")
    email = fields.Char("E-Mail")
    amount = fields.Integer("Amount", required=True)
    type = fields.Selection(
        selection=[
            ("seat", "Seat"),
            ("gastro", "Gastro"),
        ],
        string="Reservation type",
        default="seat",
        copy=False,
        required=True,
    )
    comment = fields.Text("Comment")
    station_ids = fields.Many2many('train_management.station', compute='_compute_station_ids',
                                   string="asdf")
    start_station = fields.Many2one('train_management.station', string='Start Station',
                                    domain="[('id', 'in', station_ids)]")
    start_station_short = fields.Char(related="start_station.short_name", string="Start")
    end_station = fields.Many2one("train_management.station",
                                  domain="[('id', 'in', station_ids)]")
    end_station_short = fields.Char(related="end_station.short_name", string="End")

    train = fields.Many2one("train_management.train")
    day_planning = fields.Many2one("train_management.day_planning", compute="_compute_day_planning", store=True)

    @api.depends('train')
    def _compute_day_planning(self):
        for reservation in self:
            reservation.day_planning = reservation.train.circuit.day_planning

    @api.depends('train.timetable.station')
    def _compute_station_ids(self):
        for rec in self:
            rec.station_ids = rec.train.timetable.sorted("sequence").mapped('station')

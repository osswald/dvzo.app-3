from odoo import models, fields


class TrainVehicle(models.Model):
    _name = "train_management.train_vehicle"
    _description = "Train-Vehicle"
    _rec_name = "vehicle"
    _order = "sequence"

    train = fields.Many2one("train_management.train", required=True)
    vehicle = fields.Many2one("train_management.vehicle", required=True)
    vehicle_type = fields.Selection(
        selection=[
            ("engine", "Engine"),
            ("seat", "Seat"),
            ("gastro", "Gastro"),
            ("luggage", "Luggage"),
            ("cargo", "cargo"),
        ],
        string="Type",
        required=True,
        related="vehicle.type"
    )
    comment = fields.Char()
    sequence = fields.Integer(string='Sequence', default=1)

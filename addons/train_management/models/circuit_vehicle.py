from odoo import models, fields


class CircuitVehicle(models.Model):
    _name = "train_management.circuit_vehicle"
    _description = "Circuit-Vehicle"
    _rec_name = "vehicle"
    _order = "sequence"

    circuit = fields.Many2one("train_management.circuit", required=True)
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

from odoo import models, fields


class Vehicle(models.Model):
    _name = "train_management.vehicle"
    _description = "Vehicle"

    name = fields.Char("Label", required=True)
    ds_id = fields.Char("ds id", help="UUID linking vehicles to the Drehscheibe")
    vehicleNumberNVR = fields.Char("UIC Nr")
    type = fields.Selection(
        selection=[
            ("engine", "Engine"),
            ("seat", "Seat"),
            ("gastro", "Gastro"),
            ("luggage", "Luggage"),
            ("cargo", "cargo"),
        ],
        string="Type",
        required=True,
    )
    weight = fields.Integer()
    length = fields.Integer()


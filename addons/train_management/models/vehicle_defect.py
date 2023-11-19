from datetime import datetime
from odoo import models, fields, api


class VehicleDefect(models.Model):
    _name = "train_management.vehicle_defect"
    _description = "Vehicle defect"

    vehicle = fields.Many2one("train_management.vehicle", required=True)
    date = fields.Date(required=True, default=datetime.today())
    defectTitle = fields.Char(required=True)
    defectDescription = fields.Text()
    trainNumber = fields.Char()
    whereAtVehicle = fields.Selection(
        selection=[
            ("construction", "construction"),
            ("lighting", "lighting"),
            ("labeling", "labeling"),
            ("brakeSystems", "brakeSystems"),
            ("roof", "roof"),
            ("windowsDoors", "windowsDoors"),
            ("heatingOven", "heatingOven"),
            ("interior", "interior"),
            ("loadArea", "loadArea"),
            ("wheelsAxes", "wheelsAxes"),
            ("seatsBenches", "seatsBenches"),
            ("undercarriage", "undercarriage"),
            ("tensileImpactDevices", "tensileImpactDevices"),
            ("remaining", "remaining"),
        ],
        required=True,
    )
    isAccident = fields.Selection(
        selection=[
            ("no", "no"),
            ("accident", "accident"),
            ("disorder", "disorder"),
            ("endangerment", "endangerment"),
        ],
        required=True,
        default="no"
    )
    isSecurityRelated = fields.Boolean()
    status = fields.Selection(
        selection=[
            ("pending", "Pending"),
            ("sent_to_ds", "Sent to DS"),
            ("from_ds", "From DS"),
        ],
        required=True,
        default="pending"
    )
    image1 = fields.Image()
    image2 = fields.Image()
    image3 = fields.Image()
    # TODO:
    #  Add batch job for fetching data from DS
    #  Add functionality for sending new defects to DS

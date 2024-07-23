from ..drehscheibe.api import Drehscheibe
from datetime import datetime
from odoo import models, fields, api

PROPS = ["axleWeight", "brakePadType", "brakingWeight1", "brakingWeightHighG",
         "brakingWeightLowG", "brakingWeightLowP", "cargo", "clearanceProfile",
         "clutchType", "colorBody", "colorFrame", "constructionYear",
         "distanceWheelsets", "entityECM",
         "epoch", "frameWagon", "gauge", "handbrakeWeight", "hasBavLicense",
         "hasBbLicense",
         "hasChangeOver", "hasDynamoGenerator", "hasEboLicense",
         "hasEbvLicense", "hasRicRivTenLicense",
         "historicalDesignation",
         "isBavLimited", "isBbLimited", "isEboLimited", "isEbvLimited",
         "isGuest",
         "isOperational", "isRicRivTenLimited", "lengthOverBuffer",
         "manufacturer", "manufacturerBody",
         "manufacturerFrame", "maxTowWeight", "maximumPayload", "meterWeight",
         "mileage",
         "nbrEmergencyBrakeValve", "note", "numberOfAxes", "numberOfBrakePads",
         "operationalEndDate",
         "outerHeightBody", "outerWidth", "plainOrRollerBearings",
         "specialities", "standardLoadingWeight",
         "stateChangeNote", "suspension", "vehicleGenre", "vehicleNumberNVR",
         "vehicleType",
         "vehicleWeightGross", "vehicleWeightNet", "vmax"]


class Vehicle(models.Model):
    _name = "train_management.vehicle"
    _description = "Vehicle"
    _rec_name = "historicalDesignation"

    name = fields.Char("Label", required=True, compute="_compute_name")
    vehicle_defect_ids = fields.One2many("train_management.vehicle_defect", "vehicle", string="Vehicle defects")
    ds_id = fields.Char("ds id", help="UUID linking vehicles to the Drehscheibe")
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
    axleWeight = fields.Float()
    brakePadType = fields.Char()
    brakingWeight1 = fields.Float()
    brakingWeightHighG = fields.Float()
    brakingWeightLowG = fields.Float()
    brakingWeightLowP = fields.Float()
    cargo = fields.Char()
    clearanceProfile = fields.Char()
    clutchType = fields.Char()
    colorBody = fields.Char()
    colorFrame = fields.Char()
    constructionYear = fields.Integer()
    distanceWheelsets = fields.Char()
    entityECM = fields.Char()
    epoch = fields.Char()
    frameWagon = fields.Char()
    gauge = fields.Char()
    handbrakeWeight = fields.Float()
    hasBavLicense = fields.Boolean()
    hasBbLicense = fields.Boolean()
    hasChangeOver = fields.Boolean()
    hasDynamoGenerator = fields.Boolean()
    hasEboLicense = fields.Boolean()
    hasEbvLicense = fields.Boolean()
    hasRicRivTenLicense = fields.Boolean()
    historicalDesignation = fields.Char()
    isBavLimited = fields.Boolean()
    isBbLimited = fields.Boolean()
    isEboLimited = fields.Boolean()
    isEbvLimited = fields.Boolean()
    isGuest = fields.Boolean()
    isOperational = fields.Boolean()
    isRicRivTenLimited = fields.Boolean()
    lengthOverBuffer = fields.Float()
    manufacturer = fields.Char()
    manufacturerBody = fields.Char()
    manufacturerFrame = fields.Char()
    maxTowWeight = fields.Float()
    maximumPayload = fields.Float()
    meterWeight = fields.Float()
    mileage = fields.Float()
    nbrEmergencyBrakeValve = fields.Text()
    note = fields.Text()
    numberOfAxes = fields.Integer()
    numberOfBrakePads = fields.Integer()
    operationalEndDate = fields.Datetime()
    outerHeightBody = fields.Float()
    outerWidth = fields.Float()
    plainOrRollerBearings = fields.Char()
    specialities = fields.Char()
    standardLoadingWeight = fields.Float()
    stateChangeNote = fields.Text()
    suspension = fields.Char()
    vehicleGenre = fields.Char()
    vehicleNumberNVR = fields.Char()
    vehicleType = fields.Char()
    vehicleWeightGross = fields.Float()
    vehicleWeightNet = fields.Float()
    vmax = fields.Float()
    weight = fields.Float()
    height = fields.Float()
    length = fields.Float()

    def _compute_name(self):
        self.name = self.historicalDesignation



class VehicleBatchUpdate(models.Model):
    _name = "train_management.vehicle_batch_update"
    _description = "Vehicle Batch Update"

    @api.model
    def update_vehicles(self):
        drehscheibe = Drehscheibe()
        response_data = drehscheibe.get_vehicles()
        new_items = []
        for old_item in response_data:
            new_item = {}
            for prop in PROPS:
                if prop == "operationalEndDate":
                    if old_item.get(prop):
                        new_item[prop] = datetime.strptime(
                            old_item.get(prop), "%d.%m.%Y"
                        ).strftime("%Y-%m-%d %H:%M:%S")
                else:
                    new_item[prop] = old_item.get(prop)
            new_item["ds_id"] = old_item.get("id")
            new_item["weight"] = 55
            new_item["height"] = 66
            new_item["length"] = 66
            new_item["name"] = old_item.get("id")
            new_item["type"] = "engine"
            new_items.append(new_item)
        for new_item in new_items:
            db_item = self.env["train_management.vehicle"].sudo().search(
                [("ds_id", "=", new_item["ds_id"])]
            )
            if len(db_item) == 0:
                self.env["train_management.vehicle"].sudo().create(new_item)
            else:
                del new_item["type"]  # don't update type if item already exists
                db_item.write(new_item)
        self.env.cr.commit()

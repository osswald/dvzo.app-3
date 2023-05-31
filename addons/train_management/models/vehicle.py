from ..drehscheibe.api import Drehscheibe
from datetime import datetime
from odoo import models, fields


class Vehicle(models.Model):
    _name = "train_management.vehicle"
    _description = "Vehicle"
    _rec_name = "historicalDesignation"

    props = ["axleWeight", "brakePadType", "brakingWeight1", "brakingWeightHighG",
             "brakingWeightLowG", "brakingWeightLowP", "cargo", "clearanceProfile",
             "clutchType", "colorBody", "colorFrame", "constructionYear", "distanceWheelsets", "entityECM",
             "epoch", "frameWagon", "gauge", "handbrakeWeight", "hasBavLicense", "hasBbLicense",
             "hasChangeOver", "hasDynamoGenerator", "hasEboLicense", "hasEbvLicense", "hasRicRivTenLicense",
             "historicalDesignation",
             "isBavLimited", "isBbLimited", "isEboLimited", "isEbvLimited", "isGuest",
             "isOperational", "isRicRivTenLimited", "lengthOverBuffer", "manufacturer", "manufacturerBody",
             "manufacturerFrame", "maxTowWeight", "maximumPayload", "meterWeight", "mileage",
             "nbrEmergencyBrakeValve", "note", "numberOfAxes", "numberOfBrakePads", "operationalEndDate",
             "outerHeightBody", "outerWidth", "plainOrRollerBearings", "specialities", "standardLoadingWeight",
             "stateChangeNote", "suspension", "vehicleGenre", "vehicleNumberNVR", "vehicleType",
             "vehicleWeightGross", "vehicleWeightNet", "vmax"]

    name = fields.Char("Label", required=True)
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

    def search(self, domain, offset=0, limit=None, order=None, count=False):
        drehscheibe = Drehscheibe()
        id_domain = [d for d in domain if d[0] == "id"]
        if id_domain:
            response_data = drehscheibe.get_data(uuid=id_domain[2])
        else:
            response_data = drehscheibe.get_data()

        new_items = []
        # TODO: clean up
        for old_item in response_data:
            new_item = {}
            for prop in self.props:
                if prop == "operationalEndDate":
                    if old_item.get(prop):
                        new_item[prop] = datetime.strptime(
                            old_item.get(prop), "%Y-%m-%dT%H:%M:%S%z"
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

        return self.env['train_management.vehicle'].sudo().create(
            new_items
        )

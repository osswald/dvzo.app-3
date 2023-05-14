from odoo import models, fields


class Vehicle(models.Model):
    _name = "train_management.vehicle"
    _description = "Vehicle"

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
    nbrEmergencyBrakeValve = fields.Integer()
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

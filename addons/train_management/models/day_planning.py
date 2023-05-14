from odoo import models, fields


class DayPlanning(models.Model):
    _name = "train_management.day_planning"
    _description = "Day planning"
    _order = "date"

    name = fields.Char("Label", required=True)
    date = fields.Date("Date", required=True)
    railway_company = fields.Many2one("train_management.railway_company")
    responsible_phone = fields.Many2one("res.partner", string="Responsible phone")
    type = fields.Selection(
        selection=[
            ("public", "Public"),
            ("extra", "Extra"),
            ("other", "Other"),
        ],
        string="Type",
        default="public",
        required=True,
    )
    slot_ordered_st = fields.Selection(
        selection=[
            ("open", "Open"),
            ("ordered", "Ordered"),
            ("reserved", "Reserved"),
            ("received", "Received"),
            ("not_applicable", "Not applicable"),
        ],
        string="Slot ordered ST",
        default="open",
        required=True,
    )
    slot_ordered_sbb = fields.Selection(
        selection=[
            ("open", "Open"),
            ("ordered", "Ordered"),
            ("reserved", "Reserved"),
            ("received", "Received"),
            ("not_applicable", "Not applicable"),
        ],
        string="Slot ordered SBB",
        default="not_applicable",
        required=True,
    )
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("executed", "Executed"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="draft",
    )
    active = fields.Boolean("Active", default=True)
    billed = fields.Selection(
        selection=[
            ("no", "No"),
            ("yes", "Yes"),
            ("not_applicable", "Not applicable"),
        ],
        string="Billed",
        default="not_applicable",
        copy=False,
        required=True,
    )
    personnel_disposition = fields.Selection(
        selection=[
            ("open", "Open"),
            ("disposed", "Disposed"),
            ("not_applicable", "Not applicable"),
        ],
        string="Personnel disposition",
        default="open",
        copy=False,
        required=True,
    )
    customers = fields.Integer("Customers")
    price = fields.Char("Price")
    comment = fields.Html("Comment")
    post_mortem = fields.Html("Post mortem")
    engine_planning_status = fields.Selection(
        selection=[
            ("open", "Open"),
            ("asked", "Asked"),
            ("ok", "OK"),
        ],
        string="Engine planning status",
        default="open",
        required=True,
        copy=False
    )
    carriage_planning_status = fields.Selection(
        selection=[
            ("open", "Open"),
            ("asked", "Asked"),
            ("ok", "OK"),
        ],
        string="Carriage planning status",
        default="open",
        required=True,
        copy=False
    )
    day_planning_text_ids = fields.One2many("train_management.day_planning_text", "day_planning", string="Texts")
    circuit_ids = fields.One2many("train_management.circuit", "day_planning")
    reservation_ids = fields.One2many("train_management.reservation", "day_planning")
    day_planning_shift_ids = fields.One2many("train_management.day_planning_shift", "day_planning", string="Shifts")

from odoo import models, fields, api
from odoo.exceptions import UserError
from ..drehscheibe.api import Drehscheibe


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
            ("bus", "Bus"),
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
            ("canceled", "Canceled"),
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
    frequency = fields.Integer("Frequency", compute="_compute_total_frequency", store=True)
    distance = fields.Integer("Distance", compute="_compute_total_distance", store=True)
    eating_in_bauma = fields.Integer("Eating in Bauma", compute='_compute_eating_in_bauma', store=True)
    day_planning_text_ids = fields.One2many("train_management.day_planning_text", "day_planning", string="Texts")
    circuit_ids = fields.One2many("train_management.circuit", "day_planning")
    reservation_ids = fields.One2many("train_management.reservation", "day_planning")
    train_ids = fields.One2many("train_management.train", "day_planning_id")
    day_planning_shift_ids = fields.One2many("train_management.day_planning_shift", "day_planning", string="Shifts")
    day_planning_shift_ids_count = fields.Integer(compute="_compute_sum_of_shifts")

    @api.depends('circuit_ids.frequency')
    def _compute_total_frequency(self):
        for day_planning in self:
            day_planning.frequency = sum(circuit.frequency for circuit in day_planning.circuit_ids)

    @api.depends('circuit_ids.distance')
    def _compute_total_distance(self):
        for day_planning in self:
            day_planning.distance = sum(circuit.distance for circuit in day_planning.circuit_ids)

    @api.depends('day_planning_shift_ids', 'day_planning_shift_ids.shift.eating_in_bauma')
    def _compute_eating_in_bauma(self):
        for record in self:
            sum_eating_in_bauma = sum(shift1.shift.eating_in_bauma for shift1 in record.day_planning_shift_ids if
                                      shift1.shift.eating_in_bauma)
            record.eating_in_bauma = sum_eating_in_bauma

    def briefing_recipients(self):
        cc_recipients = self.env['train_management.copy_recipient'].search([])
        recipients = [recipient.email for recipient in cc_recipients]
        people_with_shifts = self.day_planning_shift_ids.person
        for person in people_with_shifts:
            if person.email:
                recipients.append(person.email)
        return ",".join(recipients)

    def post_mortem_recipients(self):
        recipients = self.env['res.partner'].search([("mailing_ids.name", "in", "Nachlese")])
        return ",".join([recipient.email for recipient in recipients if recipient.email])

    def action_confirmed(self):
        # if "executed" in self.mapped("state"):
        #     raise UserError("Executed day plannings can't be confirmed.")
        return self.write({"state": "confirmed"})

    def action_executed(self):
        if "draft" in self.mapped("state"):
            raise UserError("Draft day plannings can't be executed")
        # TODO: add confirmation dialog
        drehscheibe = Drehscheibe()
        drehscheibe.post_day_planning(self)
        return self.write({"state": "executed"})

    def action_view_offers(self):
        res = self.env.ref("train_management.day_planning_shift_action_domain").read()[0]
        return res

    def _compute_sum_of_shifts(self):
        for record in self:
            record.day_planning_shift_ids_count = len(record.day_planning_shift_ids)

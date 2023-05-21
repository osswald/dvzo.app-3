from odoo import models, fields, api


class Train(models.Model):
    _name = "train_management.train"
    _description = "Train"

    name = fields.Char("Name", required=True)
    name_readonly = fields.Char("Label", related="name", readonly=True)
    description = fields.Text("description")
    frequency = fields.Integer("Frequency")
    distance = fields.Integer("Distance")
    start_station = fields.Many2one("train_management.station", compute="_compute_start_station")
    end_station = fields.Many2one("train_management.station", compute="_compute_end_station")
    train_vehicle = fields.One2many("train_management.train_vehicle", "train")
    timetable = fields.One2many("train_management.timetable", "train")
    train_composition = fields.Char(compute="_compute_train_composition")
    circuit = fields.Many2one("train_management.circuit", required=True, readonly=True)
    reservation_ids = fields.One2many("train_management.reservation", "train")
    day_planning_id = fields.Many2one("train_management.day_planning", compute="_compute_day_planning", store=True)

    @api.depends('circuit')
    def _compute_day_planning(self):
        for train in self:
            train.day_planning_id = train.circuit.day_planning

    @api.depends('timetable')
    def _compute_start_station(self):
        for record in self:
            lowest_sequence_record = record.timetable.sorted('sequence')[0] if record.timetable else None
            record.start_station = lowest_sequence_record.station if lowest_sequence_record else ''

    @api.depends('timetable')
    def _compute_end_station(self):
        for record in self:
            highest_sequence_record = record.timetable.sorted('sequence', reverse=True)[0] if record.timetable else None
            record.end_station = highest_sequence_record.station if highest_sequence_record else ''

    @api.depends('train_vehicle')
    def _compute_train_composition(self):
        for train in self:
            vehicle_names = train.train_vehicle.sorted('sequence').mapped('vehicle.name')
            train.train_composition = ', '.join(vehicle_names)

    @api.model
    def create(self, values):
        train = super(Train, self).create(values)

        # Copy the vehicles from the linked circuit to the train
        if train.circuit:
            for circuit_vehicle in train.circuit.circuit_vehicle:
                train_vehicle = self.env['train_management.train_vehicle'].create({
                    'train': train.id,
                    'vehicle': circuit_vehicle.vehicle.id,
                })

        return train

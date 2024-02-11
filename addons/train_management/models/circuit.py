from odoo import models, fields, api


class Circuit(models.Model):
    _name = "train_management.circuit"
    _description = "Circuit"

    name = fields.Char("Label", required=True)
    distance = fields.Integer("distance", compute="_compute_total_distance", store=True)
    frequency = fields.Integer("Frequency", compute="_compute_total_frequency", store=True)
    day_planning = fields.Many2one("train_management.day_planning", required=True, readonly=True)
    circuit_vehicle = fields.One2many("train_management.circuit_vehicle", "circuit")
    train_ids = fields.One2many("train_management.train", "circuit")
    train_composition = fields.Char(compute="_compute_train_composition")

    @api.depends('circuit_vehicle')
    def _compute_train_composition(self):
        for circuit in self:
            vehicle_names = circuit.circuit_vehicle.sorted('sequence').mapped('vehicle.historicalDesignation')
            circuit.train_composition = ', '.join(vehicle_names)

    @api.depends('train_ids.frequency')
    def _compute_total_frequency(self):
        for circuit in self:
            circuit.frequency = sum(train.frequency for train in circuit.train_ids)

    @api.depends('train_ids.distance')
    def _compute_total_distance(self):
        for circuit in self:
            circuit.distance = sum(train.distance for train in circuit.train_ids)

    @api.model
    def write(self, values):
        super(Circuit, self).write(values)
        circuit_vehicle = self.circuit_vehicle
        trains = self.train_ids
        for train in trains:
            self.env['train_management.train_vehicle'].search(
                [('train', '=', train.id)]
            ).unlink()
            for vehicle in circuit_vehicle:
                self.env['train_management.train_vehicle'].create({
                    'vehicle': vehicle.vehicle.id,
                    'train': train.id,
                    'sequence': vehicle.sequence
                })

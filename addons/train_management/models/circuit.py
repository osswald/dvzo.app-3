from odoo import models, fields, api


class Circuit(models.Model):
    _name = "train_management.circuit"
    _description = "Circuit"

    name = fields.Char("Label", required=True)
    distance = fields.Integer("distance")
    frequency = fields.Integer("Frequency")
    day_planning = fields.Many2one("train_management.day_planning", required=True, readonly=True)
    circuit_vehicle = fields.One2many("train_management.circuit_vehicle", "circuit")
    train_ids = fields.One2many("train_management.train", "circuit")
    train_composition = fields.Char(compute="_compute_train_composition")

    @api.depends('circuit_vehicle')
    def _compute_train_composition(self):
        for circuit in self:
            vehicle_names = circuit.circuit_vehicle.sorted('sequence').mapped('vehicle.name')
            circuit.train_composition = ', '.join(vehicle_names)

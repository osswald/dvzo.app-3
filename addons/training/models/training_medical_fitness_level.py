from odoo import models, fields


class TrainingMedicalFitnessLevel(models.Model):
    _name = "training.medical_fitness_level"
    _description = "Medical Fitness Level"

    name = fields.Char("Label", required=True)
    bav_equivalent = fields.Char("BAV equivalent")

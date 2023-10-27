from odoo import models, fields


class TrainingParticipant(models.Model):
    _name = "training.participant"
    _description = "Participants in trainings"
    _rec_name = 'participant'
    _order = 'participant'

    participant = fields.Many2one("res.partner", string="Participant", copy=False, required=True)
    attended = fields.Boolean("Attended")
    passed = fields.Boolean("Passed")
    training = fields.Many2one("training.training", required=True, readonly=True)

from odoo import models, fields


class Training(models.Model):
    _name = "training.training"
    _description = "Trainings"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Short Name", required=True)
    label = fields.Char("Label", required=True)
    module = fields.Many2one("training.module")
    responsible = fields.Many2one("res.partner", string="Responsible",  copy=False, required=True)
    start = fields.Date("Start date")
    end = fields.Date("End date")
    meeting_place = fields.Char("Meeting place")
    take_along = fields.Html("Take along")
    important = fields.Html("Important")
    type = fields.Selection(
        selection=[
            ("training", "Training course"),
            ("further_training", "Further training"),
        ],
        string="Type",
        default="training",
        required=True,
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("planned", "Planned"),
            ("running", "Running"),
            ("archived", "Archived"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="planned",
    )

    participant_ids = fields.One2many("training.participant", "training", "Participants")
    training_date_ids = fields.One2many("training.date", "training", "Dates")

from odoo import models, fields, api


class TrainingExam(models.Model):
    _name = "training.exam"
    _description = "Exam"
    _order = "valid_until"

    type = fields.Many2one("training.qualification.type", required=True)
    category = fields.Many2one("training.qualification.category", domain="[('type', '=', type)]", required=True)
    date = fields.Date("Exam date", required=True)
    valid_until = fields.Date("Valid until", required=True)
    vte_category = fields.Many2one("training.vte.category", string="VTE category")
    vte_rail_network = fields.Many2many("training.vte.rail.network", string="VTE rail network")
    vte_evu_regulations = fields.Many2many("training.vte.evu.regulations", string="VTE EVU regulations")
    vte_locomotive = fields.Many2many("training.vte.locomotive", string="Locomotives")
    person = fields.Many2one("res.partner", required=True, readonly=True)
    competence = fields.Many2many("res.partner.category")

    @api.model
    def create(self, values):
        # Create the training exam record
        exam = super(TrainingExam, self).create(values)

        # Create the activity
        activity = self.env['mail.activity'].create({
            'activity_type_id': self.env.ref('training.mail_activity_type_periodic_exam').id,
            'date_deadline': exam.valid_until,
            'res_id': exam.person.id,
            'res_model_id': self.env['ir.model']._get_id('res.partner'),
            'summary': 'Periodic exam',
            'note': 'Activity for periodic examination.',
        })

        return exam

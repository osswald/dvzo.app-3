from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta


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
        reminder_date = exam.valid_until - relativedelta(months=4)
        valid_until_str = exam.valid_until.strftime('%d.%m.%Y')

        # Create the activity
        activity = self.env['mail.activity'].create({
            'activity_type_id': self.env.ref('training.mail_activity_type_periodic_exam').id,
            'date_deadline': reminder_date,
            'res_id': exam.person.id,
            'res_model_id': self.env['ir.model']._get_id('res.partner'),
            'summary': _('Periodic exam'),
            'note': _('Next periodic exam has to be taken before %s', valid_until_str),
        })

        if exam.person:
            competences = exam.competence.ids
            exam.person.category_id = [(4, competence_id) for competence_id in competences]

            if 'vte_locomotive' in values and values['vte_locomotive']:
                exam.person.has_locomotive = True
                locomotives = exam.vte_locomotive.ids
                exam.person.locomotive = [(4, locomotive_id) for locomotive_id in locomotives]

        return exam

from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta


class TrainingMedicalAssessment(models.Model):
    _name = "training.medical_assessment"
    _description = "Medical assessment"
    _rec_name = "medical_fitness_level"
    _order = "valid_until"

    medical_fitness_level = fields.Many2one("training.medical_fitness_level", required=True)
    limitation = fields.Char("Limitation")
    assessment_date = fields.Date("Assessment date", required=True)
    valid_until = fields.Date("Valid until", required=True)
    assessment_file = fields.Binary(string='Assessment file', attachment=True)
    assessment_file_name = fields.Char(string='File Name')
    person = fields.Many2one("res.partner", "Person", readonly=True)

    def download_assessment_file(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % (self.assessment_file.id,),
            'target': 'new',
        }

    @api.model
    def create(self, values):
        # Create the medical assessment record
        medical_assessment = super(TrainingMedicalAssessment, self).create(values)
        reminder_date = medical_assessment.valid_until - relativedelta(months=4)
        valid_until_str = medical_assessment.valid_until.strftime('%d.%m.%Y')

        # Create the activity
        activity = self.env['mail.activity'].create({
            'activity_type_id': self.env.ref('training.mail_activity_type_medical_assessment').id,
            'date_deadline': reminder_date,
            'res_id': medical_assessment.person.id,
            'res_model_id': self.env['ir.model']._get_id('res.partner'),
            'summary': _('Medical assessment'),
            'note': _('Next medical assessment before %s', valid_until_str),
        })

        return medical_assessment

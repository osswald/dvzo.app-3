from odoo import models, fields


class TrainingMedicalAssessment(models.Model):
    _name = "training.medical_assessment"
    _description = "Medical assessment"
    _rec_name = "medical_fitness_level"
    _order = "valid_until"

    medical_fitness_level = fields.Many2one("training.medical_fitness_level", required=True)
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

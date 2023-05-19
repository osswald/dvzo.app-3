from odoo import models, fields, api


class TrainTemplate(models.Model):
    _name = "train_management.train_template"
    _description = "Train template"
    _rec_name = "label"

    label = fields.Char("Template label", required=True)
    name = fields.Char("Label", required=True)
    description = fields.Text("description")
    start_station = fields.Many2one("train_management.station", compute="_compute_start_station")
    end_station = fields.Many2one("train_management.station", compute="_compute_end_station")
    timetable = fields.One2many("train_management.timetable", "train_template")

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


class CreateTrainWizard(models.TransientModel):
    _name = 'train_management.create.train.wizard'
    _description = "Create train wizard"

    train_templates = fields.Many2many('train_management.train_template',
                                       relation="train_management_train_wizard_templates", string='Train Templates')

    def create_trains(self):
        active_circuit = self.env['train_management.circuit'].browse(self._context.get('active_id'))
        for template in self.train_templates:
            train_data = {
                'name': template.name,
                'circuit': active_circuit.id,
                'description': template.description,
                'start_station': template.start_station,
                'end_station': template.end_station,
            }
            new_train = self.env['train_management.train'].create(train_data)

            # Copy timetables from the template to the new train
            for timetable in template.timetable:
                timetable_data = {
                    'train': new_train.id,
                    'sequence': timetable.sequence,
                    'station': timetable.station.id,
                    'departure_time': timetable.departure_time,
                    'arrival_time': timetable.arrival_time,
                    'stop_code': timetable.stop_code.id,
                }
                self.env['train_management.timetable'].create(timetable_data)
        return {'type': 'ir.actions.act_window_close'}

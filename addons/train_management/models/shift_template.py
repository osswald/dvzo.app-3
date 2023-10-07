from odoo import models, fields, api


class ShiftTemplate(models.Model):
    _name = "train_management.shift_template"
    _description = "Shift template"
    _rec_name = "computed_name"

    name = fields.Char("Shift number", required=True)
    label = fields.Char("Label")
    description = fields.Text()
    valid_from = fields.Date()
    valid_until = fields.Date()
    approximate_times = fields.Boolean()
    approximate_start_time = fields.Float()
    approximate_end_time = fields.Float()
    in_training = fields.Boolean("In training")
    active = fields.Boolean("Active", default=True, copy=False)
    eating_in_bauma = fields.Boolean("Eating in Bauma", default=False, copy=True)
    shift_start = fields.Float(compute="_compute_start_time", store=True)
    shift_end = fields.Float(compute="_compute_end_time", store=True)
    shift_duration = fields.Float(compute="_compute_total_shift_duration", store=True)
    work_duration = fields.Float(compute="_compute_work_duration", store=True)
    time_accountable = fields.Float(compute="_compute_work_duration", store=True,
                                    help="Work time that counts towards the minimal working hours")

    category = fields.Many2many("res.partner.category", required=True)
    shift_position_ids = fields.One2many("train_management.shift_position", "shift_template", "Shift positions")
    computed_name = fields.Char(compute="_compute_name")

    def copy(self, default=None):
        default = default or {}
        default['name'] = self.name + " - Copy"
        default['shift_position_ids'] = [(0, 0, {
            'name': position.name,
            'start_time': position.start_time,
            'end_time': position.end_time,
            'comment': position.comment,
            'sequence': position.sequence,
            'start_station': position.start_station.id,
            'end_station': position.end_station.id,
            'type': position.type.id,
            'shift_template': self.id,
        }) for position in self.shift_position_ids]
        return super(ShiftTemplate, self).copy(default)

    @api.depends('shift_position_ids')
    def _compute_start_time(self):
        for record in self:
            lowest_sequence_record = record.shift_position_ids.sorted('sequence')[0] if record.shift_position_ids else None
            record.shift_start = lowest_sequence_record.start_time if lowest_sequence_record else ''

    @api.depends('shift_position_ids')
    def _compute_end_time(self):
        for record in self:
            highest_sequence_record = record.shift_position_ids.sorted('sequence', reverse=True)[0] if record.shift_position_ids else None
            record.shift_end = highest_sequence_record.end_time if highest_sequence_record else ''

    @api.depends('shift_position_ids')
    def _compute_total_shift_duration(self):
        for record in self:
            record.shift_duration = sum(shift_position_ids.shift_position_duration for shift_position_ids in record.shift_position_ids)

    @api.depends('shift_position_ids')
    def _compute_work_duration(self):
        for record in self:
            work_duration = 0.0
            time_accountable = 0.0

            for shift_position in record.shift_position_ids:
                if shift_position.type.is_work_time:
                    work_duration += shift_position.shift_position_duration
                    time_accountable += shift_position.shift_position_duration * (shift_position.type.work_time / 100)

            record.work_duration = work_duration
            record.time_accountable = time_accountable

    @api.depends('name', 'label')
    def _compute_name(self):
        for record in self:
            if record.name and record.label:
                record.computed_name = f"{record.name} {record.label}"
            else:
                record.computed_name = record.name

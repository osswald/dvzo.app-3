from odoo import models, fields, api


class DayPlanningShift(models.Model):
    _name = "train_management.day_planning_shift"
    _description = "Day planning shift"
    _rec_name = 'shift'

    day_planning = fields.Many2one("train_management.day_planning", string="Day planning", required=True)
    day_planning_date = fields.Date("Date", related="day_planning.date")
    shift = fields.Many2one(
        "train_management.shift_template",
        required=True,
        domain="[('valid_from', '<=', day_planning_date), ('valid_until', '>=', day_planning_date)]"
    )
    shift_categories = fields.Many2many(related="shift.category")
    shift_label = fields.Char(string='Shift Label', related='shift.label', readonly=True)
    person = fields.Many2one("res.partner", string="Person", copy=False)
    comment = fields.Char("Comment")
    day_planning_shift_offer_ids = fields.One2many("train_management.day_planning_shift_offer", "day_planning_shift")
    offers = fields.Html("Offers", compute="_compute_offers")
    sequence = fields.Integer(string='Sequence', default=1)

    @api.depends('day_planning_shift_offer_ids')
    def _compute_offers(self):
        for shift in self:
            offer_lines = []
            for offer in shift.day_planning_shift_offer_ids:
                if offer.offer == "yes":
                    icon = "<i style='color:green;' class='fa fa-check' aria-hidden='true'></i>"
                elif offer.offer == "possible":
                    icon = "<span style='color:orange;'>(<i class='fa fa-check' aria-hidden='true'></i>)</span>"
                else:
                    icon = "<i style='color:red;' class='fa fa-times' aria-hidden='true'></i>"
                offer_line = f"<b>{offer.person.name}</b>: {icon}"
                if offer.comment:
                    offer_line += f" ({offer.comment})"
                offer_lines.append(offer_line)
            shift.offers = '<br>'.join(offer_lines)


class AddShiftsWizard(models.TransientModel):
    _name = 'train_management.add.shifts.wizard'
    _description = "Add shifts wizard"

    shift_templates = fields.Many2many('train_management.shift_template',
                                       relation="train_management_shift_wizard_templates", string='Shift Templates')

    def add_shifts(self):
        active_day_planning = self.env['train_management.day_planning'].browse(self._context.get('active_id'))
        for template in self.shift_templates:
            day_planning_shift_data = {
                'day_planning': active_day_planning.id,
                'shift': template.id,
            }
            self.env['train_management.day_planning_shift'].create(day_planning_shift_data)
        return {'type': 'ir.actions.act_window_close'}

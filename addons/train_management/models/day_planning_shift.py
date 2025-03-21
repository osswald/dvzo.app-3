from datetime import timedelta

from odoo import models, fields, api

import logging

_logger = logging.getLogger(__name__)


class DayPlanningShift(models.Model):
    _name = "train_management.day_planning_shift"
    _description = "Day planning shift"
    _rec_name = 'shift'

    day_planning = fields.Many2one("train_management.day_planning", string="Day planning", required=True)
    day_planning_date = fields.Date("Date", related="day_planning.date")
    shift_template_group = fields.Many2one(related="shift.shift_template_group")
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
                    icon = "&nbsp;<i style='color:green;' class='fa fa-check' aria-hidden='true'></i>&nbsp;"
                elif offer.offer == "possible":
                    icon = "<span style='color:orange;'>(<i class='fa fa-check' aria-hidden='true'></i>)</span>"
                else:
                    icon = "&nbsp;<i style='color:red;' class='fa fa-times' aria-hidden='true'></i>&nbsp;"
                offer_line = f"{icon} <b>{offer.person.name}</b>"
                if offer.comment:
                    offer_line += f" ({offer.comment})"
                offer_lines.append(offer_line)
            shift.offers = '<br>'.join(offer_lines)

    def open_form_view(self):
        return {
            'name': 'Day planning shift Edit',
            'domain': [],
            'res_model': 'train_management.day_planning_shift',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'target': 'current',
        }

    def send_shift_emails(self):
        # Get current date
        now = fields.Datetime.now()

        # Calculate date 24 hours ago
        date_24_hours_ago = now - timedelta(days=1)

        # Get day_planning_shift records created in last 24 hours
        day_planning_shifts = self.env['train_management.day_planning_shift'].search([
            ('create_date', '>=', date_24_hours_ago),
            ('person', '=', False),
            ('day_planning.personnel_disposition', '!=', 'disposed'),
        ], order='day_planning_date')

        if not day_planning_shifts:
            _logger.warning('No new shifts available. No mails will be sent.')
            return

        shift_templates = day_planning_shifts.mapped('shift')
        category_ids = shift_templates.mapped('category')

        # Get res_partners related to these categories
        res_partners = self.env['res.partner'].search([
            ('category_id', 'in', category_ids.ids)
        ])

        # Send email
        template_id = self.env.ref(
                 'train_management.mail_template_new_shifts_available')

        # Send one email per res_partner
        for partner in res_partners:
            eligible_shift_templates = shift_templates.filtered(
                lambda r: any(category.id in partner.category_id.ids for category in r.category))

            # Filter day_planning_shifts based on eligible_shift_templates
            eligible_shift_records = day_planning_shifts.filtered(
                lambda r: r.shift in eligible_shift_templates)

            # Prepare email data
            template = template_id.with_context(shift_records=eligible_shift_records,
                                                email_to=partner.email,
                                                firstname=partner.firstname)

            # Send mail
            template.send_mail(eligible_shift_records[0].id, force_send=True)


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

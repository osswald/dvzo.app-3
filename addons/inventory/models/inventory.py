from datetime import timedelta

from odoo import models, fields, api, exceptions

import logging

_logger = logging.getLogger(__name__)


class Inventory(models.Model):
    _name = "inventory.inventory"
    _description = "Inventory"

    name = fields.Char("Label", required=True)
    computed_nr = fields.Char(compute="_compute_computed_nr", store=True, readonly=True)
    inventory_nr = fields.Integer("Inventory Number")
    serial_number = fields.Char("Serial Number")
    place = fields.Many2one("inventory.place", required=True)
    type = fields.Many2one("inventory.type", required=True)
    manufacturer = fields.Many2one("inventory.manufacturer")
    location = fields.Many2one("inventory.location")
    status = fields.Many2one("inventory.status", required=True, default=lambda self: self._get_default_status())
    date_bought = fields.Date("Date bought")
    date_calibrated = fields.Date("Date calibrated", compute="_compute_latest_check_date")
    date_expires = fields.Date("Date expires", compute="_compute_status_and_latest_expiry_date", store=True)
    responsible = fields.Many2one("res.partner")
    checks = fields.One2many("inventory.check", "inventory_id")
    active = fields.Boolean("Active", default=True)
    not_monitored = fields.Boolean("Not monitored", default=False)
    is_record_saved = fields.Boolean(compute='_compute_is_record_saved')

    @api.depends('create_date')
    def _compute_is_record_saved(self):
        for record in self:
            record.is_record_saved = bool(record.create_date)

    @api.model
    def _get_default_status(self):
        default_status = "OK"
        inventory_status = self.env['inventory.status'].search([('name', '=', default_status)], limit=1)
        if inventory_status:
            return inventory_status.id
        else:
            # Fallback value in case "ok" is not found in inventory.status
            return default_status

    @api.depends('type', 'place', 'inventory_nr')
    def _compute_computed_nr(self):
        for record in self:
            type_code = record.type.short_name if record.type else 'X'
            place_code = record.place.short_name if record.place else 'X'
            inventory_nr_padded = str(record.inventory_nr).zfill(4)
            record.computed_nr = f"{type_code}-{place_code}{inventory_nr_padded}"

    _sql_constraints = [
        ('unique_computed_nr', 'UNIQUE(computed_nr)', 'The computed number must be unique.'),
    ]

    @api.constrains('computed_nr')
    def _check_unique_computed_nr(self):
        for record in self:
            if record.computed_nr:
                existing_record = self.search([('computed_nr', '=', record.computed_nr), ('id', '!=', record.id)])
                if existing_record:
                    raise exceptions.ValidationError("The computed number must be unique.")

    @api.model
    def action_open_inventory_check(self, ids, context={}):
        for id in ids:
            wizard = self.env['inventory.check.wizard'].create({
                'inventory_id': id,
            })

            return {
                'name': 'Create Inventory Check',
                'type': 'ir.actions.act_window',
                'res_model': 'inventory.check.wizard',
                'res_id': wizard.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
                'views': [(self.env.ref('inventory.view_inventory_check_wizard').id, 'form')],
            }

    @api.depends('checks.date')
    def _compute_latest_check_date(self):
        for record in self:
            latest_check = record.checks.sorted('id', reverse=True)[:1]
            record.date_calibrated = latest_check.date if latest_check else False

    @api.depends('checks.expiry_date')
    def _compute_status_and_latest_expiry_date(self):
        for record in self:
            latest_check = record.checks.sorted('id', reverse=True)[:1]
            expiry_date = latest_check.expiry_date if latest_check else False
            record.date_expires = expiry_date
            if expiry_date:
                today = fields.Date.today()
                if expiry_date > today:
                    record.status = self.env['inventory.status'].search([('name', '=', 'OK')], limit=1)
                elif expiry_date < today:
                    record.status = self.env['inventory.status'].search([('name', '=', 'Abgelaufen')], limit=1)
                else:  # if expiry_date is today
                    record.status = self.env['inventory.status'].search([('name', '=', 'OK')], limit=1)
            else:
                record.status = self.env['inventory.status'].search([('name', '=', 'Nicht verfügbar')], limit=1)

    @api.model
    def update_inventory_status(self):
        for record in self.search([]):
            expiry_date = record.date_expires
            if expiry_date:
                today = fields.Date.today()
                if expiry_date > today:
                    record.status = self.env['inventory.status'].search([('name', '=', 'OK')], limit=1)
                elif expiry_date < today:
                    record.status = self.env['inventory.status'].search([('name', '=', 'Abgelaufen')], limit=1)
                else:
                    record.status = self.env['inventory.status'].search([('name', '=', 'OK')], limit=1)
            else:
                record.status = self.env['inventory.status'].search([('name', '=', 'Nicht verfügbar')], limit=1)

    @api.model
    def generate_expiry_reminders(self):
        today = fields.Date.today()
        fortnight = today + timedelta(days=14)

        inventories = self.search([
            ('date_expires', '>=', today),
            ('date_expires', '<=', fortnight),
        ])

        _logger.warning('Generating expiry reminders')
        _logger.info(inventories)

        # Group inventories by responsible person
        grouped_inventories = {}
        for inv in inventories:
            if inv.responsible not in grouped_inventories:
                grouped_inventories[inv.responsible] = []
            grouped_inventories[inv.responsible].append(inv)

        # Generate email for each responsible person
        template_id = self.env.ref(
            'inventory.mail_template_reminder').id  # assuming 'inventory.mail_template_reminder' is your email template's external ID
        for responsible, invs in grouped_inventories.items():
            if responsible and responsible.email:  # ensuring that a responsible person is available and he/she has email
                context = {"inventories": invs}
                _logger.info(context)
                self.env['mail.template'].browse(template_id).with_context(context).send_mail(invs[0].id,force_send=True)

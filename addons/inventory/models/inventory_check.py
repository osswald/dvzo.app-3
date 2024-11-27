from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class InventoryCheck(models.Model):
    _name = "inventory.check"
    _description = "Inventory check"
    _order = 'id desc'

    date = fields.Date("Date", required=True, default=fields.Date.today)
    expiry_date = fields.Date(
        "Expiry Date", required=True, default=lambda self: fields.Date.today() + relativedelta(years=1)
    )
    note=fields.Char("Remark")
    checked_by = fields.Many2one("res.partner", default=lambda self: self.env.user.partner_id.id)
    inventory_id = fields.Many2one("inventory.inventory")


class InventoryCheckWizard(models.TransientModel):
    _name = 'inventory.check.wizard'

    inventory_id = fields.Many2one('inventory.inventory')
    date = fields.Date('Date', required=True, default=fields.Date.today)
    expiry_date = fields.Date(
        'Expiry Date', required=True, default=lambda self: fields.Date.today() + relativedelta(years=1)
    )
    note = fields.Char("Remark")
    checked_by = fields.Many2one("res.partner", default=lambda self: self.env.user.partner_id.id)

    def action_create_inventory_check(self):
        # This method will be called when the user clicks on the wizard's Create button
        self.ensure_one()
        new_check = self.env['inventory.check'].create({
            'inventory_id': self.inventory_id.id,
            'date': self.date,
            'expiry_date': self.expiry_date,
            'note': self.note,
            'checked_by': self.checked_by.id,
        })

        action = self.sudo().env.ref('inventory.inventory_after_wizard_action').read()[0]
        action.update({
            'view_mode': 'form',
            'res_id': new_check.inventory_id.id,
            'target': 'current',
        })
        return action

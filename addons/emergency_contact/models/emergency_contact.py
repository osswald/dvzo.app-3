from odoo import models, fields, api


class EmergencyContact(models.Model):
    _name = "emergency_contact.emergency_contact"
    _description = "Emergency_contact"

    name = fields.Char("Name", required=True)
    relation = fields.Char("Relation", required=True)
    phone = fields.Char("Phone number", required=True)
    res_partner = fields.Many2one("res.partner", string="Contact", required=True)

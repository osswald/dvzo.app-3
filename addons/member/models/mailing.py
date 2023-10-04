from odoo import models, fields, api


class Mailing(models.Model):
    _name = "member.mailing"
    _description = "Mailing"

    name = fields.Char(required=True)

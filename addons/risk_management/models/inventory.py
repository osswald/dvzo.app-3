from odoo import models, fields

import logging

_logger = logging.getLogger(__name__)


class Inventory(models.Model):
    _inherit = "inventory.inventory"

    risk_assessment_ids = fields.One2many('risk_management.risk_assessment', 'inventory_ids')

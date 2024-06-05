from odoo import models, fields, api


class RiskAssessment(models.Model):
    _name = "risk_management.risk_assessment"
    _description = "Risk assessment"

    name = fields.Char("Label", required=True)
    date = fields.Date("Created on", required=True, default=fields.Date.today)
    reference = fields.Char("Reference / Event")
    task = fields.Char("Task")
    hazard = fields.Html("Hazard")
    protection_objective = fields.Char("Protection objective")
    intervention = fields.Char("Intervention")
    due_date = fields.Date("Due date")
    end_date = fields.Date("End date")
    active = fields.Boolean("Active", default=True)

    extent_of_damage_hazard_identification = fields.Many2one("risk_management.extent_of_damage")
    probability_hazard_identification = fields.Many2one("risk_management.probability")
    risk_zone_hazard_identification = fields.Many2one("risk_management.risk_zone")
    extent_of_damage_risk_reduction = fields.Many2one("risk_management.extent_of_damage")
    probability_hazard_risk_reduction = fields.Many2one("risk_management.probability")
    risk_zone_hazard_risk_reduction = fields.Many2one("risk_management.risk_zone")
    department = fields.Many2many("risk_management.department")
    residual_risk = fields.Many2one("risk_management.residual_risk")

    damage_ids = fields.Many2many("risk_management.damage")

    asset_id = fields.Many2one("risk_management.asset")
    inventory_ids = fields.Many2many("inventory.inventory")
    business_risk_id = fields.Many2one("risk_management.business_risk")
    res_partner_id = fields.Many2one("res.partner")
    checks = fields.One2many("risk_management.check", "risk_assessment_id")

    # TODO: add domain to restrict to businesses
    # TODO: compute risk_zone

    @api.model
    def action_open_risk_assessment_check(self, ids, context={}):
        for id in ids:
            wizard = self.env['risk_management.check.wizard'].create({
                'risk_assessment_id': id,
            })

            return {
                'name': 'Create Risk Assessment Check',
                'type': 'ir.actions.act_window',
                'res_model': 'risk_management.check.wizard',
                'res_id': wizard.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
                'views': [(self.env.ref('risk_management.view_risk_assessment_check_wizard').id, 'form')],
            }


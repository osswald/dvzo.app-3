from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class RiskAssessmentCheck(models.Model):
    _name = "risk_management.check"
    _description = "Risk assessment check"
    _order = 'id desc'

    date = fields.Date("Date", required=True, default=fields.Date.today)
    expiry_date = fields.Date(
        "Expiry Date", required=True, default=lambda self: fields.Date.today() + relativedelta(years=1)
    )
    checked_by = fields.Many2one("res.partner", default=lambda self: self.env.user.partner_id.id)
    risk_assessment_id = fields.Many2one("risk_management.risk_assessment")


class RiskAssessmentCheckWizard(models.TransientModel):
    _name = 'risk_management.check.wizard'

    risk_assessment_id = fields.Many2one('risk_management.risk_assessment')
    date = fields.Date('Date', required=True, default=fields.Date.today)
    expiry_date = fields.Date(
        'Expiry Date', required=True, default=lambda self: fields.Date.today() + relativedelta(years=1)
    )
    checked_by = fields.Many2one("res.partner", default=lambda self: self.env.user.partner_id.id)

    def action_create_risk_assessment_check(self):
        # This method will be called when the user clicks on the wizard's Create button
        self.ensure_one()
        new_check = self.env['risk_management.check'].create({
            'risk_assessment_id': self.risk_assessment_id.id,
            'date': self.date,
            'expiry_date': self.expiry_date,
            'checked_by': self.checked_by.id,
        })

        action = self.sudo().env.ref('risk_management.risk_assessment_after_wizard_action').read()[0]
        action.update({
            'view_mode': 'form',
            'res_id': new_check.risk_assessment_id.id,
            'target': 'current',
        })
        return action

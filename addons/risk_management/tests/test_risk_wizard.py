from datetime import date, timedelta

from odoo.tests import tagged

from .common import RiskManagementTestCommon


@tagged("post_install", "-at_install")
class TestRiskWizard(RiskManagementTestCommon):
    def test_action_create_risk_assessment_check(self):
        check_date = date(2024, 3, 1)
        expiry_date = check_date + timedelta(days=365)
        wizard = self.env["risk_management.check.wizard"].create(
            {
                "risk_assessment_id": self.risk_assessment.id,
                "date": check_date,
                "expiry_date": expiry_date,
                "checked_by": self.env.user.partner_id.id,
            }
        )
        action = wizard.action_create_risk_assessment_check()
        check = self.env["risk_management.check"].search(
            [("risk_assessment_id", "=", self.risk_assessment.id)]
        )
        self.assertEqual(len(check), 1)
        self.assertEqual(check.date, check_date)
        self.assertEqual(check.expiry_date, expiry_date)
        self.assertEqual(action["res_model"], "risk_management.risk_assessment")
        self.assertEqual(action["res_id"], self.risk_assessment.id)
        self.assertEqual(action["view_mode"], "form")

    def test_action_open_risk_assessment_check(self):
        action = self.risk_assessment.action_open_risk_assessment_check(
            [self.risk_assessment.id]
        )
        wizard = self.env["risk_management.check.wizard"].browse(action["res_id"])
        self.assertEqual(wizard.risk_assessment_id, self.risk_assessment)
        self.assertEqual(action["res_model"], "risk_management.check.wizard")
        self.assertEqual(action["view_mode"], "form")

from datetime import date

from odoo.tests.common import TransactionCase


class RiskManagementTestCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.risk_assessment = cls.env["risk_management.risk_assessment"].create(
            {
                "name": "Test Risk Assessment",
                "date": date(2024, 1, 1),
            }
        )

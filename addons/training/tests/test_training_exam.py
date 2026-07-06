from datetime import date

from dateutil.relativedelta import relativedelta
from odoo.tests import tagged

from .common import TrainingTestCommon


@tagged("post_install", "-at_install")
class TestTrainingExam(TrainingTestCommon):
    def test_exam_create_activity(self):
        valid_until = date(2025, 8, 15)
        self._create_exam(valid_until=valid_until)
        activity = self.env["mail.activity"].search(
            [
                ("res_id", "=", self.partner.id),
                ("res_model", "=", "res.partner"),
            ],
            limit=1,
        )
        self.assertTrue(activity)
        self.assertEqual(
            activity.date_deadline,
            valid_until - relativedelta(months=4),
        )

    def test_exam_create_competence_categories(self):
        self._create_exam()
        self.assertIn(self.competence_category, self.partner.category_id)

    def test_partner_exam_valid_until_compute(self):
        self._create_exam(valid_until=date(2025, 6, 1))
        self._create_exam(valid_until=date(2026, 1, 1))
        self.assertEqual(self.partner.exam_valid_until, date(2026, 1, 1))

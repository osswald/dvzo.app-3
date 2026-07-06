from odoo.tests import tagged

from .common import TrainManagementTestCommon


@tagged("post_install", "-at_install")
class TestShiftTemplate(TrainManagementTestCommon):
    def test_shift_duration_sum(self):
        template = self._create_shift_template()
        self.assertEqual(template.shift_duration, 5.0)

    def test_time_accountable_percentage(self):
        template = self._create_shift_template()
        self.assertEqual(template.work_duration, 4.0)
        self.assertEqual(template.time_accountable, 2.0)

    def test_shift_start_end_from_positions(self):
        template = self._create_shift_template()
        self.assertEqual(template.shift_start, 8.0)
        self.assertEqual(template.shift_end, 13.0)

    def test_shift_computed_name(self):
        template = self._create_shift_template()
        self.assertEqual(template.computed_name, "S1 Morning Shift")

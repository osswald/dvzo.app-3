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

    def test_shift_computed_name_without_label(self):
        template = self._create_shift_template(label=False)
        self.assertEqual(template.computed_name, "S1")

    def test_shift_position_duration(self):
        template = self._create_shift_template()
        position = template.shift_position_ids.filtered(
            lambda p: p.name == "Work block"
        )
        self.assertEqual(position.shift_position_duration, 4.0)

    def test_shift_template_name_search(self):
        template = self._create_shift_template(name="NUM1", label="Night Shift")
        results = self.env["train_management.shift_template"].name_search("Night")
        self.assertIn(template.id, [result[0] for result in results])

    def test_shift_template_copy_duplicates_positions(self):
        template = self._create_shift_template()
        copied = template.copy()
        self.assertEqual(len(copied.shift_position_ids), len(template.shift_position_ids))
        self.assertEqual(copied.name, "S1 - Copy")

from odoo.tests import tagged

from .common import TrainManagementTestCommon


@tagged("post_install", "-at_install")
class TestDayPlanning(TrainManagementTestCommon):
    def test_day_planning_total_frequency_and_distance(self):
        circuit = self._create_circuit()
        self._create_train(circuit, frequency=12, distance=30)
        circuit_b = self._create_circuit(name="Circuit B")
        self._create_train(circuit_b, frequency=8, distance=10)
        self.assertEqual(self.day_planning.frequency, 20)
        self.assertEqual(self.day_planning.distance, 40)

    def test_day_planning_eating_in_bauma(self):
        template_with_meal = self._create_shift_template(
            name="MEAL", label="Meal shift", eating_in_bauma=True
        )
        template_without_meal = self._create_shift_template(
            name="NOMEAL", label="No meal shift", eating_in_bauma=False
        )
        self._create_day_planning_shift(
            self.partner, template_with_meal, person=self.partner
        )
        self._create_day_planning_shift(
            self.partner, template_without_meal, person=self.partner
        )
        self.assertEqual(self.day_planning.eating_in_bauma, 1)

    def test_day_planning_shift_counts(self):
        template = self._create_shift_template()
        self._create_day_planning_shift(self.partner, template)
        self.env["train_management.day_planning_shift"].create(
            {
                "day_planning": self.day_planning.id,
                "shift": template.id,
            }
        )
        circuit = self._create_circuit()
        self._create_train(circuit)
        self.assertEqual(self.day_planning.day_planning_shift_ids_count, 2)
        self.assertEqual(self.day_planning.day_planning_shifts_allocated_count, 1)
        self.assertEqual(self.day_planning.day_planning_train_ids_count, 1)

    def test_briefing_recipients(self):
        self.partner.email = "shift.partner@test.example"
        template = self._create_shift_template()
        self._create_day_planning_shift(self.partner, template)
        self.env["train_management.copy_recipient"].create(
            {"name": "CC Recipient", "email": "cc@test.example"}
        )
        recipients = self.day_planning.briefing_recipients().split(",")
        self.assertIn("shift.partner@test.example", recipients)
        self.assertIn("cc@test.example", recipients)

    def test_get_sorted_shifts_groups_by_template_group(self):
        group_a = self.env["train_management.shift_template_group"].create(
            {"name": "Group A", "sequence": 1}
        )
        group_b = self.env["train_management.shift_template_group"].create(
            {"name": "Group B", "sequence": 2}
        )
        shift_a = self._create_shift_template(
            name="A1", label="Shift A1", shift_template_group=group_a.id
        )
        shift_b = self._create_shift_template(
            name="B1", label="Shift B1", shift_template_group=group_b.id
        )
        shift_other = self._create_shift_template(name="X1", label="Shift X1")
        self._create_day_planning_shift(self.partner, shift_b)
        self._create_day_planning_shift(self.partner, shift_a)
        self._create_day_planning_shift(self.partner, shift_other)
        grouped = self.day_planning.get_sorted_shifts()
        group_keys = list(grouped.keys())
        self.assertEqual(group_keys[0].name, "Group A")
        self.assertEqual(group_keys[1].name, "Group B")
        self.assertEqual(group_keys[2], "Others")

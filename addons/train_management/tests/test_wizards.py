from datetime import date

from odoo.tests import tagged

from .common import TrainManagementTestCommon


@tagged("post_install", "-at_install")
class TestTrainManagementWizards(TrainManagementTestCommon):
    def test_add_shifts_wizard(self):
        template_a = self._create_shift_template(name="S-A", label="Shift A")
        template_b = self._create_shift_template(name="S-B", label="Shift B")
        wizard = self.env["train_management.add.shifts.wizard"].create(
            {
                "shift_templates": [(6, 0, [template_a.id, template_b.id])],
            }
        )
        wizard.with_context(active_id=self.day_planning.id).add_shifts()
        shifts = self.day_planning.day_planning_shift_ids
        self.assertEqual(len(shifts), 2)
        self.assertEqual(shifts.mapped("shift"), template_a | template_b)

    def test_create_trains_wizard(self):
        circuit = self._create_circuit()
        template = self.env["train_management.train_template"].create(
            {
                "label": "Template 1",
                "name": "Morning Express",
                "distance": 42,
                "description": "Test template",
                "reservation_quota": 80,
            }
        )
        self.env["train_management.timetable"].create(
            {
                "train_template": template.id,
                "station": self.station_a.id,
                "stop_code": self.stop_code.id,
                "sequence": 1,
                "departure_time": 8.0,
            }
        )
        self.env["train_management.timetable"].create(
            {
                "train_template": template.id,
                "station": self.station_b.id,
                "stop_code": self.stop_code.id,
                "sequence": 2,
                "arrival_time": 10.0,
            }
        )
        wizard = self.env["train_management.create.train.wizard"].create(
            {"train_templates": [(6, 0, [template.id])]}
        )
        wizard.with_context(active_id=circuit.id).create_trains()
        train = circuit.train_ids
        self.assertEqual(len(train), 1)
        self.assertEqual(train.name, "Morning Express")
        self.assertEqual(train.distance, 42)
        self.assertEqual(len(train.timetable), 2)
        self.assertEqual(train.start_station, self.station_a)
        self.assertEqual(train.end_station, self.station_b)

    def test_add_shift_positions_wizard(self):
        source_template = self._create_shift_template(name="SRC", label="Source")
        target_template = self._create_shift_template(
            name="TGT",
            label="Target",
            time_accountable_positions=[],
        )
        self.assertEqual(len(target_template.shift_position_ids), 0)
        wizard = self.env["train_management.add.shift.positions.wizard"].create(
            {"shift_template": source_template.id}
        )
        wizard.with_context(active_id=target_template.id).add_shift_positions()
        self.assertEqual(
            len(target_template.shift_position_ids),
            len(source_template.shift_position_ids),
        )
        self.assertEqual(
            target_template.shift_position_ids.mapped("name"),
            source_template.shift_position_ids.mapped("name"),
        )

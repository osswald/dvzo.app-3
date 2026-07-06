from unittest.mock import patch

from odoo.exceptions import UserError
from odoo.tests import tagged

from .common import TrainManagementTestCommon


@tagged("post_install", "-at_install")
class TestCircuitTrain(TrainManagementTestCommon):
    def test_train_stations_from_timetable(self):
        circuit = self._create_circuit()
        train = self._create_train(circuit)
        self.env["train_management.timetable"].create(
            {
                "train": train.id,
                "station": self.station_a.id,
                "stop_code": self.stop_code.id,
                "sequence": 1,
            }
        )
        self.env["train_management.timetable"].create(
            {
                "train": train.id,
                "station": self.station_b.id,
                "stop_code": self.stop_code.id,
                "sequence": 2,
            }
        )
        self.assertEqual(train.start_station, self.station_a)
        self.assertEqual(train.end_station, self.station_b)

    def test_train_create_copies_circuit_vehicles(self):
        circuit = self._create_circuit()
        vehicle = self._create_vehicle("Loco 1")
        self.env["train_management.circuit_vehicle"].create(
            {
                "circuit": circuit.id,
                "vehicle": vehicle.id,
                "sequence": 1,
            }
        )
        train = self._create_train(circuit)
        self.assertEqual(len(train.train_vehicle), 1)
        self.assertEqual(train.train_vehicle.vehicle, vehicle)

    def test_circuit_write_syncs_train_vehicles(self):
        circuit = self._create_circuit()
        train = self._create_train(circuit)
        vehicle = self._create_vehicle("Loco 2")
        self.env["train_management.circuit_vehicle"].create(
            {
                "circuit": circuit.id,
                "vehicle": vehicle.id,
                "sequence": 1,
            }
        )
        circuit.write({"name": "Updated Circuit"})
        self.assertEqual(len(train.train_vehicle), 1)
        self.assertEqual(train.train_vehicle.vehicle, vehicle)

    def test_day_planning_confirmed_from_draft(self):
        self.day_planning.action_confirmed()
        self.assertEqual(self.day_planning.state, "confirmed")

    def test_day_planning_executed_from_draft_raises(self):
        with self.assertRaises(UserError):
            self.day_planning.action_executed()

    def test_day_planning_confirmed_from_executed_raises(self):
        self.day_planning.write({"state": "confirmed"})
        with patch(
            "odoo.addons.train_management.models.day_planning.Drehscheibe"
        ) as mock_drehscheibe:
            mock_drehscheibe.return_value.post_day_planning.return_value = None
            self.day_planning.action_executed()
        with self.assertRaises(UserError):
            self.day_planning.action_confirmed()

    @patch("odoo.addons.train_management.models.day_planning.Drehscheibe")
    def test_day_planning_executed_from_confirmed(self, mock_drehscheibe):
        mock_drehscheibe.return_value.post_day_planning.return_value = None
        self.day_planning.action_confirmed()
        self.day_planning.action_executed()
        self.assertEqual(self.day_planning.state, "executed")
        mock_drehscheibe.return_value.post_day_planning.assert_called_once()

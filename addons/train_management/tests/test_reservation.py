from odoo.tests import tagged

from .common import TrainManagementTestCommon


@tagged("post_install", "-at_install")
class TestReservation(TrainManagementTestCommon):
    def test_reservation_day_planning_from_train(self):
        circuit = self._create_circuit()
        train = self._create_train(circuit)
        reservation = self.env["train_management.reservation"].create(
            {"name": "Seat block", "amount": 4, "train": train.id}
        )
        self.assertEqual(reservation.day_planning, self.day_planning)
        self.assertEqual(reservation.day_planning_date, self.day_planning.date)

    def test_reservation_station_ids_from_timetable(self):
        circuit = self._create_circuit()
        train = self._create_train_with_timetable(circuit)
        reservation = self.env["train_management.reservation"].create(
            {"name": "Seat block", "amount": 4, "train": train.id}
        )
        self.assertEqual(
            reservation.station_ids,
            self.station_a | self.station_b,
        )

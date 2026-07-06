from odoo.tests import tagged

from .common import TrainManagementTestCommon


@tagged("post_install", "-at_install")
class TestTrain(TrainManagementTestCommon):
    def test_train_composition_from_vehicles(self):
        circuit = self._create_circuit()
        train = self._create_train(circuit)
        vehicle_a = self._create_vehicle("Engine 1")
        vehicle_b = self._create_vehicle("Car 1")
        self.env["train_management.train_vehicle"].create(
            {"train": train.id, "vehicle": vehicle_b.id, "sequence": 2}
        )
        self.env["train_management.train_vehicle"].create(
            {"train": train.id, "vehicle": vehicle_a.id, "sequence": 1}
        )
        self.assertEqual(train.train_composition, "Engine 1, Car 1")

    def test_train_reservation_amount(self):
        circuit = self._create_circuit()
        train = self._create_train(circuit)
        self.env["train_management.reservation"].create(
            {"name": "Reservation A", "amount": 12, "train": train.id}
        )
        self.env["train_management.reservation"].create(
            {"name": "Reservation B", "amount": 8, "train": train.id}
        )
        self.assertEqual(train.reservation_amount, 20)

    def test_train_day_planning_from_circuit(self):
        circuit = self._create_circuit()
        train = self._create_train(circuit)
        self.assertEqual(train.day_planning_id, self.day_planning)

    def test_train_default_get_railway_company(self):
        self.day_planning.railway_company = self.railway_company
        circuit = self._create_circuit()
        defaults = self.env["train_management.train"].with_context(
            default_circuit=circuit.id
        ).default_get(["circuit", "railway_company"])
        self.assertEqual(defaults["railway_company"], self.railway_company.id)

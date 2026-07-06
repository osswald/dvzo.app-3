from odoo.tests import tagged

from .common import TrainManagementTestCommon


@tagged("post_install", "-at_install")
class TestCircuit(TrainManagementTestCommon):
    def test_circuit_total_frequency_and_distance(self):
        circuit = self._create_circuit()
        self._create_train(circuit, frequency=10, distance=20)
        self._create_train(circuit, frequency=5, distance=15)
        self.assertEqual(circuit.frequency, 15)
        self.assertEqual(circuit.distance, 35)

    def test_circuit_train_composition(self):
        circuit = self._create_circuit()
        vehicle_a = self._create_vehicle("Loco A")
        vehicle_b = self._create_vehicle("Car B")
        self.env["train_management.circuit_vehicle"].create(
            {"circuit": circuit.id, "vehicle": vehicle_b.id, "sequence": 2}
        )
        self.env["train_management.circuit_vehicle"].create(
            {"circuit": circuit.id, "vehicle": vehicle_a.id, "sequence": 1}
        )
        self.assertEqual(circuit.train_composition, "Loco A, Car B")

    def test_circuit_write_sets_train_railway_company(self):
        circuit = self._create_circuit()
        self.day_planning.railway_company = self.railway_company
        train = self._create_train(circuit)
        vehicle = self._create_vehicle("Loco 3")
        self.env["train_management.circuit_vehicle"].create(
            {"circuit": circuit.id, "vehicle": vehicle.id, "sequence": 1}
        )
        circuit.write({"name": "Railway sync"})
        self.assertEqual(train.railway_company, self.railway_company)

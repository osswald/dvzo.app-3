from datetime import date

from odoo.tests.common import TransactionCase


class TrainManagementTestCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_category = cls.env["res.partner.category"].create(
            {"name": "Shift Category"}
        )
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Shift Test Partner",
                "category_id": [(6, 0, [cls.partner_category.id])],
            }
        )
        cls.station_a = cls.env["train_management.station"].create(
            {
                "name": "Station A",
                "short_name": "STA",
                "didok": "1001",
                "bpuic": "1001001",
            }
        )
        cls.station_b = cls.env["train_management.station"].create(
            {
                "name": "Station B",
                "short_name": "STB",
                "didok": "1002",
                "bpuic": "1002002",
            }
        )
        cls.stop_code = cls.env["train_management.stop_code"].create(
            {
                "name": "Commercial Stop",
                "code": "C01",
                "type": "commercial",
            }
        )
        cls.work_position_type = cls.env["train_management.shift_position_type"].create(
            {
                "name": "Work",
                "work_time": 50,
                "is_work_time": True,
            }
        )
        cls.non_work_position_type = cls.env[
            "train_management.shift_position_type"
        ].create(
            {
                "name": "Break",
                "work_time": 0,
                "is_work_time": False,
            }
        )
        cls.day_planning = cls.env["train_management.day_planning"].create(
            {
                "name": "Test Day",
                "date": date(2024, 6, 15),
            }
        )
        cls.railway_company = cls.env["train_management.railway_company"].create(
            {"name": "Test Railway"}
        )

    def _create_shift_template(self, time_accountable_positions=None, **values):
        data = {
            "name": "S1",
            "label": "Morning Shift",
            "valid_from": date(2024, 1, 1),
            "valid_until": date(2024, 12, 31),
            "category": [(6, 0, [self.partner_category.id])],
        }
        data.update(values)
        template = self.env["train_management.shift_template"].create(data)
        positions = time_accountable_positions or [
            {
                "name": "Work block",
                "start_time": 8.0,
                "end_time": 12.0,
                "sequence": 1,
                "type": self.work_position_type.id,
                "start_station": self.station_a.id,
                "end_station": self.station_b.id,
            },
            {
                "name": "Break",
                "start_time": 12.0,
                "end_time": 13.0,
                "sequence": 2,
                "type": self.non_work_position_type.id,
                "start_station": self.station_a.id,
                "end_station": self.station_a.id,
            },
        ]
        for position in positions:
            position["shift_template"] = template.id
            self.env["train_management.shift_position"].create(position)
        return template

    def _create_vehicle(self, designation):
        return self.env["train_management.vehicle"].create(
            {
                "name": designation,
                "historicalDesignation": designation,
                "type": "engine",
            }
        )

    def _create_circuit(self, **values):
        data = {
            "name": "Test Circuit",
            "day_planning": self.day_planning.id,
        }
        data.update(values)
        return self.env["train_management.circuit"].create(data)

    def _create_train(self, circuit, **values):
        data = {
            "name": "Train 1",
            "circuit": circuit.id,
        }
        data.update(values)
        return self.env["train_management.train"].create(data)

    def _create_day_planning_shift(self, partner, shift_template, planning=None, **values):
        data = {
            "day_planning": (planning or self.day_planning).id,
            "shift": shift_template.id,
            "person": partner.id,
        }
        data.update(values)
        return self.env["train_management.day_planning_shift"].create(data)

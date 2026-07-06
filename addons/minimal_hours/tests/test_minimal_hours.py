from datetime import date
from unittest.mock import patch

from odoo.tests import tagged

from odoo.addons.train_management.tests.common import TrainManagementTestCommon


@tagged("post_install", "-at_install")
class TestMinimalHours(TrainManagementTestCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.today = date(2024, 6, 15)
        cls.hours_category = cls.env["res.partner.category"].create(
            {
                "name": "VTE 100h",
                "minimal_hours_vte": 100,
                "minimal_shifts": 0,
            }
        )
        cls.shifts_category = cls.env["res.partner.category"].create(
            {
                "name": "VTE 2 shifts",
                "minimal_hours_vte": 0,
                "minimal_shifts": 2,
            }
        )
        cls.full_work_type = cls.env["train_management.shift_position_type"].create(
            {
                "name": "Full work",
                "work_time": 100,
                "is_work_time": True,
            }
        )

    def setUp(self):
        super().setUp()
        self.date_patcher = patch(
            "odoo.addons.minimal_hours.models.res_partner.date"
        )
        self.mock_date = self.date_patcher.start()
        self.mock_date.today.return_value = self.today
        self.addCleanup(self.date_patcher.stop)

    def _create_hours_shift_template(self, accountable_hours):
        return self._create_shift_template(
            time_accountable_positions=[
                {
                    "name": "Work block",
                    "start_time": 0.0,
                    "end_time": float(accountable_hours),
                    "sequence": 1,
                    "type": self.full_work_type.id,
                    "start_station": self.station_a.id,
                    "end_station": self.station_b.id,
                }
            ]
        )

    def _assign_shift(self, partner, shift_template, shift_date):
        planning = self.env["train_management.day_planning"].create(
            {
                "name": "Planning %s" % shift_date,
                "date": shift_date,
            }
        )
        return self._create_day_planning_shift(
            partner,
            shift_template,
            planning=planning,
        )

    def test_min_hours_from_categories(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Hours Partner",
                "category_id": [
                    (
                        6,
                        0,
                        [
                            self.env["res.partner.category"]
                            .create({"name": "Low", "minimal_hours_vte": 40})
                            .id,
                            self.hours_category.id,
                        ],
                    )
                ],
            }
        )
        self.assertEqual(partner.min_hours_category, 100)
        self.assertEqual(partner.min_shifts_category, 0)

    def test_hours_worked_current_year(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Worked Partner",
                "category_id": [(6, 0, [self.hours_category.id])],
            }
        )
        template = self._create_hours_shift_template(30)
        self._assign_shift(partner, template, date(2024, 3, 1))
        self._assign_shift(partner, template, date(2024, 5, 1))
        self.assertEqual(partner.hours_worked_current_year, 60)

    def test_hours_planned_current_year(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Planned Partner",
                "category_id": [(6, 0, [self.hours_category.id])],
            }
        )
        template = self._create_hours_shift_template(25)
        self._assign_shift(partner, template, date(2024, 9, 1))
        self.assertEqual(partner.hours_planned_current_year, 25)

    def test_goal_unknown_no_threshold(self):
        partner = self.env["res.partner"].create({"name": "Unknown Partner"})
        self.assertEqual(partner.goal_reached_current_year, "unknown")

    def test_goal_reached_hours(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Reached Partner",
                "category_id": [(6, 0, [self.hours_category.id])],
            }
        )
        template = self._create_hours_shift_template(50)
        self._assign_shift(partner, template, date(2024, 2, 1))
        self._assign_shift(partner, template, date(2024, 4, 1))
        self.assertEqual(partner.goal_reached_current_year, "reached")

    def test_goal_reachable_hours(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Reachable Partner",
                "category_id": [(6, 0, [self.hours_category.id])],
            }
        )
        template = self._create_hours_shift_template(50)
        self._assign_shift(partner, template, date(2024, 2, 1))
        self._assign_shift(partner, template, date(2024, 9, 1))
        self.assertEqual(partner.goal_reached_current_year, "reachable")

    def test_goal_not_reachable_hours(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Not Reachable Partner",
                "category_id": [(6, 0, [self.hours_category.id])],
            }
        )
        template = self._create_hours_shift_template(30)
        self._assign_shift(partner, template, date(2024, 2, 1))
        self.assertEqual(partner.goal_reached_current_year, "not_reachable")

    def test_goal_reached_shifts_only(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Shifts Partner",
                "category_id": [(6, 0, [self.shifts_category.id])],
            }
        )
        template = self._create_shift_template()
        self._assign_shift(partner, template, date(2024, 2, 1))
        self._assign_shift(partner, template, date(2024, 4, 1))
        self.assertEqual(partner.goal_reached_current_year, "reached")

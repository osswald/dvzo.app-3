from odoo.tests import tagged

from .common import TrainManagementTestCommon


@tagged("post_install", "-at_install")
class TestDayPlanningShift(TrainManagementTestCommon):
    def test_shift_offers_html(self):
        template = self._create_shift_template()
        shift = self.env["train_management.day_planning_shift"].create(
            {
                "day_planning": self.day_planning.id,
                "shift": template.id,
            }
        )
        offer_partner = self.env["res.partner"].create(
            {"name": "Offer Partner", "email": "offer@test.example"}
        )
        self.env["train_management.day_planning_shift_offer"].create(
            {
                "day_planning_shift": shift.id,
                "person": offer_partner.id,
                "offer": "yes",
                "comment": "Available",
            }
        )
        self.env["train_management.day_planning_shift_offer"].create(
            {
                "day_planning_shift": shift.id,
                "person": self.partner.id,
                "offer": "no",
            }
        )
        self.assertIn("Offer Partner", shift.offers)
        self.assertIn("Available", shift.offers)
        self.assertIn("fa-check", shift.offers)
        self.assertIn("fa-times", shift.offers)

    def test_shift_offer_day_planning_compute(self):
        template = self._create_shift_template()
        shift = self._create_day_planning_shift(self.partner, template)
        offer = self.env["train_management.day_planning_shift_offer"].create(
            {
                "day_planning_shift": shift.id,
                "person": self.partner.id,
                "offer": "possible",
            }
        )
        self.assertEqual(offer.day_planning, self.day_planning)
        self.assertEqual(offer.day_planning_date, self.day_planning.date)

    def test_open_form_view_action(self):
        template = self._create_shift_template()
        shift = self._create_day_planning_shift(self.partner, template)
        action = shift.open_form_view()
        self.assertEqual(action["res_model"], "train_management.day_planning_shift")
        self.assertEqual(action["res_id"], shift.id)
        self.assertEqual(action["view_mode"], "form")

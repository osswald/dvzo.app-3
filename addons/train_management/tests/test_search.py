from odoo.tests import tagged

from .common import TrainManagementTestCommon


@tagged("post_install", "-at_install")
class TestTrainManagementSearch(TrainManagementTestCommon):
    def test_station_name_search_by_short_name(self):
        results = self.env["train_management.station"].name_search("STA")
        self.assertIn(self.station_a.id, [result[0] for result in results])

    def test_stop_code_name_search_by_code(self):
        results = self.env["train_management.stop_code"].name_search("C01")
        self.assertIn(self.stop_code.id, [result[0] for result in results])

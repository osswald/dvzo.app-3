from odoo.exceptions import UserError
from odoo.tests import tagged

from .common import TrainingTestCommon


@tagged("post_install", "-at_install")
class TestTrainingState(TrainingTestCommon):
    def test_planned_to_running(self):
        training = self._create_training()
        training.action_running()
        self.assertEqual(training.state, "running")

    def test_archived_to_running_raises(self):
        training = self._create_training()
        training.action_archived()
        with self.assertRaises(UserError):
            training.action_running()

    def test_canceled_to_archived_raises(self):
        training = self._create_training()
        training.action_canceled()
        with self.assertRaises(UserError):
            training.action_archived()

    def test_canceled_to_planned_raises(self):
        training = self._create_training()
        training.action_canceled()
        with self.assertRaises(UserError):
            training.action_planned()

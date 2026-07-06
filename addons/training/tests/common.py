from datetime import date

from odoo.tests.common import TransactionCase


class TrainingTestCommon(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create(
            {"name": "Training Test Partner", "email": "training@test.example"}
        )
        cls.qualification_type = cls.env["training.qualification.type"].create(
            {"name": "Test Qualification Type"}
        )
        cls.qualification_category = cls.env["training.qualification.category"].create(
            {
                "name": "Test Qualification Category",
                "type": cls.qualification_type.id,
            }
        )
        cls.competence_category = cls.env["res.partner.category"].create(
            {"name": "Test Competence"}
        )

    def _create_training(self, **values):
        data = {
            "name": "TRN",
            "label": "Test Training",
            "responsible": self.partner.id,
        }
        data.update(values)
        return self.env["training.training"].create(data)

    def _create_exam(self, partner=None, valid_until=None, **values):
        data = {
            "type": self.qualification_type.id,
            "category": self.qualification_category.id,
            "date": date(2024, 1, 1),
            "valid_until": valid_until or date(2025, 12, 31),
            "person": (partner or self.partner).id,
            "competence": [(6, 0, [self.competence_category.id])],
        }
        data.update(values)
        return self.env["training.exam"].create(data)

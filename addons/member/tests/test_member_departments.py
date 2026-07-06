from odoo.tests import tagged

from .common import MemberTestCommon


@tagged("post_install", "-at_install")
class TestMemberDepartments(MemberTestCommon):
    def test_compute_departments(self):
        self._add_department(self.partner, self.department_ops, self.type_member)
        self._add_department(self.partner, self.department_board, self.type_admin)
        self.assertEqual(
            self.partner.departments,
            "Operations - Member\nBoard - Admin",
        )

    def test_compute_department_hidden(self):
        self._add_department(self.partner, self.department_ops, self.type_member)
        self._add_department(self.partner, self.department_board, self.type_admin)
        self.assertEqual(
            self.partner.department_hidden,
            self.department_ops | self.department_board,
        )

    def test_compute_department_admin(self):
        self._add_department(self.partner, self.department_ops, self.type_member)
        self._add_department(self.partner, self.department_board, self.type_admin)
        self.assertEqual(self.partner.department_admin, self.department_board)

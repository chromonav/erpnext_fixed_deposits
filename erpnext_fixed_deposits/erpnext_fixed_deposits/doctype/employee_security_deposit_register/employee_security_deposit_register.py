# Copyright (c) 2023, Hybrowlabs Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeeSecurityDepositRegister(Document):
    def before_save(self):
        self.calculate_interest()

    def calculate_interest(self):
        self.interest_amount = (self.deposit_amount * self.rate_of_interest * self.quarterly_duration)/100
        self.total_amount = self.deposit_amount + self.interest_amount

    def validate(self):
        if self.deposit_amount <= 0:
            frappe.throw("Deposit Amount should be greater than zero")

        if self.rate_of_interest <= 0:
            frappe.throw("Rate of Interest should be greater than zero")

        if self.quarterly_duration <= 0:
            frappe.throw("Quarterly Duration should be greater than zero")

    def on_update(self):
        if frappe.utils.date_diff(frappe.utils.nowdate(), self.date_of_joining) >= 1095 and frappe.utils.date_diff(frappe.utils.nowdate(), self.date_of_joining) < 1102:
            frappe.msgprint("Employee {0}'s deposit will be completed in one week.".format(self.employee_name))
        frappe.msgprint("Employee Security Deposit Register updated successfully!")

